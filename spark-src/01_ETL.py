from pyspark.sql import functions as F
from pyspark.sql.window import Window
import threading
import asyncio
import threading
import time
# import httpx
from datetime import datetime
import json
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, StringType
import argparse


aws_access_key_id = os.environ.get('ACCESS_KEY')
aws_secret_access_key = os.environ.get('SECRET_KEY')
ACCESS_KEY_ID = aws_access_key_id
SECRET_ACCESS_KEY = aws_secret_access_key
MASTER_URL = "3.7.15.0"


def current_milli_time():
    return round(time.time() * 1000)


def mssql_write(df,target_write_mode, output_url,output_username, output_password,output_table,numPartitions,batchsize,reliabilityLevel,schemaCheckEnabled,tableLock):
    print(df.count())
    print("target_write_mode>>",target_write_mode)
    print(output_url)
    print(output_username)
    print(output_password)
    print("output_table>>",output_table)
    print(numPartitions)
    print("batchsize>>",batchsize)
    print(reliabilityLevel)
    print("schemaCheckEnabled>>",schemaCheckEnabled)
    print(tableLock)
    try:
        # df.write.format("jdbc") \
        #     .mode("overwrite") \
        #     .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver") \
        #     .option("url", output_url) \
        #     .option("dbtable", output_table) \
        #     .option("user", output_username) \
        #     .option("password", output_password) \
        #     .option("batchsize", batchsize) \
        #     .save()
            # .option("batchsize", batchsize) \
            # .option("numPartitions", numPartitions) \
            # .option("reliabilityLevel", reliabilityLevel) \
            # .option("schemaCheckEnabled", schemaCheckEnabled) \
            # .option("tableLock", tableLock) \
            # .save()
        df.write.format("com.microsoft.sqlserver.jdbc.spark").mode("overwrite") \
        .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver") \
        .option("url", output_url) \
        .option("dbtable", output_table) \
        .option("user", output_username) \
        .option("password", output_password) \
        .option("batchsize",batchsize) \
        .option("numPartitions",numPartitions) \
        .option("reliabilityLevel", reliabilityLevel) \
        .option("schemaCheckEnabled", schemaCheckEnabled) \
        .option("tableLock", tableLock) \
        .save()
    ### .option("tableLock", "true") \
    except ValueError as error :
        print("Connector write failed", error)


def s3Write(dataframe,databasename,tablename):
    s3location=f's3a://rightdataspark/{databasename}/{tablename}'
    print("s3location>>>>",s3location)
    print("dataframe count>>>>",dataframe.count())

    dataframe.write.mode("overwrite").option("header", "true").parquet(s3location)




def s3_read_parquet(databasename, tablename):
    s3location = f's3a://rightdataspark/{databasename}/{tablename}'
    print("read s3location>>", s3location)

    df = spark.read.parquet(s3location)
    print(df.count())
    return df

def strtobool (val):
    """Convert a string representation of truth to true (1) or false (0).
    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
    'val' is anything else.
    """
    val = val.lower()
    if val in ('y', 'yes', 't', 'true', 'on', '1'):
        return 1
    elif val in ('n', 'no', 'f', 'false', 'off', '0'):
        return 0
    else:
        raise ValueError("invalid truth value %r" % (val,))


start = current_milli_time()
print("############init 1")


#### input parameters starts here#######
try:
    # ####Input parameters
    #### inputPort we dont need
    parser = argparse.ArgumentParser(description="PySpark Job with Named Parameters comparision")
    parser.add_argument("--master_url")
    # parser.add_argument("--access_key_id")
    # parser.add_argument("--secret_access_key")

    parser.add_argument("--performETL")
    parser.add_argument("--inputSpark")
    parser.add_argument("--etlSqlQuery")


    parser.add_argument("--targetSourceType")
    parser.add_argument("--targetHost",default="None")
    parser.add_argument("--targetPort",default="1433")
    parser.add_argument("--targetDatabase")
    parser.add_argument("--targetUserName",default="rd_usr_sprk")
    parser.add_argument("--targetPassword",default="RDExtUser12345")
    parser.add_argument("--targetDbTable")
    parser.add_argument("--targetWriteMode")
    parser.add_argument("--targetNumPartitions",default=5)
    parser.add_argument("--targetBatchSize",default=50000)
    parser.add_argument("--targetReliabilityLevel",default="BEST_EFFORT")
    parser.add_argument("--targetSchemaCheckEnabled",default="false")
    parser.add_argument("--targetTableLock",default=True)
    parser.add_argument("--src",default="src_table")
    parser.add_argument("--tgt",default="target_table")




    args = parser.parse_args()
    MASTER_URL = args.master_url

    region = "ap-south-1"


    performETL = bool(strtobool(args.performETL))

    # inputSpark = args.inputSpark
    inputSpark = bool(strtobool(args.inputSpark))

    etlSqlQuery = args.etlSqlQuery

    target_source_type = args.targetSourceType
    target_host = args.targetHost
    target_port = args.targetPort
    target_database = args.targetDatabase
    target_username = args.targetUserName
    target_password = args.targetPassword
    target_dbtable = args.targetDbTable
    target_write_mode = args.targetWriteMode
    target_numPartitions = args.targetNumPartitions
    target_batch_size = args.targetBatchSize
    target_reliabilityLevel = args.targetReliabilityLevel
    target_schemaCheckEnabled = args.targetSchemaCheckEnabled
    target_tableLock = args.targetTableLock
    src = args.src
    tgt = args.tgt






    print("########################inputSpark, ",inputSpark)
    print("#######################performETL, ",performETL)
    print("#########################src, ",src)
    print("###################################tgt, ",tgt)





