import time
import httpx
from datetime import datetime


def current_milli_time():
    return round(time.time() * 1000)


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


def databricksWrite(tablename,dataframe,mode,spark):
    spark.sql('drop table if exists '+tablename+' ')
    dataframe.write.format("delta").mode(mode).saveAsTable(tablename)


def s3Write(dataframe,databasename,tablename):
    s3location=f's3a://rightdataspark/{databasename}/{tablename}'
    print("s3location>>>>",s3location)
    print("dataframe count>>>>",dataframe.count())

    dataframe.write.mode("overwrite").option("header", "true").parquet(s3location)


def redshift(input_url, input_username, input_password, queryOrtableFlag, queryOrtable,numPartitions,fetchsize,spark,redshift_tempdir):
    if (queryOrtableFlag=='query'):
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
        
    elif (queryOrtableFlag=='table'):
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


def snowflake(sfUrl, sfUser, sfPassword, sfDatabase,sfSchema,sfWarehouse,queryOrtableFlag, queryOrtable,numPartitions,fetchsize, spark):
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

def mssql(input_url, input_username, input_password, queryOrtableFlag, queryOrtable,numPartitions,fetchsize,prepare_query, spark):
    print("queryOrtable: \n")
    # print(queryOrtable)
    if queryOrtableFlag == "query":
        if(prepare_query.strip() !=""):
            print("prepare_query: ",prepare_query)
            df = (
                spark.read.format("jdbc")
                .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver")
                .option("url", input_url)
                .option("prepareQuery", prepare_query)
                .option("query", queryOrtable)
                .option("user", input_username)
                .option("password", input_password)
                .option("numPartitions", numPartitions)
                .option("fetchsize", fetchsize)
                .load()
            )
            
        else:
            print("prepare_query null:",prepare_query)
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

def postgresql(input_url, input_username, input_password, queryOrtableFlag, queryOrtable,numPartitions,fetchsize, spark):
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

def databricks(queryOrtable,queryOrtableFlag,spark):
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

    try:
        df.write.format("com.microsoft.sqlserver.jdbc.spark") \
        .mode(target_write_mode) \
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
    except ValueError as error :
        print("Connector write failed", error)

    return "success"


def w_response_builder(run_id,source_row_count,before_target_count,after_target_count,status_message,jobStatus,startTime,endTime):
    w_response={
    "runId": run_id,
    "notebookData": {
        "sourceRowCount":source_row_count,
        "beforeTargetCount": before_target_count,
        "afterTargetCount": after_target_count,
        "statusMessage": status_message,
        "jobStatus":jobStatus,
        "startTime":startTime,
        "endTime":endTime
        
    }
}
    print(w_response)
    return w_response

async def send_request1(webhook_url,w_response):
    # The URL of endpoint
    url = webhook_url
    print(url)

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=w_response)

        # Check the response
        if response.status_code == 200:
            print("Item created successfully:")
            print(response.json())
        else:
            print(f"Failed to create item. Status code: {response.status_code}")
            print(response.text)


async def send_request(webhook_url,w_response):
    today_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    # The URL of endpoint
    url = webhook_url
    print(url)
    try:
        print("inside try")
        async with httpx.AsyncClient() as client:

            response = await client.post(url, json=w_response)

            # Check the response
            if response.status_code == 200:
                print("Item created successfully:")
                print(response.json())
            else:
                print(f"Failed to create item. Status code: {response.status_code}")
                print(response.text)


    except Exception as ex:
        print("issue with: ",url)
        print(ex)