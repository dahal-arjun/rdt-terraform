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




def current_milli_time():
    return round(time.time() * 1000)


def databricksWrite(tablename,dataframe,mode):
#     mode='overwrite'
    spark.sql('drop table if exists '+tablename+' ')
    dataframe.write.format("delta").mode(mode).saveAsTable(tablename)

def s3Write(dataframe,databasename,tablename):
    s3location=f's3a://rightdataspark/{databasename}/{tablename}'
    print("s3location>>>>",s3location)
    print("dataframe count>>>>",dataframe.count())

    dataframe.write.mode("overwrite").option("header", "true").parquet(s3location)




def redshift(input_url, input_username, input_password, queryOrtableFlag, queryOrtable, numPartitions, fetchsize):
    if (queryOrtableFlag == 'query'):
        df = (
            spark.read.format("redshift")
            .option("url", input_url)
            .option("forward_spark_s3_credentials", True)
            .option("user", input_username)
            .option("password", input_password)
            .option("tempdir", redshift_tempdir)
            .option("query", queryOrtable)
            .option("numPartitions", numPartitions)
            .option("fetchsize", fetchsize)
            .load()
        )

    elif (queryOrtableFlag == 'table'):
        df = (
            spark.read.format("redshift")
            .option("url", input_url)
            .option("forward_spark_s3_credentials", True)
            .option("user", input_username)
            .option("password", input_password)
            .option("tempdir", redshift_tempdir)
            .option("dbtable", queryOrtable)
            .option("numPartitions", numPartitions)
            .option("fetchsize", fetchsize)
            .load()
        )
    # display(df)
    return df


def snowflake(spark,sfUrl, sfUser, sfPassword, sfDatabase,sfSchema,sfWarehouse,queryOrtableFlag, queryOrtable,numPartitions,fetchsize):
    if queryOrtableFlag == "query":
        df = (
            spark.read.format("snowflake")
            .option("query", queryOrtable)
            .option("sfUrl", sfUrl)
            .option("sfUser", sfUser)
            .option("sfPassword", sfPassword)
            .option("sfDatabase", sfDatabase)
            .option("sfSchema", sfSchema)
            .option("sfWarehouse", sfWarehouse)
            .load()
        )

    elif queryOrtableFlag == "table":
        df = (
            spark.read.format("snowflake")
            .option("dbtable", queryOrtable)
            .option("sfUrl", sfUrl)
            .option("sfUser", sfUser)
            .option("sfPassword", sfPassword)
            .option("sfDatabase", sfDatabase)
            .option("sfSchema", sfSchema)
            .option("sfWarehouse", sfWarehouse)
            .load()
        )
    return df




def mssql(input_url, input_username, input_password, queryOrtableFlag, queryOrtable,numPartitions,fetchsize):
    if queryOrtableFlag == "query":
        df = (
            spark.read.format("jdbc")
            .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver")
            .option("url", input_url)
            .option("query", queryOrtable)
            .option("user", input_username)
            .option("password", input_password)
            .option("numPartitions", numPartitions)
            .option("fetchsize", fetchsize)
            .load()
        )

    elif queryOrtableFlag == "table":
        df = (
            spark.read.format("jdbc")
            .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver")
            .option("url", input_url)
            .option("dbtable", queryOrtable)
            .option("user", input_username)
            .option("password", input_password)
            .option("numPartitions", numPartitions)
            .option("fetchsize", fetchsize)
            .load()
        )
    return df

def postgresql(input_url, input_username, input_password, queryOrtableFlag, queryOrtable,numPartitions,fetchsize):
    if queryOrtableFlag == "query":
        df = (
            spark.read.format("jdbc")
            .option("driver", "org.postgresql.Driver")
            .option("url", input_url)
            .option("query", queryOrtable)
            .option("user", input_username)
            .option("password", input_password)
            .option("numPartitions", numPartitions)
            .option("fetchsize", fetchsize)
            .load()
        )

    elif queryOrtableFlag == "table":
        df = (
            spark.read.format("jdbc")
            .option("driver", "org.postgresql.Driver")
            .option("url", input_url)
            .option("dbtable", queryOrtable)
            .option("user", input_username)
            .option("password", input_password)
            .option("numPartitions", numPartitions)
            .option("fetchsize", fetchsize)
            .load()
        )
    return df

def databricks(queryOrtable,queryOrtableFlag):
    if queryOrtableFlag == "query":
        df = spark.sql(queryOrtable)

    elif queryOrtableFlag == "table":
        df = spark.read.table(queryOrtable)

    return df

def postgresql_write(df, output_url,output_username, output_password,target_write_mode,output_table,repartition,batchsize):

    (df.repartition(int(repartition)).write.mode(target_write_mode).format("jdbc")
    .option("url", output_url)
    .option("driver", "org.postgresql.Driver")
    .option("dbtable", output_table)
    .option("user", output_username)
    .option("batchsize", int(batchsize))
    .option("password", output_password)
    .save())

    return "success"

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