except Exception as ex:
    print("Exception occur")
    end = current_milli_time()
    # w_response_data = w_response_builder(run_id, 0, 0, 0, str(str(ex)[0:500]), "failed", start, end)
    # print(w_response_data)
    # await send_request(webhook_url, w_response_data)
    time.sleep(1.5)
    # dbutils.notebook.exit(str(ex))
    print("doesnot exeuted")


spark = SparkSession.builder \
    .master(f"spark://{MASTER_URL}:7077") \
    .appName("AWS cluster Comparision") \
    .config("spark.hadoop.mapreduce.fileoutputcommitter.algorithm.version", 2) \
    .config("spark.sql.parquet.output.committer.class", "org.apache.hadoop.mapreduce.lib.output.FileOutputCommitter") \
    .config("spark.sql.parquet.output.committer.factory",
            "com.apache.spark.sql.execution.datasources.parquet.ParquetOutputCommitterFactory") \
    .config("spark.scheduler.mode", "FAIR") \
    .config("spark.submit.deployMode", "client") \
    .config("spark.hadoop.fs.s3a.access.key", ACCESS_KEY_ID) \
    .config("spark.hadoop.fs.s3a.secret.key", SECRET_ACCESS_KEY) \
    .getOrCreate()

print("############init 2")

if(inputSpark):
    srd_db=src.split(".")[0]
    srd_tbl=src.split(".")[-1]
    print("######################### srd_db, ", srd_db)
    print("######################### srd_tbl, ", srd_tbl)
    src_df=s3_read_parquet(srd_db, srd_tbl)
    src_df.createOrReplaceTempView("_source_table")

    tgt_df=s3_read_parquet(tgt.split(".")[0], (tgt.split(".")[1]))
    tgt_df.createOrReplaceTempView("_target_table")

    updated_etlSqlQuery = etlSqlQuery.replace(src, "_source_table").replace(
        tgt, "_target_table")


    print(updated_etlSqlQuery)

print("######### before comparision   ")
outdf = spark.sql(updated_etlSqlQuery)

print("######### after comparision   ")
print("outdf count>> ",outdf.count())



try:

    if (target_source_type=='mssql'): #done
        # target_url = f"jdbc:sqlserver://{target_host}:{target_port};database={target_database};encrypt=false"
        # print("mssql url :::: ",target_url)
        # print("target rows :::: ",outdf.count())
        print("target_source_type :::: ",target_source_type)
        target_url = f"jdbc:sqlserver://{target_host}:{target_port};database={target_database};encrypt=false"
        print("#############target_url :::: ",target_url)

        target_df=mssql_write(outdf,target_write_mode, target_url,target_username, target_password,target_dbtable,target_numPartitions,target_batch_size,target_reliabilityLevel,target_schemaCheckEnabled,target_tableLock)
        print("################## mssql write done yaya")
        # print("write completed to mssql  table:",target_dbtable)
        # end = current_milli_time()
        # w_response_data1=w_response_builder(run_id,outdf.count(),outdf.count(),outdf.count(),"completed","success",start,end)
        # await send_request(webhook_url,w_response_data1)
        print(target_source_type)
        # print(input_source_type)
    elif (target_source_type=='s3'):

        s3Write(outdf,target_database,target_dbtable)
        print("target rows :::: ",outdf.count())
        print("write completed to s3 bucket:",target_dbtable)
        end = current_milli_time()
        # w_response_data1=w_response_builder(run_id,outdf.count(),outdf.count(),outdf.count(),"completed","success",start,end)
        # await send_request(webhook_url,w_response_data1)
        print(target_source_type)
        # print(input_source_type)

except Exception as ex:
    print("Exception occur 3")
    print(ex)
    end = current_milli_time()
    # w_response_data=w_response_builder(run_id,outdf.count(),0,0,str(str(ex)[0:500]),"failed",start,end)
    # print(w_response_data)
    # await send_request(webhook_url,w_response_data)
    time.sleep(1.4)
    # dbutils.notebook.exit(str(ex))
    print("doesnot exeuted 3")

print("all done ")










    # df.createOrReplaceTempView("leftover")
# input_1 = s3_read_parquet("rdt_demo_data", "rightdata_db_dbo_S_1470_18_SOURCE")
# print("############init 3")

# input_1.show(100)






