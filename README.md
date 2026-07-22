# Equity Nexus

## Multi-Agent Investment Research System

Equity Nexus is a prototype multi-agent system that demonstrates how specialized AI agents can work together to produce investment research and recommendations.

---

## Problem Statement

Individual investors often struggle to synthesize large volumes of market data, financial metrics, and news sentiment into a coherent investment decision. Manually cross-referencing multiple data sources is time-consuming and prone to bias.

Equity Nexus addresses this by using a pipeline of specialized agents, each responsible for one aspect of the analysis, that combine their outputs into a single, actionable recommendation.

---

## Objectives

1. Demonstrate a sequential multi-agent workflow for investment research.
2. Separate concerns: sentiment analysis, fundamental analysis, and decision-making are handled by independent agents.
3. Produce a structured, readable output that includes a recommendation, confidence level, and investment thesis.
4. Provide a foundation for future integration with real financial data APIs and LLM-powered analysis.

---

## Agent Descriptions

### Agent 1: MarketSentimentAgent

| Attribute       | Value                                      |
|-----------------|--------------------------------------------|
| **Input**       | Company name and stock ticker              |
| **Analyzes**    | News articles and earnings call transcripts |
| **Output**      | SentimentReport (sentiment label, score, news summary, highlights) |

This agent simulates the process of gathering and analyzing market sentiment. In a production system, it would fetch real news articles and earnings call transcripts and apply NLP-based sentiment analysis.

---

### Agent 2: FundamentalAnalysisAgent

| Attribute       | Value                                      |
|-----------------|--------------------------------------------|
| **Input**       | Company name and stock ticker              |
| **Analyzes**    | Revenue growth, P/E ratio, debt-to-equity, profit margin |
| **Output**      | FinancialReport (metrics, valuation, financial health) |

This agent simulates the retrieval and evaluation of key financial metrics. In a production system, it would query financial data APIs such as Yahoo Finance or Alpha Vantage.

---

### Agent 3: InvestmentDecisionAgent

| Attribute       | Value                                      |
|-----------------|--------------------------------------------|
| **Input**       | SentimentReport + FinancialReport          |
| **Analyzes**    | Combined scores from both previous agents  |
| **Output**      | InvestmentDecision (recommendation, confidence, thesis, risks) |

This agent is the final step in the pipeline. It weighs sentiment and fundamental data to produce a BUY, HOLD, or SELL recommendation, along with a confidence level and a short investment thesis.

---

## Workflow

```
User Input (Company Name)
        |
        v
+---------------------------+
| MarketSentimentAgent      |
| -> SentimentReport        |
+---------------------------+
        |
        v
+---------------------------+
| FundamentalAnalysisAgent  |
| -> FinancialReport        |
+---------------------------+
        |
        v
+---------------------------+
| InvestmentDecisionAgent   |
| -> InvestmentDecision     |
+---------------------------+
        |
        v
   Final Output
   (Recommendation, Confidence, Thesis, Risks)
```

Each agent runs sequentially. The output of one agent feeds into the next, forming a clean data pipeline.

---

## Project Structure

```
EquityNexus/
│
├── agents/
│   ├── __init__.py              # Package initializer
│   ├── market_sentiment.py      # Agent 1: Sentiment analysis
│   ├── fundamental_analysis.py  # Agent 2: Financial metrics
│   └── investment_decision.py   # Agent 3: Final recommendation
│
├── main.py                      # Entry point and workflow driver
├── README.md                    # This file
└── requirements.txt             # Python dependencies
```

---

## Requirements

- Python 3.7 or higher
- No external libraries required (uses only Python standard library)

---

## How to Run

1. **Clone or download** this project to your local machine.

2. **Navigate** to the project directory:
   ```bash
   cd EquityNexus
   ```

3. **Run** the main script:
   ```bash
   python3 main.py
   ```

4. **Enter a company name** when prompted (e.g., `Tesla`, `Apple`, `Microsoft`, `Amazon`, `Google`).

5. **View** the three-part analysis:
   - Market Sentiment Report
   - Fundamental Analysis Report
   - Final Investment Recommendation

---

## Sample Output

```
==================================================
           EQUITY NEXUS
   Multi-Agent Investment Research System
==================================================

  STEP 1: Company Selection
  ----------------------------------------------
  Enter company name (e.g., Tesla, Apple, Microsoft): Tesla

  >> Analyzing Tesla (TSLA)...

  STEP 2: Running MarketSentimentAgent...
  [MarketSentimentAgent] Analyzing market sentiment for Tesla (TSLA)...
  [MarketSentimentAgent] Sentiment analysis complete.

  === Market Sentiment Report ===

  Company:              Tesla (TSLA)
  Overall Sentiment:    Positive
  Sentiment Score:      0.6
  ...
```

---

## Future Enhancements

- **Real API Integration**: Connect to Yahoo Finance, Alpha Vantage, and news APIs for live data.
- **LLM-Powered Analysis**: Use large language models for deeper sentiment analysis and thesis generation.
- **Web Interface**: Build a Streamlit or Flask frontend for interactive use.
- **Backtesting**: Add historical performance evaluation of past recommendations.
- **Multi-Company Comparison**: Allow users to compare multiple stocks side by side.

---

## License

This project is for educational purposes as part of the Silicon Valley AI Fellowship.
