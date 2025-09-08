# MCP statistical analysis tools that can be used by AI agents

# prints out interesting numbers about the data
def printCoolStats(data):
    print("=" * 45)
    print("NBA 3-POINTER EVOLUTION")
    print("=" * 45)

    # split up data by era
    oldSchool = data[data['era'] == 'Old School']
    modern = data[data['era'] == 'Modern Era']

    print(f"\nOld School Days (1984-1996):")
    print(f"  Average attempts: {oldSchool['attemptsPerGame'].mean():.1f} per game")
    print(f"  Shooting pct: {oldSchool['threePtPct'].mean():.1%}")

    print(f"\nModern NBA (2014-2023):")
    print(f"  Average attempts: {modern['attemptsPerGame'].mean():.1f} per game")
    print(f"  Shooting pct: {modern['threePtPct'].mean():.1%}")

    # calculate the crazy increase using ratio math
    increaseRatio = (modern['attemptsPerGame'].mean() /
                     oldSchool['attemptsPerGame'].mean() - 1) * 100

    print(f"\nTHE BIG PICTURE:")
    print(f"  3-point attempts went up {increaseRatio:.0f}%!")
    print(f"  Highest year: {data.loc[data['attemptsPerGame'].idxmax(), 'year']}")  # idxmax finds index of max value

    # find some other interesting stuff using loc indexer
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


# calculates year-over-year changes
def findBiggestJumps(data):
    # sort by year first using sort_values
    dataSorted = data.sort_values('year')

    # calculate yr-to-yr changes using diff() which subtracts previous row
    dataSorted['changeFromPrevYr'] = dataSorted['attemptsPerGame'].diff()

    print(f"\nBIGGEST YEAR-TO-YEAR JUMPS:")
    biggestIncreases = dataSorted.nlargest(3, 'changeFromPrevYr')  # nlargest gets top 3

    for _, row in biggestIncreases.iterrows():  # iterrows loops through df rows
        if row['changeFromPrevYr'] > 0:  # only positive changes
            print(f"  {int(row['year'])}: +{row['changeFromPrevYr']:.1f} more attempts")


# basic summary stats - learned this in stats class
def eraSummaryTable(data):
    print(f"\nSUMMARY TABLE BY ERA:")
    print("-" * 50)

    # agg() applies multiple functions to grouped data
    summary = data.groupby('era').agg({
        'attemptsPerGame': ['mean', 'std', 'min', 'max'],  # std=standard deviation
        'threePtPct': ['mean', 'std'],
        'ptsPerGame': 'mean'
    }).round(2)  # round to 2 decimal places

    #
    summary.columns = ['AvgAttempts', 'StdAttempts', 'MinAttempts', 'MaxAttempts',
                       'AvgPct', 'StdPct', 'AvgPts']

    print(summary)


# returns structured data instead of printing
def getMcpStatsAnalysis(data):
    oldSchool = data[data['era'] == 'Old School']
    growing = data[data['era'] == 'Growing Up']
    modern = data[data['era'] == 'Modern Era']

    # calculate yr-over-yr changes
    dataSorted = data.sort_values('year')
    dataSorted['change'] = dataSorted['attemptsPerGame'].diff()
    biggestJump = dataSorted.loc[dataSorted['change'].idxmax()]

    return {
        'mcpToolUsed': 'getMcpStatsAnalysis',
        'eraComparison': {
            'oldSchool': {
                'avgAttempts': round(oldSchool['attemptsPerGame'].mean(), 2),
                'avgPct': round(oldSchool['threePtPct'].mean(), 3),
                'yearRange': '1984-1996'
            },
            'growingUp': {
                'avgAttempts': round(growing['attemptsPerGame'].mean(), 2),
                'avgPct': round(growing['threePtPct'].mean(), 3),
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
                (modern['attemptsPerGame'].mean() / oldSchool['attemptsPerGame'].mean() - 1) * 100, 1),
            'peakYear': int(data.loc[data['attemptsPerGame'].idxmax(), 'year']),
            'biggestYearlyJump': {
                'year': int(biggestJump['year']),
                'increase': round(biggestJump['change'], 2)
            }
        }
    }


# runs all the stats funcs - main entry point for analysis
def runAllStats(data):
    printCoolStats(data)
    findBiggestJumps(data)
    eraSummaryTable(data)