from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import from_json, explode
from pyspark.streaming import *

spark = SparkSession \
    .builder \
    .appName("Total goals streaming") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")


home_goals = spark \
    .read \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "home_goals") \
    .option("startingOffsets", "earliest") \
    .load()


away_goals = spark \
    .read \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "away_goals") \
    .option("startingOffsets", "earliest") \
    .load()


home_schema = StructType(
    [
    StructField("team", StringType()), 
    StructField("home_goal", IntegerType())
    ]
)

away_schema = StructType(
    [
    StructField("team", StringType()), 
    StructField("away_goal", IntegerType())
    ]
)

home_goals = home_goals.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)") 
home_goals = home_goals.select(from_json(home_goals.value, home_schema).alias("json"))
home_goals = home_goals.select(
    home_goals.json.team.alias("team"),
    home_goals.json.home_goal.alias("home_goal")
)

away_goals = away_goals.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)") 
away_goals = away_goals.select(from_json(away_goals.value, away_schema).alias("json"))
away_goals = away_goals.select(
    away_goals.json.team.alias("team"),
    away_goals.json.away_goal.alias("away_goal")
)

total_goals = home_goals.join(away_goals, "team", "outer")
total_goals = total_goals.na.fill(0)

total_goals = total_goals.select(
    total_goals.team,
    (total_goals.home_goal + total_goals.away_goal).alias("total_goal")
)

#removes header noise
headers = ['home_team', 'away_team']
total_goals = total_goals.filter(total_goals.team.isin(headers) == False)

total_goals.coalesce(1) \
    .write \
    .csv("total_goals_streaming")