"""
InvestmentDecisionAgent
========================
This agent is the final step in the Equity Nexus workflow.
It receives the SentimentReport and FinancialReport from the
previous two agents, combines the information, and produces
a single investment recommendation.

The decision process:
    1. Calculate a composite score (weighted average of sentiment and fundamentals).
    2. Map the score to a BUY, HOLD, or SELL recommendation.
    3. Compute a confidence level based on agreement between the two analyses.
    4. Generate a short investment thesis explaining the reasoning.
    5. Identify key risk factors.
"""

from dataclasses import dataclass
from typing import List

from agents.market_sentiment import SentimentReport
from agents.fundamental_analysis import FinancialReport


@dataclass
class InvestmentDecision:
    """
    Data structure that holds the final investment decision.

    Attributes:
        company (str): The company name.
        ticker (str): The stock ticker symbol.
        recommendation (str): BUY, HOLD, or SELL.
        confidence_level (float): Confidence in the recommendation, 0.0 to 1.0.
        investment_thesis (str): A short narrative explaining the recommendation.
        risk_factors (list): Key risks identified during analysis.
        sentiment_score (float): The raw sentiment score from Agent 1.
        financial_health (str): The health label from Agent 2.
    """
    company: str
    ticker: str
    recommendation: str
    confidence_level: float
    investment_thesis: str
    risk_factors: List[str]
    sentiment_score: float
    financial_health: str


