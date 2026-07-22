"""
FundamentalAnalysisAgent
=========================
This agent simulates the analysis of key financial metrics for a given company.
In a production environment, it would fetch data from APIs such as:
    - Yahoo Finance
    - Alpha Vantage
    - SEC EDGAR filings
    - Bloomberg Terminal

For this prototype, it returns pre-built sample data to demonstrate the workflow.

Key metrics analyzed:
    - Revenue Growth Rate (%)
    - Price-to-Earnings (P/E) Ratio
    - Debt-to-Equity Ratio
    - Profit Margin (%)
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class FinancialReport:
    """
    Data structure that holds the output of the fundamental analysis.

    Attributes:
        company (str): The company name.
        ticker (str): The stock ticker symbol.
        revenue_growth (float): Year-over-year revenue growth as a percentage.
        pe_ratio (float): Price-to-Earnings ratio.
        debt_to_equity (float): Total debt divided by total equity.
        profit_margin (float): Net income as a percentage of revenue.
        valuation (str): Estimated valuation - Undervalued, Fairly Valued, or Overvalued.
        financial_health (str): Overall health assessment - Strong, Moderate, or Weak.
        metrics (dict): Raw metrics dictionary for downstream processing.
    """
    company: str
    ticker: str
    revenue_growth: float
    pe_ratio: float
    debt_to_equity: float
    profit_margin: float
    valuation: str
    financial_health: str
    metrics: Dict[str, float]


class FundamentalAnalysisAgent:
    """
    Agent that analyzes fundamental financial metrics for a company.

    This agent retrieves key financial data and evaluates the company's
    valuation and financial health based on standard industry heuristics.
    """

    def __init__(self):
        self.agent_name = "FundamentalAnalysisAgent"

    def analyze(self, company_name: str, ticker: str) -> FinancialReport:
        """
        Run fundamental analysis on the given company.

        Steps:
            1. Fetch financial metrics (revenue growth, P/E, D/E, margin).
            2. Assess valuation based on the P/E ratio.
            3. Assess financial health based on debt levels and margins.
            4. Return a structured FinancialReport.

        Args:
            company_name (str): The name of the company.
            ticker (str): The stock ticker symbol.

        Returns:
            FinancialReport: A structured report with financial findings.
        """
        print(f"  [{self.agent_name}] Analyzing financials for {company_name} ({ticker})...")

        # Step 1: Fetch the key financial metrics
        metrics = self._fetch_financial_metrics(company_name)

        # Step 2: Determine valuation category
        valuation = self._assess_valuation(metrics["pe_ratio"])

        # Step 3: Determine financial health category
        health = self._assess_financial_health(
            metrics["debt_to_equity"],
            metrics["profit_margin"]
        )

        # Step 4: Build and return the report
        report = FinancialReport(
            company=company_name,
            ticker=ticker,
            revenue_growth=metrics["revenue_growth"],
            pe_ratio=metrics["pe_ratio"],
            debt_to_equity=metrics["debt_to_equity"],
            profit_margin=metrics["profit_margin"],
            valuation=valuation,
            financial_health=health,
            metrics=metrics
        )

        print(f"  [{self.agent_name}] Fundamental analysis complete.")
        return report

    def _fetch_financial_metrics(self, company_name: str) -> Dict[str, float]:
        """
        Retrieve financial metrics for the given company.

        In production, this would call real financial data APIs.
        For this prototype, it returns hardcoded sample data.

        Args:
            company_name (str): The company to look up.

        Returns:
            dict: A dictionary containing revenue_growth, pe_ratio,
                  debt_to_equity, and profit_margin.
        """
        sample_data = {
            "Tesla": {
                "revenue_growth": 25.0,
                "pe_ratio": 65.0,
                "debt_to_equity": 0.15,
                "profit_margin": 15.0
            },
            "Apple": {
                "revenue_growth": 8.0,
                "pe_ratio": 28.0,
                "debt_to_equity": 1.8,
                "profit_margin": 25.0
            },
            "Microsoft": {
                "revenue_growth": 18.0,
                "pe_ratio": 35.0,
                "debt_to_equity": 0.45,
                "profit_margin": 35.0
            },
            "Amazon": {
                "revenue_growth": 12.0,
                "pe_ratio": 55.0,
                "debt_to_equity": 0.70,
                "profit_margin": 7.0
            },
            "Google": {
                "revenue_growth": 15.0,
                "pe_ratio": 25.0,
                "debt_to_equity": 0.10,
                "profit_margin": 22.0
            }
        }

        return sample_data.get(company_name, {
            "revenue_growth": 10.0,
            "pe_ratio": 20.0,
            "debt_to_equity": 0.50,
            "profit_margin": 12.0
        })

    def _assess_valuation(self, pe_ratio: float) -> str:
        """
        Assess whether a stock appears undervalued, fairly valued,
        or overvalued based on its P/E ratio.

        Heuristic:
            - P/E < 15  -> Undervalued
            - P/E 15-25 -> Fairly Valued
            - P/E > 25  -> Overvalued

        Args:
            pe_ratio (float): The current P/E ratio.

        Returns:
            str: Valuation label.
        """
        if pe_ratio < 15:
            return "Undervalued"
        elif pe_ratio <= 25:
            return "Fairly Valued"
        else:
            return "Overvalued"

    def _assess_financial_health(self, debt_to_equity: float, profit_margin: float) -> str:
        """
        Assess overall financial health using leverage and profitability.

        Heuristic:
            - Low debt (< 0.5) AND high margin (> 15%) -> Strong
            - Moderate debt (< 1.5) AND decent margin (> 8%) -> Moderate
            - Otherwise -> Weak

        Args:
            debt_to_equity (float): The company's debt-to-equity ratio.
            profit_margin (float): The company's net profit margin (%).

        Returns:
            str: Health label.
        """
        if debt_to_equity < 0.5 and profit_margin > 15:
            return "Strong"
        elif debt_to_equity < 1.5 and profit_margin > 8:
            return "Moderate"
        else:
            return "Weak"
