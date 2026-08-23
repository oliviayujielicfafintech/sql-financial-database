import sqlite3
import pandas as pd

# 1. 创建内存 SQL 数据库连接 / Create SQLite Database
conn = sqlite3.connect("financial_research.db")
cursor = conn.cursor()

# 2. 建立财报数据库表 (Income Statement Table)
cursor.execute("DROP TABLE IF EXISTS financial_metrics")
cursor.execute("""
CREATE TABLE financial_metrics (
    ticker TEXT PRIMARY KEY,
    company_name TEXT,
    sector TEXT,
    revenue_m REAL,          -- 营业收入 (百万美元)
    net_income_m REAL,       -- 净利润 (百万美元)
    rd_expenses_m REAL,      -- 研发支出 (百万美元)
    revenue_growth_yoY REAL  -- 营收同比增速 (%)
)
""")

# 3. 写入真实及对比标的数据 (AAOI, NVDA, LUMN, COHR, CIEN)
financial_data = [
    ('AAOI', 'Applied Optoelectronics', 'Technology', 215.5, 12.4, 38.2, 18.5),
    ('NVDA', 'NVIDIA Corporation', 'Technology', 60922.0, 29760.0, 8680.0, 125.9),
    ('LUMN', 'Lumen Technologies', 'Telecommunications', 14520.0, -10300.0, 120.0, -12.4),
    ('COHR', 'Coherent Corp', 'Technology', 4710.0, -182.0, 395.0, 6.2),
    ('CIEN', 'Ciena Corporation', 'Technology', 4380.0, 255.0, 520.0, 13.8)
]

cursor.executemany("""
INSERT INTO financial_metrics VALUES (?, ?, ?, ?, ?, ?, ?)
""", financial_data)
conn.commit()

# 4. 执行买方投研 SQL 筛选：计算 Margin，并筛选“高增长且盈利”的标的
sql_query = """
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
"""

# 5. 用 Pandas 读取并展示 SQL 查询结果
df_sql = pd.read_sql_query(sql_query, conn)
conn.close()

print("==================================================")
print("=== SQL Equity Screening: High Growth & Profitable ===")
print("==================================================")
print(df_sql.to_string(index=False))
