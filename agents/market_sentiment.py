"""
MarketSentimentAgent
====================
This agent simulates the analysis of market sentiment for a given company.
In a production environment, it would fetch and analyze:
    - Recent news articles
    - Earnings call transcripts
    - Social media sentiment
    - Analyst opinions

For this prototype, it returns pre-built sample data to demonstrate the workflow.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class SentimentReport:
    """
    Data structure that holds the output of the sentiment analysis.

    Attributes:
        company (str): The company name.
        ticker (str): The stock ticker symbol.
        overall_sentiment (str): Label - Positive, Neutral, or Negative.
        sentiment_score (float): Numerical score from -1.0 (very negative) to 1.0 (very positive).
        news_summary (str): A summary of recent news sentiment.
        earnings_call_sentiment (str): A summary of the latest earnings call tone.
        key_highlights (list): Notable positive or negative highlights.
    """
    company: str
    ticker: str
    overall_sentiment: str
    sentiment_score: float
    news_summary: str
    earnings_call_sentiment: str
    key_highlights: List[str]


class MarketSentimentAgent:
    """
    Agent that analyzes market sentiment for a company.

    This agent processes news and earnings call data to determine
    the overall market sentiment toward a stock. It combines multiple
    signals into a single sentiment score and report.
    """

    def __init__(self):
        self.agent_name = "MarketSentimentAgent"

    def analyze(self, company_name: str, ticker: str) -> SentimentReport:
        """
        Run sentiment analysis on the given company.

        Steps:
            1. Analyze recent news articles for sentiment.
            2. Analyze the latest earnings call for tone and sentiment.
            3. Combine both scores into an overall sentiment rating.
            4. Return a structured SentimentReport.

        Args:
            company_name (str): The name of the company.
            ticker (str): The stock ticker symbol.

        Returns:
            SentimentReport: A structured report with sentiment findings.
        """
        print(f"\n  [{self.agent_name}] Analyzing market sentiment for {company_name} ({ticker})...")

        # Step 1: Analyze news sentiment
        news = self._analyze_news(company_name)

        # Step 2: Analyze earnings call sentiment
        earnings = self._analyze_earnings_call(company_name)

        # Step 3: Combine scores (average of news and earnings)
        combined_score = (news["score"] + earnings["score"]) / 2

        # Step 4: Determine sentiment label based on combined score
        if combined_score > 0.2:
            sentiment_label = "Positive"
        elif combined_score < -0.2:
            sentiment_label = "Negative"
        else:
            sentiment_label = "Neutral"

        # Step 5: Build and return the report
        report = SentimentReport(
            company=company_name,
            ticker=ticker,
            overall_sentiment=sentiment_label,
            sentiment_score=round(combined_score, 2),
            news_summary=news["summary"],
            earnings_call_sentiment=earnings["summary"],
            key_highlights=[news["highlight"], earnings["highlight"]]
        )

        print(f"  [{self.agent_name}] Sentiment analysis complete.")
        return report

    def _analyze_news(self, company_name: str) -> dict:
        """
        Simulate analysis of recent news articles.

        In production, this would fetch articles from a news API
        and run NLP-based sentiment analysis on the headlines and content.

        Args:
            company_name (str): The company to look up.

        Returns:
            dict: Contains 'score' (float), 'summary' (str), and 'highlight' (str).
        """
        sample_news = {
            "Tesla": {
                "score": 0.65,
                "summary": "Recent coverage highlights strong EV demand and Tesla's expansion into new markets.",
                "highlight": "Positive media attention on new model announcements and production milestones."
            },
            "Apple": {
                "score": 0.70,
                "summary": "Apple continues to demonstrate strong brand loyalty and accelerating services growth.",
                "highlight": "Record-breaking services revenue reported in the latest quarter."
            },
            "Microsoft": {
                "score": 0.75,
                "summary": "Microsoft's AI and cloud segments are driving significant investor optimism.",
                "highlight": "Azure revenue growth exceeded analyst expectations."
            },
            "Amazon": {
                "score": 0.55,
                "summary": "AWS remains a growth engine while retail margins continue to improve.",
                "highlight": "Strong holiday season performance boosted overall revenue outlook."
            },
            "Google": {
                "score": 0.60,
                "summary": "Alphabet's search dominance and YouTube ad revenue are key positives.",
                "highlight": "AI-powered search features are expected to drive future engagement."
            }
        }

        return sample_news.get(company_name, {
            "score": 0.30,
            "summary": f"General market outlook for {company_name} is cautiously optimistic.",
            "highlight": f"Steady market interest and moderate analyst coverage for {company_name}."
        })

    def _analyze_earnings_call(self, company_name: str) -> dict:
        """
        Simulate analysis of the latest earnings call.

        In production, this would transcribe the call and analyze
        the language, tone, and key statements from executives.

        Args:
            company_name (str): The company to look up.

        Returns:
            dict: Contains 'score' (float), 'summary' (str), and 'highlight' (str).
        """
        sample_earnings = {
            "Tesla": {
                "score": 0.55,
                "summary": "Management expressed confidence in production targets and margin expansion.",
                "highlight": "CEO outlined a clear path to profitability in the energy division."
            },
            "Apple": {
                "score": 0.65,
                "summary": "Strong forward guidance with a major focus on AI integration across products.",
                "highlight": "CFO emphasized robust free cash flow and shareholder returns."
            },
            "Microsoft": {
                "score": 0.80,
                "summary": "Executives highlighted record cloud revenue and strong enterprise adoption of AI tools.",
                "highlight": "COO confirmed continued investment in data center infrastructure."
            },
            "Amazon": {
                "score": 0.50,
                "summary": "Management remained optimistic about AWS growth while noting retail cost efficiencies.",
                "highlight": "CFO pointed to improving operating income across all segments."
            },
            "Google": {
                "score": 0.60,
                "summary": "Leadership expressed confidence in AI-driven search innovation and ad revenue growth.",
                "highlight": "CEO emphasized commitment to responsible AI development."
            }
        }

        return sample_earnings.get(company_name, {
            "score": 0.25,
            "summary": f"{company_name} management provided steady but unremarkable guidance.",
            "highlight": f"Focus on operational efficiency and long-term strategic goals."
        })
