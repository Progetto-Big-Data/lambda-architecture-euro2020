from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split
from pyspark.streaming import *

spark = SparkSession \
    .builder \
    .appName("Total goals streaming") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

streaming = StreamingContext(
    sparkContext=spark.sparkContext,
    batchDuration=10
)

records = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "final_fixtures") \
    .load()

fixtures = records.select(
    split(records.value, ",").alias("fixture")
)

home_goals = fixtures.select(
    fixtures.fixture[1].alias("home_team"), 
    fixtures.fixture[3].cast("integer").alias("home_goal")
)

total_home_goals = home_goals.groupBy("home_team").sum("home_goal")

query = total_home_goals \
    .writeStream \
    .outputMode("complete") \
    .format("console") \
    .start()

query.awaitTermination()