def w_response_builder(run_id, source_row_count, before_target_count, after_target_count, status_message, jobStatus,
                       startTime, endTime):
    w_response = {
        "runId": run_id,
        "notebookData": {
            "sourceRowCount": source_row_count,
            "beforeTargetCount": before_target_count,
            "afterTargetCount": after_target_count,
            "statusMessage": status_message,
            "jobStatus": jobStatus,
            "startTime": startTime,
            "endTime": endTime

        }
    }
    print(w_response)
    return w_response



# async def send_request1(webhook_url,w_response):
#     # The URL of endpoint
#     url = webhook_url
#     print(url)
#
#     async with httpx.AsyncClient() as client:
#         response = await client.post(url, json=w_response)
#
#         # Check the response
#         if response.status_code == 200:
#             print("Item created successfully:")
#             print(response.json())
#         else:
#             print(f"Failed to create item. Status code: {response.status_code}")
#             print(response.text)

# COMMAND ----------

# async def send_request(webhook_url,w_response):
#     today_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
#
#     # The URL of endpoint
#     url = webhook_url
#     print(url)
#     try:
#         print("inside try")
#         async with httpx.AsyncClient() as client:
#
#             response = await client.post(url, json=w_response)
#
#             # Check the response
#             if response.status_code == 200:
#                 print("Item created successfully:")
#                 print(response.json())
#             else:
#                 print(f"Failed to create item. Status code: {response.status_code}")
#                 print(response.text)
#
#
#     except Exception as ex:
#         print("issue with: ",url)
#         print(ex)



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
print("start::",start)
redshift_tempdir= "s3a://db-6e5564b8abd47a6f78a0237b2654bc92-s3-root-bucket/rdt-databricks"
# webhook_url = "http://54.243.34.74:9090/run_update"

#############################
#### input parameters starts here#######
try:
    # ####Input parameters
    #### inputPort we dont need
    parser = argparse.ArgumentParser(description="PySpark Job with Named Parameters")
    parser.add_argument("--master_url")
    # parser.add_argument("--access_key_id")
    # parser.add_argument("--secret_access_key")

    parser.add_argument("--inputSourceType")
    parser.add_argument("--inputUrl")
    parser.add_argument("--inputUserName")
    parser.add_argument("--inputPassword")
    parser.add_argument("--inputDbTable")
    parser.add_argument("--inputQueryOrTableFlag")
    parser.add_argument("--inputNumPartitions")
    parser.add_argument("--inputFetchSize")
    parser.add_argument("--inputSchema")
    parser.add_argument("--inputWarehouse")
    parser.add_argument("--inputDatabase")

    parser.add_argument("--targetSourceType")
    parser.add_argument("--targetDbTable")
    parser.add_argument("--targetDatabase")
    parser.add_argument("--targetWriteMode")
    parser.add_argument("--targetHost",default="None")
    parser.add_argument("--targetPort",default="1433")
    parser.add_argument("--targetUserName",default="rd_usr_sprk")
    parser.add_argument("--targetPassword",default="RDExtUser12345")
    parser.add_argument("--targetNumPartitions",default=5)
    parser.add_argument("--targetBatchSize",default=50000)
    parser.add_argument("--targetReliabilityLevel",default="BEST_EFFORT")
    parser.add_argument("--targetSchemaCheckEnabled",default="false")
    parser.add_argument("--targetTableLock",default=True)



    args = parser.parse_args()
    MASTER_URL = args.master_url


    aws_access_key_id = os.environ.get('ACCESS_KEY')
    aws_secret_access_key = os.environ.get('SECRET_KEY')
    ACCESS_KEY_ID = aws_access_key_id
    SECRET_ACCESS_KEY = aws_secret_access_key
    aws_region = os.environ.get('REGION')
    ACCESS_KEY_ID = aws_access_key_id
    SECRET_ACCESS_KEY = aws_secret_access_key
    region = aws_region

    input_source_type = args.inputSourceType
    input_url = args.inputUrl
    input_username = args.inputUserName
    input_password = args.inputPassword
    input_dbtable = args.inputDbTable
    input_queryOrtableFlag = args.inputQueryOrTableFlag
    input_numPartitions = args.inputNumPartitions
    input_fetchsize = args.inputFetchSize
    input_schema = args.inputSchema
    input_warehouse = args.inputWarehouse
    input_database = args.inputDatabase

    target_source_type = args.targetSourceType
    target_dbtable = args.targetDbTable
    target_write_mode = args.targetWriteMode
    target_database = args.targetDatabase
    target_host = args.targetHost
    target_port = args.targetPort
    target_username = args.targetUserName
    target_password = args.targetPassword
    target_numPartitions = args.targetNumPartitions
    target_batch_size = args.targetBatchSize
    target_reliabilityLevel = args.targetReliabilityLevel
    target_schemaCheckEnabled = args.targetSchemaCheckEnabled
    target_tableLock = args.targetTableLock





    print("##############target_host>>",target_host)
    print("#################input_source_type>",input_source_type)





except Exception as ex:
    print("Exception occur")
    end = current_milli_time()
    # w_response_data = w_response_builder(run_id, 0, 0, 0, str(str(ex)[0:500]), "failed", start, end)
    # print(w_response_data)
    # await send_request(webhook_url, w_response_data)
    time.sleep(1.5)
    # dbutils.notebook.exit(str(ex))
    print("doesnot exeuted")

