# this shows how AI agents could use these tools to analyze NBA data

from data_generator import createNbaData, saveDataForMcp, getEraStatsForMcp
from plotter import *
from stats_calculator import runAllStats, getMcpStatsAnalysis

import json

# this is how MCP would work as an NBA analysis tools
def demonstrateMcpUsage():
    print("=" * 60)
    print("MCP TOOLS DEMONSTRATION")
    print("=" * 60)

    # simulate an AI agent requesting era-specific data through MCP
    print("1. AI Agent Request: 'Get stats for Modern Era'")
    analyticsStats = getEraStatsForMcp("Modern Era")
    print("\tMCP Response:")
    print(json.dumps(analyticsStats, indent=4))

    print("\n" + "-" * 50)

    # simulate AI requesting structured analysis
    print("2. AI Agent Request: 'Provide comprehensive statistical analysis'")
    nbaData = createNbaData()
    mcpAnalysis = getMcpStatsAnalysis(nbaData)
    print("\tMCP Response:")
    print(json.dumps(mcpAnalysis, indent=4))

# runs the whole analysis with MCP integration
def main():
# get our realistic fake data
    nbaData = createNbaData()

    # demonstrate MCP protocol usage first
    demonstrateMcpUsage()

    # then show  analysis
    runAllStats(nbaData)

    # these function calls could be made by an AI agent via MCP
    plotAttemptsTimeline(nbaData)
    plotEraBoxplots(nbaData)

    # save data in MCP-compatible format
    saveDataForMcp()

if __name__ == "__main__":
    main()