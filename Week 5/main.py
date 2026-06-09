import pyspark.sql.functions as F
from pyspark.sql import SparkSession
from pyspark.sql.types import *

# Define required schemas for DataFrame validation
# NOTE: "Order Date" and "Ship Date" are updated to StringType here. If read as DateType,
# any dates matching non-standard formats (like yyyy/MM/dd) would silently convert to 
# Null during the initial read before your normalization code could parse them.
order_schema = StructType([
    StructField("Order ID", StringType(), True),
    StructField("Order Date", StringType(), True),
    StructField("Ship Date", StringType(), True),
    StructField("Customer Name", StringType(), True),
    StructField("Segment", StringType(), True),
    StructField("Country", StringType(), True),
    StructField("State", StringType(), True),
    StructField("City", StringType(), True),
    StructField("Postal Code", StringType(), True),
    StructField("Region", StringType(), True),
    StructField("Product ID", StringType(), True),
    StructField("Product Name", StringType(), True),
    StructField("Category", StringType(), True),
    StructField("Sub-Category", StringType(), True),
    StructField("Quantity", IntegerType(), True),
    StructField("Discount", FloatType(), True),
    StructField("Profit", FloatType(), True),
    StructField("Sales", FloatType(), True)
])

def clean_superstore_data(input_path: str, output_path: str) -> None:
    # Initialize Spark session with optimized configurations
    spark = SparkSession.builder \
        .appName("Superstore_Cleaning") \
        .config("spark.sql.shuffle.partitions", 200) \
        .config("spark.executor.memory", "8g") \
        .config("spark.sql.legacy.allowUntypedNulls", "true") \
        .getOrCreate()

    try:
        # 1. FIXED: 'sep' expects a string format (","), not a set ({","})
        df = spark.read.csv(input_path,
                            sep=",",
                            header=True,
                            schema=order_schema,
                            inferSchema=False)

        # 2. FIXED: Corrected parenthesis nesting errors inside F.coalesce
        df = df.withColumn("Order Date", F.coalesce(
            F.to_date(F.col("Order Date"), "yyyy-MM-dd"),
            F.to_date(F.col("Order Date"), "yyyy/MM/dd")
        )).withColumn("Ship Date", F.coalesce(
            F.to_date(F.col("Ship Date"), "yyyy-MM-dd"),
            F.to_date(F.col("Ship Date"), "yyyy/MM/dd")
        ))

        # 3. FIXED (PERFORMANCE): Replaced the loop that executed .count() on every column 
        # (which triggered dozens of slow table scans) with a single-pass aggregation query.
        total_count = df.count()
        if total_count == 0:
            print("Dataset is empty. Exiting cleaning job.")
            return

        null_counts_expr = [F.sum(F.col(c).isNull().cast("int")).alias(c) for c in df.columns]
        null_stats = df.select(null_counts_expr).collect()[0].asDict()
        print(f"\nNull value distribution:\n{null_stats}")

        # 4. Drop columns with >70% nulls while preserving order
        high_null_cols = [col for col, val in null_stats.items() if val > 0.7 * total_count]
        if high_null_cols:
            print(f"Dropping high-null columns: {high_null_cols}")
            df = df.drop(*high_null_cols)

        # 5. FIXED: Added the missing comparison operator (< 0) for the 'Quantity' validation logic
        df = (df.withColumn("Discount", F.when(F.col("Discount") > 1, 1.0)
                                        .otherwise(F.col("Discount")))
                .withColumn("Quantity", F.when(F.col("Quantity") < 0, 0)
                                        .otherwise(F.col("Quantity")))
                .withColumn("Sales", F.col("Quantity") * (F.col("Profit") + F.col("Discount"))))

        # 6. FIXED: .fillna() can only accept literal constant mappings. Passing a lambda 
        # function throws a runtime error. Dynamic columns must use F.when().otherwise() instead.
        if "Profit" in df.columns:
            df = df.withColumn("Profit", F.when(F.col("Profit").isNull(), F.col("Sales") * 0.5)
                                          .otherwise(F.col("Profit")))

        # Define literal fallback mappings for static values
        fill_literals = {
            "Discount": 0.1,
            "Postal Code": "XYZ123",
            "Segment": "Online"
        }
        # Apply safely to columns that weren't dropped in Step 4
        fill_literals = {k: v for k, v in fill_literals.items() if k in df.columns}
        df = df.fillna(fill_literals)

        # 7. FIXED: Replaced broken Python UDF array initializers with high-performance, 
        # native Spark functions to prevent execution-phase JVM-to-Python memory serialization bottlenecks.
        df = df.withColumn("ValidationErrors", F.array().cast(ArrayType(StringType()))) \
               .withColumn("MemoryErrors", F.array().cast(ArrayType(StringType())))

        # 8. FIXED: Moved .coalesce(1) BEFORE .write. .write.parquet() executes immediately and 
        # returns None, meaning appending .coalesce(1) to the end threw an AttributeError.
        # Fixed formatting options and removed invalid keyword argument 'escapeUnsafe'.
        (df.coalesce(1).write
            .mode("overwrite")
            .option("compression", "zstd")
            .partitionBy("Region", "Segment")
            .parquet(output_path))

    except Exception as e:
        raise RuntimeError(f"Cleaning failed: {str(e)}")
        
    finally:
        spark.stop()
        print("Data cleaning completed successfully!")
