from pyspark.sql import SparkSession
from pyspark.sql import functions
from pyspark.sql.functions import split
from pyspark.streaming import *

spark = SparkSession \
    .builder \
    .appName("Aggregate goals streaming") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

records = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "final_fixtures") \
    .option("startingOffsets", "earliest") \
    .load()

fixtures = records.select(
    split(records.value, ",").alias("fixture")
)

home_goals = fixtures.select(
    fixtures.fixture[1].alias("team"), 
    fixtures.fixture[3].cast("integer").alias("home_goal")
)

away_goals = fixtures.select(
    fixtures.fixture[2].alias("team"), 
    fixtures.fixture[4].cast("integer").alias("away_goal")
)

total_home_goals = home_goals.groupBy("team").agg(functions.sum("home_goal").alias("home_goal"))
total_away_goals = away_goals.groupBy("team").agg(functions.sum("away_goal").alias("away_goal"))


home_query = total_home_goals \
    .selectExpr("CAST(team AS STRING) AS key", "to_json(struct(*)) AS value") \
    .writeStream \
    .outputMode("complete") \
    .option("checkpointLocation", "/tmp/spark-streaming/home-goals/checkpoint") \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("topic", "home_goals") \
    .start()

away_query = total_away_goals \
    .selectExpr("CAST(team AS STRING) AS key", "to_json(struct(*)) AS value") \
    .writeStream \
    .outputMode("complete") \
    .option("checkpointLocation", "/tmp/spark-streaming/away-goals/checkpoint") \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("topic", "away_goals") \
    .start()

home_query.awaitTermination()
away_query.awaitTermination()