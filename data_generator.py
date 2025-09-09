import pandas as pd
import numpy as np
import json

# MCP Tool: generates NBA data - this func could be exposed as an MCP tool for AI agents
def createNbaData():
    years = list(range(1984, 2024)) # Year Jordan joined
    dataList = []

    for yr in years:
        # diff eras had diff shooting patterns, helps MCP understand trends
        if yr < 1997:  # old  era
            avgAttempts = np.random.normal(2.5 + (yr - 1984) * 0.1, 0.3)  # loc=mean, scale=std_dev
            shootingPct = np.random.normal(0.28, 0.02)
        elif yr < 2014:  # GSW transition
            avgAttempts = np.random.normal(12 + (yr - 1997) * 0.3, 1.0) # # of attempts + (yr- min(year)) * mean, std_dev
            shootingPct = np.random.normal(0.35, 0.015) # normal distro at 35% with .015 std_Dev
        else:  # modern nba boom
            avgAttempts = np.random.normal(22 + (yr - 2014) * 1.2, 2.0)
            shootingPct = np.random.normal(0.365, 0.01)

        # basic math to get pts from threes
        ptsFromThrees = avgAttempts * shootingPct * 3 # 3ball based on shootingPct

        dataList.append({
            'year': yr,
            'attemptsPerGame': avgAttempts,
            'threePtPct': max(0.2, min(0.4, shootingPct)),  # keep between 20-40% we don't need random 3s from non shooters
            'ptsPerGame': ptsFromThrees,
            'era': getEraName(yr)
        })

    return pd.DataFrame(dataList) # return new data list


# era labels
def getEraName(yr):
    if yr < 1997:
        return "Old Era"
    elif yr < 2014:
        return "New Era"
    else:
        return "Modern Era"


# MCP save func - outputs JSON for protocol integration
def saveDataForMcp():
    df = createNbaData()

    # save as CSV for human analysis
    df.to_csv('nba_data.csv', index=False)

    # save as JSON for MCP tools
    dataDict = df.to_dict('records')  # converts df to list of dicts
    mcpOutput = {
        'metadata': {
            'source': 'NBA 3-Point Analysis MCP Tool',
            'years_covered': '1984-2024',
            'totalDataPts': len(dataDict),
            'mcpVersion': '1.0',
            'toolCapabilities': ['data_generation', 'era_analysis', 'trend_detection']
        },
        'schema': {
            'year': 'integer',
            'attemptsPerGame': 'float',
            'threePtPct': 'float',
            'ptsPerGame': 'float',
            'era': 'string'
        },
        'data': dataDict
    }

    with open('nba_data_mcp.json', 'w') as f:
        json.dump(mcpOutput, f, indent=2)

    return df


# AI agent could call this to get specific era stats
def getEraStatsForMcp(eraName):
    df = createNbaData() # creates dataframe from what was made above
    eraData = df[df['era'] == eraName] # era data come from era name

    if eraData.empty:
        return {"error": f"Era '{eraName}' not found"}

    # return structured data that MCP can easily parse and use
    return {
        'requestedEra': eraName,
        'avgAttempts': round(eraData['attemptsPerGame'].mean(), 2),
        'avgPct': round(eraData['threePtPct'].mean(), 3),
        'avgPts': round(eraData['ptsPerGame'].mean(), 2),
        'yearRange': f"{eraData['year'].min()}-{eraData['year'].max()}",
        'sampleSize': len(eraData),
        'mcpToolUsed': 'getEraStatsForMcp'
    }