# MCP statistical analysis tools that can be used by AI agents

# prints out interesting numbers about the data
def printCoolStats(data):
    print("=" * 45)
    print("NBA 3-POINTER EVOLUTION")
    print("=" * 45)

    # split up data by era
    oldEra = data[data['era'] == 'Old Era']
    newEra = data[data['era'] == 'New Era']
    modern = data[data['era'] == 'Modern Era']

    print(f"\nOld Era Days (1984-1996):")
    print(f"  Average attempts: {oldEra['attemptsPerGame'].mean():.1f} per game")
    print(f"  Shooting pct: {oldEra['threePtPct'].mean():.1%}")

    print(f"\nNew Era (1997-2013):")
    print(f"  Average attempts: {newEra['attemptsPerGame'].mean():.1f} per game")
    print(f"  Shooting pct: {newEra['threePtPct'].mean():.1%}")

    print(f"\nModern NBA (2014-2023):")
    print(f"  Average attempts: {modern['attemptsPerGame'].mean():.1f} per game")
    print(f"  Shooting pct: {modern['threePtPct'].mean():.1%}")

    bestShootingYr = data.loc[data['threePtPct'].idxmax()]
    worstShootingYr = data.loc[data['threePtPct'].idxmin()]

    print(f"\nFUN FACTS:")
    print(f"  Best shooting yr: {bestShootingYr['year']} at {bestShootingYr['threePtPct']:.1%}")
    print(f"  Worst shooting yr: {worstShootingYr['year']} at {worstShootingYr['threePtPct']:.1%}")

    # era comparisons using unique() to get distinct values
    print(f"\nERA BREAKDOWN:")
    for era in data['era'].unique():
        eraData = data[data['era'] == era]
        print(f"  {era}: {eraData['attemptsPerGame'].mean():.1f} attempts avg")

# basic summary stats - learned this in stats class
def eraSummaryTable(data):
    print(f"\nSUMMARY TABLE BY ERA:")
    print("-" * 50)

    # agg() applies multiple functions to grouped data
    summary = data.groupby('era').agg({
        'attemptsPerGame': ['mean', 'std', 'min', 'max'],
        'threePtPct': 'mean',
        'ptsPerGame': 'mean'
    }).round(2)  # round to 2 decimal places

    #
    summary.columns = ['AvgAttempts', 'StdAttempts', 'MinAttempts',
                       'MaxAttempts', 'AvgPct', 'AvgPts']

    print(summary)


# returns structured data instead of printing
def getMcpStatsAnalysis(data):
    oldEra = data[data['era'] == 'Old Era']
    newEra = data[data['era'] == 'New Era']
    modern = data[data['era'] == 'Modern Era']

    # calculate yr-over-yr changes
    dataSorted = data.sort_values('year')
    dataSorted['change'] = dataSorted['attemptsPerGame'].diff()
    biggestJump = dataSorted.loc[dataSorted['change'].idxmax()]

    return {
        'mcpToolUsed': 'getMcpStatsAnalysis',
        'eraComparison': {
            'oldEra': {
                'avgAttempts': round(oldEra['attemptsPerGame'].mean(), 2),
                'avgPct': round(oldEra['threePtPct'].mean(), 3),
                'yearRange': '1984-1996'
            },
            'newEra': {
                'avgAttempts': round(newEra['attemptsPerGame'].mean(), 2),
                'avgPct': round(newEra['threePtPct'].mean(), 3),
                'yearRange': '1997-2013'
            },
            'modernEra': {
                'avgAttempts': round(modern['attemptsPerGame'].mean(), 2),
                'avgPct': round(modern['threePtPct'].mean(), 3),
                'yearRange': '2014-2023'
            }
        },
        'overallTrends': {
            'totalIncreasePct': round(
                (modern['attemptsPerGame'].mean() / oldEra['attemptsPerGame'].mean() - 1) * 100, 1),
            'peakYear': int(data.loc[data['attemptsPerGame'].idxmax(), 'year']),
            'biggestYearlyJump': {
                'year': int(biggestJump['year']),
                'increase': round(biggestJump['change'], 2)
            }
        }
    }

# runs all the stats funcs
def runAllStats(data):
    printCoolStats(data)
    eraSummaryTable(data)