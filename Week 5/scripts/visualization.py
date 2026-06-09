import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pyspark.sql import SparkSession
import numpy as np

def generate_visualizations(input_path: str, output_dir: str)-> None:
    # Configure plotting environment
    plt.style.use('dark_background')
    plt.rcParams['figure.facecolor'] = '#121212'
    plt.rcParams['axes.facecolor'] = '#1e1e1e'
    plt.rcParams['axes.edgecolor'] = '#444444'
    plt.rcParams['grid.color'] = '#333333'
    plt.rcParams['font.family'] = 'monospace'

    spark = SparkSession.builder.appName("Visualization").getOrCreate()

    try:
        # Load analytical results
        sales_summary = spark.read.parquet(f"{input_path}/sales_summary")
        profitability = spark.read.parquet(f"{input_path}/profitability")
        geo_stats = spark.read.parquet(f"{input_path}/geographic_stats")
        product_stats = spark.read.parquet(f"{input_path}/product_stats")

        # Convert to pandas for visualization
        sales_pd = sales_summary.toPandas()
        profit_pd = profitability.toPandas()
        geo_pd = geo_stats.toPandas()
        product_pd = product_stats.limit(50).toPandas()

        # 1. Quarterly Sales Trends
        seasonality = (profit_pd.assign(
            Quarter=lambda x: pd.to_datetime(x['Order Date']).dt.quarter
        )
        .pivot_table(index='Quarter', values='Regional_Revenue', aggfunc='sum')
        .reindex([1, 2, 3, 4]))

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=seasonality, x=seasonality.index, y='Regional_Revenue',
                    palette='viridis', ax=ax, hue=seasonality.index, legend=False)
        ax.set_title('Quarterly Revenue Distribution', fontsize=14, pad=15)
        ax.set_xlabel('Quarter', fontsize=12)
        ax.set_ylabel('Revenue ($)', fontsize=12)
        ax.set_xticklabels(['Q1', 'Q2', 'Q3', 'Q4'])
        plt.savefig(f"{output_dir}/quarterly_trends.png", dpi=400, bbox_inches='tight')
        plt.close()

        # 2. Regional Profitability Heatmap
        region_pivot = profit_pd.pivot_table(index='Region', columns='Segment',
                                           values='Avg_Profit_per_Order', aggfunc='mean')
        plt.figure(figsize=(10, 8))
        sns.heatmap(region_pivot, annot=True, fmt='.2f', cmap='RdYlGn',
                    linewidths=0.5, linecolor='#444444')
        plt.title('Regional Profitability by Segment', fontsize=14, pad=15)
        plt.tight_layout()
        plt.savefig(f"{output_dir}/profitability_heatmap.png", dpi=400, bbox_inches='tight')
        plt.close()

        # 3. Top Products Performance
        top_products = product_pd.nlargest(10, 'Total_Sales')
        fig, ax = plt.subplots(figsize=(12, 6))
        bars = ax.barh(top_products['Product Name'], top_products['Total_Sales'],
                       color=plt.cm.plasma(np.linspace(0.1, 0.9, len(top_products))))
        ax.set_xlabel('Total Sales ($)', fontsize=12)
        ax.set_title('Top 10 Products by Revenue', fontsize=14, pad=15)
        ax.set_yticklabels(top_products['Product Name'], fontsize=9)
        plt.tight_layout()
        plt.savefig(f"{output_dir}/top_products.png", dpi=400, bbox_inches='tight')
        plt.close()

        # 4. Geographic Performance Scatter
        fig, ax = plt.subplots(figsize=(12, 8))
        scatter = ax.scatter(geo_pd['Total_Sales'], geo_pd['Avg_Profit'],
                            c=geo_pd['Transactions'], cmap='viridis',
                            s=geo_pd['Transactions']*2, alpha=0.7, edgecolors='white', linewidth=0.5)
        plt.colorbar(scatter, label='Transaction Volume')
        ax.set_xlabel('Total Sales ($)', fontsize=12)
        ax.set_ylabel('Average Profit ($)', fontsize=12)
        ax.set_title('Geographic Performance Analysis', fontsize=14, pad=15)
        plt.tight_layout()
        plt.savefig(f"{output_dir}/geographic_performance.png", dpi=400, bbox_inches='tight')
        plt.close()

        # 5. Sales vs Profit Distribution
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.scatter(product_pd['Total_Sales'], product_pd['Avg_Unit_Profit'],
                  alpha=0.6, c=product_pd['Units_Sold'], cmap='plasma', s=50)
        ax.set_xlabel('Total Sales ($)', fontsize=12)
        ax.set_ylabel('Average Profit ($)', fontsize=12)
        ax.set_title('Sales vs Profit Distribution', fontsize=14, pad=15)
        plt.colorbar(ax.collections[0], label='Units Sold')
        plt.savefig(f"{output_dir}/sales_profit_distribution.png", dpi=400, bbox_inches='tight')
        plt.close()

    except Exception as e:
        spark.stop()
        raise RuntimeError(f"Visualization failed: {str(e)}")

    finally:
        spark.stop()
        print("Visualizations generated successfully!")

if __name__ == "__main__":
    import sys
    generate_visualizations(sys.argv[1] if len(sys.argv) > 1 else "results",
                           sys.argv[2] if len(sys.argv) > 2 else "visualizations")