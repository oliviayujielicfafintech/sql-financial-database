import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# 1. 整合 SQL 财报数据与 FinBERT 情绪数据
data = {
    'Ticker': ['NVDA', 'AAOI', 'CIEN', 'COHR', 'LUMN'],
    'Company': ['NVIDIA', 'Applied Optoelectronics', 'Ciena', 'Coherent', 'Lumen'],
    'Revenue_M': [60922.0, 215.5, 4380.0, 4710.0, 14520.0],
    'YoY_Growth_Pct': [125.9, 18.5, 13.8, 6.2, -12.4],
    'Net_Margin_Pct': [48.85, 5.75, 5.82, -3.86, -70.94],
    'Sentiment_Index': [85.5, 23.43, 12.0, -5.2, -45.0]
}

df_dashboard = pd.DataFrame(data)

# 2. 创建 Plotly 交互式散点图 (白底主题)
fig = px.scatter(
    df_dashboard,
    x='YoY_Growth_Pct',
    y='Net_Margin_Pct',
    size='Revenue_M',
    color='Sentiment_Index',
    hover_name='Company',
    text='Ticker',
    labels={
        'YoY_Growth_Pct': 'Revenue YoY Growth (%)',
        'Net_Margin_Pct': 'Net Profit Margin (%)',
        'Sentiment_Index': 'FinBERT Sentiment Score'
    },
    title='<b>Institutional Equity Analytics Dashboard</b><br><sup>Financial Performance vs. Sentiment Score</sup>',
    color_continuous_scale='RdYlGn',
    size_max=50
)

fig.update_traces(textposition='top center')

# 修改为 plotly_white 模板，并显式指定背景颜色
fig.update_layout(
    template='plotly_white',
    paper_bgcolor='white',
    plot_bgcolor='white',
    height=500
)

# 显示交互看板
fig.show()

# 重新保存白底 HTML 文件
fig.write_html("interactive_financial_dashboard.html")
print("[SUCCESS] White-theme dashboard saved successfully!")
