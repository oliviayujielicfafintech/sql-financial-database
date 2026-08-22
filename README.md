# 📊 Institutional SQL Financial Database & Equity Screening Engine

> An end-to-end SQLite financial database pipeline designed for automated ingestion, ratio calculation, and multi-factor equity screening across public tech companies.

---

## 🎯 Executive Summary

In institutional quantitative research and fundamental equity analysis, maintaining a structured database of company filings (10-K / 10-Q) is foundational. This project demonstrates an automated relational database workflow using Python and **SQLite**. 

The pipeline ingests raw income statement data (Revenue, Net Income, R&D Expenses, YoY Growth), executes custom SQL query logic to engineer profitability and reinvestment metrics, and filters high-growth, profitable equity targets dynamically.

---

## 🛠️ Tech Stack & Architecture

* **Database Engine:** SQLite3
* **Language & Analysis:** Python, Pandas
* **SQL Techniques Implemented:** Dynamic Schema Creation, Aggregations, Conditional Filtering (`WHERE`), Computed Columns (`ROUND`, Arithmetic Calculations), Sorting (`ORDER BY`).

---

## 🧮 Computed Financial Metrics (SQL Level)

Instead of relying on downstream manual calculations, financial ratios are computed directly within the relational database query engine:

1. **Net Profit Margin (%)**:
   $$\text{Net Profit Margin} = \left( \frac{\text{Net Income}}{\text{Revenue}} \right) \times 100$$
2. **R and D Intensity Ratio (%)**:
   $$\text{RD Ratio} = \left( \frac{\text{RD Expenses}}{\text{Revenue}} \right) \times 100$$

---

## 🔍 Institutional Screening Criteria

The SQL engine applies a strict quantitative filter to isolate high-quality growth equities:
* **Revenue YoY Growth Threshold:** $> +10.0\%$
* **Profitability Gate:** $\text{Net Income} > 0$ 

```sql
SELECT 
    ticker,
    company_name,
    revenue_m AS Revenue_M,
    revenue_growth_yoY AS YoY_Growth_Pct,
    ROUND((net_income_m / revenue_m) * 100, 2) AS Net_Profit_Margin_Pct,
    ROUND((rd_expenses_m / revenue_m) * 100, 2) AS RD_Ratio_Pct
FROM financial_metrics
WHERE revenue_growth_yoY > 10.0 
  AND net_income_m > 0
ORDER BY revenue_growth_yoY DESC;