# dbutils.notebook.exit("stop")



spark = SparkSession.builder \
    .master(f"spark://{MASTER_URL}:7077") \
    .appName("AWS cluster standalone") \
    .config("spark.hadoop.mapreduce.fileoutputcommitter.algorithm.version", 2)  \
    .config("spark.sql.parquet.output.committer.class", "org.apache.hadoop.mapreduce.lib.output.FileOutputCommitter")  \
    .config("spark.sql.parquet.output.committer.factory", "com.apache.spark.sql.execution.datasources.parquet.ParquetOutputCommitterFactory")  \
    .config("spark.scheduler.mode", "FAIR") \
    .config("spark.hadoop.fs.s3a.access.key", ACCESS_KEY_ID) \
    .config("spark.hadoop.fs.s3a.secret.key", SECRET_ACCESS_KEY) \
    .getOrCreate()


#############################
#### input parameters starts ends#######

print("input_source_type>>",input_source_type)
##################### fetching/reading data#################
try:
    end=0
    if (input_source_type=='postgresql'): #done
        print("input_url :::: ",input_url)
        # outdf=postgresql(input_url,input_username,input_password,input_queryOrtableFlag,input_dbtable,input_numPartitions,input_fetchsize)
        # print("postgresql rows :::: ",outdf.count())
        # w_response_data=w_response_builder(run_id,outdf.count(),0,0,"running","running",start,end)

    elif (input_source_type=='redshift'):##done
        print(input_url)
        # outdf=redshift(input_url, input_username, input_password, input_queryOrtableFlag, input_dbtable,input_numPartitions,input_fetchsize)
        # print("redshift rows :::: ",outdf.count())
        # w_response_data=w_response_builder(run_id,outdf.count(),0,0,"running","running",start,end)
    elif (input_source_type=='snowflake'):###done
        print(input_url)
        outdf=snowflake(spark,input_url, input_username, input_password, input_database,input_schema,input_warehouse,input_queryOrtableFlag, input_dbtable,input_numPartitions,input_fetchsize)
        print("snowflake rows :::: ",outdf.count())
        # w_response_data=w_response_builder(run_id,outdf.count(),0,0,"running","running",start,end)
    elif (input_source_type=='mssql'): ####done
        print(input_source_type)
        # outdf= mssql(input_url, input_username, input_password, input_queryOrtableFlag, input_dbtable,input_numPartitions,input_fetchsize)
        # print("mssql rows :::: ",outdf.count())
        # w_response_data=w_response_builder(run_id,outdf.count(),0,0,"running","running",start,end)
    elif (input_source_type=='databricks'): ####done
        print(input_source_type)
        # outdf= databricks(input_dbtable,input_queryOrtableFlag)
        # print("databricks rows :::: ",outdf.count())
        # w_response_data=w_response_builder(run_id,outdf.count(),0,0,"running","running",start,end)



    # print (w_response_data)

    # await send_request(webhook_url,w_response_data)

except Exception as ex:
    print("Exception occur 2")
    end = current_milli_time()
    # w_response_data=w_response_builder(run_id,0,0,0,str(str(ex)[0:500]),"failed",start,end)
    # print(w_response_data)
    # await send_request(webhook_url,w_response_data)
    time.sleep(1.4)
    # dbutils.notebook.exit(str(ex))
    print("doesnot exeuted 2")


# dbutils.notebook.exit("stop")

# outdf1=outdf
# display(outdf)

######### reading completed#####################

# print("read roes target rows :::: ", outdf.count())

########## writing data starts###########
try:

    if (target_source_type=='mssql'): #done
        # target_url = f"jdbc:sqlserver://{target_host}:{target_port};database={target_database};encrypt=false"
        # print("mssql url :::: ",target_url)
        # print("target rows :::: ",outdf.count())
        print("target_source_type :::: ",target_source_type)
        target_url = f"jdbc:sqlserver://{target_host}:{target_port};database={target_database};encrypt=false"
        print("#############target_url :::: ",target_url)

        target_df=mssql_write(outdf,target_write_mode, target_url,target_username, target_password,target_dbtable,target_numPartitions,target_batch_size,target_reliabilityLevel,target_schemaCheckEnabled,target_tableLock)
        # print("write completed to mssql  table:",target_dbtable)
        # end = current_milli_time()
        # w_response_data1=w_response_builder(run_id,outdf.count(),outdf.count(),outdf.count(),"completed","success",start,end)
        # await send_request(webhook_url,w_response_data1)
        print(target_source_type)
        print(input_source_type)
    elif (target_source_type=='s3'):

        s3Write(outdf,target_database,target_dbtable)
        print("target rows :::: ",outdf.count())
        print("write completed to s3 bucket:",target_dbtable)
        end = current_milli_time()
        # w_response_data1=w_response_builder(run_id,outdf.count(),outdf.count(),outdf.count(),"completed","success",start,end)
        # await send_request(webhook_url,w_response_data1)
        print(target_source_type)
        print(input_source_type)

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


    ####### writing data completed