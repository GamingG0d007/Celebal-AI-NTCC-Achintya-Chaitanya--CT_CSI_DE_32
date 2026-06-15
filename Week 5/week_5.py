from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    count,
    sum,
    avg,
    min,
    max,
    trim,
    when
)

spark = SparkSession.builder \
    .appName("Superstore_Data_Cleaning_Aggregation") \
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

print("Original Record Count:")
print(df.count())

print("\nOriginal Schema:")
df.printSchema()

df = df.dropDuplicates()

print("\nRecord Count After Removing Duplicates:")
print(df.count())

df = df.replace("", None)

df = df.na.fill({
    "Region": "Unknown",
    "Category": "Unknown",
    "Segment": "Unknown"
})

df = df.withColumn(
    "Sales",
    col("Sales").cast("double")
)

df = df.withColumn(
    "Profit",
    col("Profit").cast("double")
)

df = df.withColumn(
    "Quantity",
    col("Quantity").cast("int")
)

df = df.withColumnRenamed(
    "Sub-Category",
    "Sub_Category"
)

print("\nCleaned Schema:")
df.printSchema()

filtered_df = df.filter(
    (col("Sales") > 100) &
    (col("Profit") > 0)
)

print("\nFiltered Records:")
filtered_df.show(10, truncate=False)

print("\nCategory Aggregation")

category_stats = filtered_df.groupBy("Category").agg(
    count("*").alias("Total_Orders"),
    sum("Sales").alias("Total_Sales"),
    avg("Sales").alias("Average_Sales"),
    min("Sales").alias("Minimum_Sales"),
    max("Sales").alias("Maximum_Sales")
)

category_stats.show(truncate=False)

print("\nRegion Aggregation")

region_stats = filtered_df.groupBy("Region").agg(
    count("*").alias("Orders"),
    sum("Profit").alias("Total_Profit")
)

region_stats.show()

print("\nCategories with Sales > 100000")

high_sales_categories = category_stats.filter(
    col("Total_Sales") > 100000
)

high_sales_categories.show()

print("\nTop Regions by Profit")

region_stats.orderBy(
    col("Total_Profit").desc()
).show()

print("\nExecution Plan")
filtered_df.explain(True)

spark.stop()