from pyspark.sql import SparkSession
from pyspark.sql.functions import to_timestamp, date_format

from pathlib import Path
"""
надо подключиться к clickhouse и создать таблицу sensor_readings
"""

spark = SparkSession.builder.getOrCreate()

df = spark.read.parquet("/opt/data/*.parquet")
clean_df = df.dropDuplicates(["device_id", "timestamp"])

clean_df = clean_df.withColumn(
    "timestamp", 
    date_format(
        to_timestamp("timestamp", "yyyy-MM-dd'T'HH:mm:ss.SSSSSS"), 
        "yyyy-MM-dd HH:mm:ss.SSSSSS"
    )
)

clean_df.write \
    .format("clickhouse") \
    .option("host", "clickhouse") \
    .option("protocol", "http") \
    .option("http_port", "8123") \
    .option("database", "smart_home") \
    .option("table", "sensor_readings_2") \
    .option("user", "default") \
    .option("password", "default") \
    .option("ssl", "false") \
    .mode("append") \
    .save()

print(f"✅ Загружено записей: {clean_df.count()}")
spark.stop()


data_dir = Path("/opt/data")

parquet_files = list(data_dir.glob("*.parquet"))

for file_path in parquet_files:
    try:
        file_path.unlink()
        print(f"Удалён: {file_path.name}")
    except OSError as e:
        print(f"Ошибка при удалении {file_path.name}: {e}")
