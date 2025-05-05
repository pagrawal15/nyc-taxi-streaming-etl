from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp, from_json
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DoubleType

# Step 1: Create Spark Session
spark = SparkSession.builder \
    .appName("TaxiTripStreamingETL") \
    .getOrCreate()

# Step 2: Define the JSON schema for parsing
schema = StructType([
    StructField("trip_id", IntegerType(), True),
    StructField("pickup_datetime", StringType(), True),
    StructField("dropoff_datetime", StringType(), True),
    StructField("pickup_lat", DoubleType(), True),
    StructField("pickup_lon", DoubleType(), True),
    StructField("dropoff_lat", DoubleType(), True),
    StructField("dropoff_lon", DoubleType(), True),
    StructField("fare_amount", DoubleType(), True),
    StructField("passenger_count", IntegerType(), True)
])

# Step 3: Read Streaming Data from Kafka
kafka_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "taxi_trips") \
    .option("startingOffsets", "earliest") \
    .load()

# Step 4: Parse Kafka Value as JSON
parsed_df = kafka_df.selectExpr("CAST(value AS STRING) as json_value") \
    .select(from_json(col("json_value"), schema).alias("data")) \
    .select("data.*")

# Step 5: Transform columns (convert to timestamp type)
final_df = parsed_df.withColumn("pickup_datetime", to_timestamp("pickup_datetime")) \
                    .withColumn("dropoff_datetime", to_timestamp("dropoff_datetime"))

# Step 6: Write Stream into Postgres
query = final_df.writeStream \
    .foreachBatch(lambda batch_df, batch_id: 
        batch_df.write
        .format("jdbc")
        .option("url", "jdbc:postgresql://postgres:5432/taxi_rides") \
        .option("dbtable", "rides") \
        .option("user", "taxi") \
        .option("password", "taxi123") \
        .option("driver", "org.postgresql.Driver") \
        .mode("append")
        .save()
    ) \
    .outputMode("update") \
    .start()

query.awaitTermination()
