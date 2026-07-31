  """
Equity Nexus - Main Workflow
=============================
Multi-Agent Investment Research System

This script demonstrates the Equity Nexus workflow using sample data.
Three specialized agents work sequentially to produce an investment recommendation:

    1. MarketSentimentAgent  -> Analyzes news and sentiment
    2. FundamentalAnalysisAgent -> Analyzes financial metrics
    3. InvestmentDecisionAgent -> Combines reports and recommends

Workflow:
    Step 1: User enters a company name or stock ticker
    Step 2: MarketSentimentAgent produces a sentiment report
    Step 3: FundamentalAnalysisAgent produces a financial report
    Step 4: InvestmentDecisionAgent produces a final recommendation

To run: python3 main.py
"""

import agenthog

# --------------------------------------------------------------------------
# IMPORTANT: Replace the two values below with YOUR real credentials.
# Get your API key from: app.theagentos.space -> Settings -> API Keys
# Get your Workspace ID from the SAME page (Settings -> API Keys) --
# do NOT use a workspace ID copied from a generic docs/quickstart example.
# --------------------------------------------------------------------------
agenthog.init(
    api_key="agops_3VlAtt8-yxOfMOA0h9SgA1PpUUYr_N0E",
    workspace_id="3153d277-1857-44fc-b3a8-a882e83f8493",
)

# ------------------------------------------------------------------
# Import the three agents
# ------------------------------------------------------------------
from agents.market_sentiment import MarketSentimentAgent
from agents.fundamental_analysis import FundamentalAnalysisAgent
from agents.investment_decision import InvestmentDecisionAgent


# ------------------------------------------------------------------
# Display Helpers
# ------------------------------------------------------------------

def print_banner():
    """Print the professional welcome banner."""
    print()
    print("=" * 50)
    print("           EQUITY NEXUS")
    print("   Multi-Agent Investment Research System")
    print("=" * 50)
    print()


def print_section_header(title):
    """
    Print a formatted section header.

    Args:
        title (str): The section title to display.
    """
    print()
    print(f"  === {title} ===")
    print()


def print_separator():
    """Print a thin separator line for visual spacing."""
    print("  " + "-" * 46)


# ------------------------------------------------------------------
# Report Display Functions
# ------------------------------------------------------------------

def display_sentiment_report(report):
    """
    Display the Market Sentiment Report in a clean format.

    Args:
        report (SentimentReport): The output from MarketSentimentAgent.
    """
    print_section_header("Market Sentiment Report")

    print(f"  Company:              {report.company} ({report.ticker})")
    print(f"  Overall Sentiment:    {report.overall_sentiment}")
    print(f"  Sentiment Score:      {report.sentiment_score}")
    print()
    print_separator()
    print()
    print(f"  News Summary:")
    print(f"    {report.news_summary}")
    print()
    print(f"  Earnings Call Tone:")
    print(f"    {report.earnings_call_sentiment}")
    print()
    print_separator()
    print()
    print(f"  Positive Factors:")
    for highlight in report.key_highlights:
        print(f"    + {highlight}")
    print()
    print(f"  Risks:")
    if report.sentiment_score < 0:
        print("    - Negative media coverage detected.")
    else:
        print("    - No major sentiment risks flagged.")
    print()


def display_financial_report(report):
    """
    Display the Fundamental Analysis Report in a clean format.

    Args:
        report (FinancialReport): The output from FundamentalAnalysisAgent.
    """
    print_section_header("Fundamental Analysis Report")

    print(f"  Company:              {report.company} ({report.ticker})")
    print()
    print(f"  Revenue Growth:       {report.revenue_growth}%")
    print(f"  P/E Ratio:            {report.pe_ratio}")
    print(f"  Debt-to-Equity:       {report.debt_to_equity}")
    print(f"  Profit Margin:        {report.profit_margin}%")
    print()
    print_separator()
    print()
    print(f"  Valuation:            {report.valuation}")
    print(f"  Financial Health:     {report.financial_health}")
    print()


def display_investment_decision(decision):
    """
    Display the Final Investment Recommendation in a clean format.

    Args:
        decision (InvestmentDecision): The output from InvestmentDecisionAgent.
    """
    print_section_header("Final Investment Recommendation")

    print(f"  Company:              {decision.company} ({decision.ticker})")
    print(f"  Recommendation:       {decision.recommendation}")
    print(f"  Confidence:           {int(decision.confidence_level * 100)}%")
    print()
    print_separator()
    print()
    print(f"  Investment Thesis:")
    print(f"    {decision.investment_thesis}")
    print()
    print_separator()
    print()
    print(f"  Risk Factors:")
    for risk in decision.risk_factors:
        print(f"    ! {risk}")
    print()
    print("=" * 50)
    print()


# ------------------------------------------------------------------
# Main Workflow
# ------------------------------------------------------------------

def main():
    """
    Run the Equity Nexus investment analysis workflow.

    This function orchestrates the three-agent pipeline:
        1. Get user input (company name or ticker)
        2. Run MarketSentimentAgent -> sentiment report
        3. Run FundamentalAnalysisAgent -> financial report
        4. Run InvestmentDecisionAgent -> final recommendation
    """

    # Display the welcome banner
    print_banner()

    # ------------------------------------------------------------------
    # STEP 1: Get user input
    # ------------------------------------------------------------------
    print("  STEP 1: Company Selection")
    print_separator()
    print()

    # Prompt user for a company name
    company_name = input("  Enter company name (e.g., Tesla, Apple, Microsoft): ").strip()

    # Map common company names to ticker symbols
    # In production, this would query a stock symbol lookup API
    ticker_map = {
        "Tesla": "TSLA",
        "Apple": "AAPL",
        "Microsoft": "MSFT",
        "Amazon": "AMZN",
        "Google": "GOOGL"
    }

    # Look up the ticker, or default to UNKNOWN
    ticker = ticker_map.get(company_name, "UNKNOWN")

    print()
    print(f"  >> Analyzing {company_name} ({ticker})...")
    print()

    with agenthog.start_task_run(task_run_id="equity_nexus_research") as run:
        # ------------------------------------------------------------------
        # STEP 2: Run MarketSentimentAgent
        # ------------------------------------------------------------------
        print("  STEP 2: Running MarketSentimentAgent...")
        sentiment_agent = MarketSentimentAgent()
        sentiment_report = sentiment_agent.analyze(company_name, ticker)

        # Display the sentiment report
        display_sentiment_report(sentiment_report)

        # ------------------------------------------------------------------
        # STEP 3: Run FundamentalAnalysisAgent
        # ------------------------------------------------------------------
        print("  STEP 3: Running FundamentalAnalysisAgent...")
        fundamental_agent = FundamentalAnalysisAgent()
        financial_report = fundamental_agent.analyze(company_name, ticker)

        # Display the financial report
        display_financial_report(financial_report)

        # ------------------------------------------------------------------
        # STEP 4: Run InvestmentDecisionAgent
        # ------------------------------------------------------------------
        print("  STEP 4: Running InvestmentDecisionAgent...")
        decision_agent = InvestmentDecisionAgent()
        investment_decision = decision_agent.analyze(sentiment_report, financial_report)

        # Display the final recommendation
        display_investment_decision(investment_decision)

    # Block here until AgentOS confirms the trace has actually been sent.
    print("  Sending trace data to AgentOS, please wait...")
    agenthog.shutdown()
    print("  Trace sent. Check the Traces page on app.theagentos.space.")


# ------------------------------------------------------------------
# Entry Point
# ------------------------------------------------------------------
if __name__ == "__main__":
    main()
    
