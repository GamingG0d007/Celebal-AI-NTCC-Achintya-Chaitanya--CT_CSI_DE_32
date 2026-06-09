import pyspark.sql.functions as F
from pyspark.sql.window import Window
from pyspark.sql.types import *

def perform_data_analysis(input_path: str, output_path: str)-> None:
    # Configure Spark session with memory optimization
    spark = SparkSession.builder
        .appName("Superstore_Analysis")
        .config("spark.sql.adaptive.enabled", "true")
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true")
        .config("spark.sql.shuffle.partitions", 150)
        .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
        .getOrCreate()

    try:
        # Load cleaned data
        df = spark.read.parquet(input_path)

        # Cache frequently accessed DataFrame
        df.cache()

        # Define window specifications for analysis
        regional_window = Window.partitionBy("Region").orderBy("Order Date")
        product_window = Window.partitionBy("Category", "Sub-Category")
        time_window = Window.partitionBy(F.year("Order Date"), F.month("Order Date"))

        # 1. Temporal Analysis with Window Functions
        temporal_analysis = (df.withColumn("Order_Sequence",
                          F.row_number().over(regional_window))
                           .withColumn("Sales_Rank",
                          F.rank().over(Window.partitionBy("Region").orderBy(F.desc("Sales"))))
                           .withColumn("Trend_Sales",
                          F.avg("Sales").over(time_window)))

        # 2. Multi-dimensional Aggregations
        sales_summary = df.agg(
            F.count("*").alias("Total_Orders"),
            F.sum("Sales").alias("Total_Revenue"),
            F.avg("Sales").alias("Avg_Order_Value"),
            F.mean("Profit").alias("Avg_Profit"),
            F.stddev("Sales").alias("Sales_Volatility"),
            F.min("Order Date").alias("First_Order"),
            F.max("Order Date").alias("Last_Order")
        )

        # 3. Profitability by Dimensions
        profitability = df.groupBy("Region", "Segment").agg(
            F.count("*").alias("Order_Count"),
            F.sum("Profit").alias("Total_Profit"),
            F.avg("Profit").alias("Avg_Profit_per_Order"),
            F.variance("Profit").alias("Profit_Variance"),
            F.sum("Sales").alias("Regional_Revenue")
        ).withColumn("Profit_Margin",
                (F.col("Total_Profit") / F.col("Regional_Revenue")) * 100)

        # 4. Product Analysis
        product_stats = (df.groupBy("Product Name", "Category", "Sub-Category")
                        .agg(
                            F.sum("Quantity").alias("Units_Sold"),
                            F.sum("Sales").alias("Total_Sales"),
                            F.avg("Profit").alias("Avg_Unit_Profit"),
                            F.min("Discount").alias("Min_Discount"),
                            F.max("Discount").alias("Max_Discount"),
                            F.countDistinct("Customer Name").alias("Unique_Customers")
                        )
                        .orderBy(F.desc("Total_Sales")))

        # 5. Geographic Performance
        geo_stats = (df.groupBy("State", "Region", "City")
                    .agg(
                        F.count("*").alias("Transactions"),
                        F.sum("Sales").alias("Total_Sales"),
                        F.avg("Profit").alias("Avg_Profit"),
                        F.countDistinct("Product ID").alias("Products_Sold")
                    )
                    .withColumn("Performance_Rating",
                        F.when(F.col("Avg_Profit") > F.lit(50), "High")
                        .when(F.col("Avg_Profit") > F.lit(20), "Medium")
                        .otherwise("Low")))

        # 6. Segment Analysis
        segment_analysis = (df.groupBy("Segment")
                           .agg(
                               F.count("*").alias("Orders"),
                               F.sum("Sales").alias("Revenue"),
                               F.avg("Discount").alias("Avg_Discount"),
                               F.skewness("Profit").alias("Profit_Skew")
                           )
                           .withColumn("Segment_Value",
                               F.col("Revenue") / F.sum("Revenue").over(Window.partitionBy())))

        # Write results to parquet with partitioning
        (sales_summary.write.mode("overwrite").parquet(f"{output_path}/sales_summary"))
        (profitability.write.mode("overwrite").partitionBy("Region").parquet(f"{output_path}/profitability"))
        (product_stats.write.mode("overwrite").partitionBy("Category").parquet(f"{output_path}/product_stats"))
        (geo_stats.write.mode("overwrite").parquet(f"{output_path}/geographic_stats"))
        (segment_analysis.write.mode("overwrite").parquet(f"{output_path}/segment_analysis"))

        # Print insights
        print("\n=== DATA INSIGHTS ===")
        print(f"Total Records Processed: {sales_summary.first()['Total_Orders']}")
        print(f"Average Order Value: ${sales_summary.first()['Avg_Order_Value']:.2f}")
        print(f"Total Revenue Generated: ${sales_summary.first()['Total_Revenue']:.2f}")
        print(f"Profit Margin: {(sales_summary.first()['Avg_Profit'] / sales_summary.first()['Avg_Order_Value']) * 100:.2f}%")

        # Show top segments
        print("\n=== TOP SEGMENTS ===")
        segment_analysis.orderBy(F.desc("Revenue")).show(5, truncate=False)

    except Exception as e:
        spark.stop()
        raise RuntimeError(f"Analysis failed: {str(e)}")

    finally:
        spark.stop()
        print("Data analysis completed successfully!")

if __name__ == "__main__":
    import sys
    input_path = sys.argv[1] if len(sys.argv) > 1 else "data/cleaned"
    output_path = sys.argv[2] if len(sys.argv) > 2 else "results"
    perform_data_analysis(input_path, output_path)