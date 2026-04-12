from airflow import DAG
from airflow.operators.bash import BashOperator

from datetime import datetime

with DAG('smart_home_pipeline',
         start_date=datetime(2026,1,1),
         schedule_interval='@hourly',
         catchup=False,
         max_active_runs=1
         ) as dag:
    
    producer_task = BashOperator(
        task_id='run_producer',
        bash_command='docker start -a smart-home-producer'
    )
    
    consumer_task = BashOperator(
        task_id='run_consumer',
        bash_command='docker start -a smart-home-consumer'
    )
    
    spark_task = BashOperator(
        task_id='run_spark',
        bash_command='''
        docker exec smart-home-spark-master /opt/spark/bin/spark-submit \
        --master spark://spark-master:7077 \
        --jars /opt/jars/clickhouse-spark-runtime-3.5_2.12-0.10.0.jar \
        /opt/spark_processor/processor.py
        '''
    )
    
    producer_task >> consumer_task >> spark_task