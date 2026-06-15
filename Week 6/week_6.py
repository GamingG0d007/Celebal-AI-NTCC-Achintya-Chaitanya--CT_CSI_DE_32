from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    when,
    upper,
    to_date,
    year,
    month,
    current_date,
    expr
)

spark = SparkSession.builder \
    .appName("Superstore_ETL_Pipeline") \
    .master("local[*]") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

df = spark.read \
    .option("header", "true") \
    .option("inferSchema", "false") \
    .option("quote", '"') \
    .option("escape", '"') \
    .option("multiLine", "true") \
    .csv("./Superstore.csv")

print("Number of Columns:", len(df.columns))

print("\nColumns:")
for c in df.columns:
    print(c)

print("\nSchema:")
df.printSchema()

print("\nSample Records:")
df.show(5, truncate=False)

df_selected = df.select(
    "Order ID",
    "Order Date",
    "Customer Name",
    "Segment",
    "Region",
    "Category",
    "Sub-Category",
    "Sales",
    "Quantity",
    "Profit"
)

df_selected = df_selected \
    .withColumnRenamed("Customer Name", "Customer_Name") \
    .withColumnRenamed("Sub-Category", "Sub_Category")

df_selected = df_selected.withColumn(
    "Order Date",
    to_date(col("Order Date"), "M/d/yyyy")
)

df_selected = df_selected \
    .withColumn("Sales", expr("try_cast(Sales as double)")) \
    .withColumn("Profit", expr("try_cast(Profit as double)")) \
    .withColumn("Quantity", expr("try_cast(Quantity as int)"))

df_selected = df_selected.filter(
    col("Sales").isNotNull()
)

df_selected = df_selected.withColumn(
    "Order_Year",
    year(col("Order Date"))
)

df_selected = df_selected.withColumn(
    "Order_Month",
    month(col("Order Date"))
)

df_selected = df_selected.withColumn(
    "Profit_Status",
    when(col("Profit") > 0, "Profit")
    .otherwise("Loss")
)

df_selected = df_selected.withColumn(
    "Processing_Date",
    current_date()
)

df_selected = df_selected.withColumn(
    "Customer_Name",
    upper(col("Customer_Name"))
)

df_clean = df_selected.na.fill({
    "Segment": "Unknown",
    "Region": "Unknown"
})

df_filtered = df_clean.filter(
    col("Sales") > 500
)

print("\nFILTERED DATA")
df_filtered.show(10, truncate=False)

print("\nTotal Records After Filter:")
print(df_filtered.count())

region_sales = df_filtered.groupBy(
    "Region"
).sum(
    "Sales"
).withColumnRenamed(
    "sum(Sales)",
    "Total_Sales"
)

print("\nREGION WISE SALES")
region_sales.show()

category_profit = df_filtered.groupBy(
    "Category"
).sum(
    "Profit"
).withColumnRenamed(
    "sum(Profit)",
    "Total_Profit"
)

print("\nCATEGORY PROFIT")
category_profit.show()

print("\nEXECUTION PLAN")
df_filtered.explain(True)

try:
    df_filtered.write \
        .mode("overwrite") \
        .option("header", "true") \
        .csv("./output/superstore_csv")

    df_filtered.write \
        .mode("overwrite") \
        .parquet("./output/superstore_parquet")

    print("\nFiles saved successfully.")

except Exception as e:
    print("\nWrite operation skipped.")
    print("Reason:")
    print(e)

spark.stop()