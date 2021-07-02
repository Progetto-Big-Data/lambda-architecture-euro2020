$SPARK_HOME/bin/spark-submit \
    --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.1 \
    --master yarn \
    streaming/total_goals/main.py