class InvestmentDecisionAgent:
    """
    Agent that combines sentiment and fundamental analysis
    to produce a final investment recommendation.

    This is the "brain" of the workflow -- it weighs both inputs
    and produces an actionable output for the user.
    """

    def __init__(self):
        self.agent_name = "InvestmentDecisionAgent"

    def analyze(
        self,
        sentiment_report: SentimentReport,
        financial_report: FinancialReport
    ) -> InvestmentDecision:
        """
        Generate the final investment decision.

        Steps:
            1. Calculate a composite score from both reports.
            2. Map the score to a BUY / HOLD / SELL recommendation.
            3. Calculate confidence based on agreement between analyses.
            4. Generate an investment thesis.
            5. Identify risk factors.
            6. Return a structured InvestmentDecision.

        Args:
            sentiment_report (SentimentReport): Output from MarketSentimentAgent.
            financial_report (FinancialReport): Output from FundamentalAnalysisAgent.

        Returns:
            InvestmentDecision: The final recommendation.
        """
        company = sentiment_report.company
        ticker = sentiment_report.ticker

        print(f"  [{self.agent_name}] Generating investment decision for {company} ({ticker})...")

        # Step 1: Compute composite score
        composite = self._calculate_composite_score(sentiment_report, financial_report)

        # Step 2: Determine recommendation
        recommendation = self._determine_recommendation(composite)

        # Step 3: Calculate confidence
        confidence = self._calculate_confidence(sentiment_report, financial_report)

        # Step 4: Generate thesis
        thesis = self._generate_thesis(sentiment_report, financial_report, recommendation)

        # Step 5: Identify risks
        risks = self._identify_risks(sentiment_report, financial_report)

        # Step 6: Build the decision object
        decision = InvestmentDecision(
            company=company,
            ticker=ticker,
            recommendation=recommendation,
            confidence_level=round(confidence, 2),
            investment_thesis=thesis,
            risk_factors=risks,
            sentiment_score=sentiment_report.sentiment_score,
            financial_health=financial_report.financial_health
        )

        print(f"  [{self.agent_name}] Decision complete.")
        return decision

    # ------------------------------------------------------------------
    # Scoring Logic
    # ------------------------------------------------------------------

    def _calculate_composite_score(
        self,
        sentiment: SentimentReport,
        financial: FinancialReport
    ) -> float:
        """
        Combine sentiment and fundamental scores into one composite score.

        Weighting:
            - 40% from sentiment analysis
            - 60% from fundamental analysis

        The sentiment score is first normalized from [-1, 1] to [0, 1].

        Args:
            sentiment (SentimentReport): The sentiment analysis output.
            financial (FinancialReport): The fundamental analysis output.

        Returns:
            float: A composite score between 0.0 and 1.0.
        """
        # Normalize sentiment from [-1, 1] to [0, 1]
        normalized_sentiment = (sentiment.sentiment_score + 1) / 2

        # Calculate a fundamental score from raw metrics
        fundamental_score = self._calculate_fundamental_score(financial)

        # Weighted combination
        return (0.4 * normalized_sentiment) + (0.6 * fundamental_score)

    def _calculate_fundamental_score(self, financial: FinancialReport) -> float:
        """
        Convert raw financial metrics into a single score (0.0 to 1.0).

        Each metric contributes positively or negatively to the score:
            - High revenue growth -> positive
            - Low P/E ratio -> positive
            - Low debt-to-equity -> positive
            - High profit margin -> positive

        Args:
            financial (FinancialReport): The fundamental analysis output.

        Returns:
            float: A score between 0.0 and 1.0.
        """
        score = 0.5  # Start at neutral

        # Revenue growth contribution
        if financial.revenue_growth > 20:
            score += 0.20
        elif financial.revenue_growth > 10:
            score += 0.10
        elif financial.revenue_growth < 0:
            score -= 0.20

        # P/E ratio contribution (lower is generally better)
        if financial.pe_ratio < 15:
            score += 0.15
        elif financial.pe_ratio > 40:
            score -= 0.15

        # Debt-to-equity contribution
        if financial.debt_to_equity < 0.5:
            score += 0.10
        elif financial.debt_to_equity > 2.0:
            score -= 0.15

        # Profit margin contribution
        if financial.profit_margin > 20:
            score += 0.10
        elif financial.profit_margin < 5:
            score -= 0.10

        # Clamp to [0, 1]
        return max(0.0, min(1.0, score))

    # ------------------------------------------------------------------
    # Recommendation Logic
    # ------------------------------------------------------------------

    def _determine_recommendation(self, composite_score: float) -> str:
        """
        Map a composite score to a BUY, HOLD, or SELL recommendation.

        Thresholds:
            - >= 0.6 -> BUY
            - >= 0.4 -> HOLD
            - < 0.4  -> SELL

        Args:
            composite_score (float): The combined score from both analyses.

        Returns:
            str: One of 'BUY', 'HOLD', or 'SELL'.
        """
        if composite_score >= 0.6:
            return "BUY"
        elif composite_score >= 0.4:
            return "HOLD"
        else:
            return "SELL"

    def _calculate_confidence(
        self,
        sentiment: SentimentReport,
        financial: FinancialReport
    ) -> float:
        """
        Calculate confidence based on how well the two analyses agree.

        If both sentiment and fundamentals point in the same direction,
        confidence is high. If they diverge, confidence is lower.

        Args:
            sentiment (SentimentReport): The sentiment analysis output.
            financial (FinancialReport): The fundamental analysis output.

        Returns:
            float: A confidence level between 0.0 and 1.0.
        """
        sentiment_positive = sentiment.sentiment_score > 0.2
        fundamentals_strong = financial.financial_health in ["Strong", "Moderate"]

        if sentiment_positive and fundamentals_strong:
            return 0.85   # Both agree on positive outlook
        elif not sentiment_positive and not fundamentals_strong:
            return 0.80   # Both agree on cautious outlook
        else:
            return 0.55   # Mixed signals reduce confidence

    # ------------------------------------------------------------------
    # Thesis Generation
    # ------------------------------------------------------------------

    def _generate_thesis(
        self,
        sentiment: SentimentReport,
        financial: FinancialReport,
        recommendation: str
    ) -> str:
        """
        Generate a short investment thesis based on all available data.

        The thesis is a 3-4 sentence narrative that summarizes:
            - The overall outlook
            - The sentiment situation
            - The fundamental situation
            - The valuation context

        Args:
            sentiment (SentimentReport): The sentiment analysis output.
            financial (FinancialReport): The fundamental analysis output.
            recommendation (str): The final recommendation (BUY/HOLD/SELL).

        Returns:
            str: A narrative investment thesis.
        """
        parts = []

        # Opening statement based on recommendation
        if recommendation == "BUY":
            parts.append(f"{sentiment.company} presents a compelling investment opportunity.")
        elif recommendation == "HOLD":
            parts.append(f"{sentiment.company} is fairly valued at current levels.")
        else:
            parts.append(f"{sentiment.company} faces headwinds that warrant a cautious approach.")

        # Sentiment context
        parts.append(
            f"Market sentiment is {sentiment.overall_sentiment.lower()} "
            f"(score: {sentiment.sentiment_score})."
        )

        # Fundamental context
        parts.append(
            f"The company demonstrates {financial.financial_health.lower()} financial health "
            f"with {financial.revenue_growth}% revenue growth."
        )

        # Valuation context
        parts.append(
            f"A P/E ratio of {financial.pe_ratio} suggests the stock is "
            f"{financial.valuation.lower()}."
        )

        return " ".join(parts)

    # ------------------------------------------------------------------
    # Risk Identification
    # ------------------------------------------------------------------

    def _identify_risks(
        self,
        sentiment: SentimentReport,
        financial: FinancialReport
    ) -> List[str]:
        """
        Identify key risk factors based on the analysis results.

        Checks for:
            - Overvaluation
            - High leverage
            - Low profitability
            - Negative sentiment
            - Slow growth

        Args:
            sentiment (SentimentReport): The sentiment analysis output.
            financial (FinancialReport): The fundamental analysis output.

        Returns:
            list: A list of risk factor strings.
        """
        risks = []

        if financial.valuation == "Overvalued":
            risks.append("High P/E ratio suggests potential overvaluation.")

        if financial.debt_to_equity > 1.5:
            risks.append("High debt-to-equity ratio increases financial risk.")

        if financial.profit_margin < 10:
            risks.append("Low profit margin may indicate operational challenges.")

        if sentiment.sentiment_score < 0:
            risks.append("Negative market sentiment could pressure the stock price.")

        if financial.revenue_growth < 5:
            risks.append("Slowing revenue growth may impact future valuations.")

        return risks if risks else ["No significant risk factors identified."]
