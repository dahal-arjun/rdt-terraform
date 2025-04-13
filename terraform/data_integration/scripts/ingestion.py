from pyspark.sql import SparkSession
import argparse
import time
from ingestion_unit import *
import re
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Boolean, Column, String

SQLALCHEMY_DATABASE_URL = f'postgresql://spark:spark@3.7.15.0:5432/postgres'

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Session(Base):
    __tablename__ = "session"

    id = Column(String, primary_key=True, index=True)
    application_id = Column(String)
    driver_id = Column(String)
    
def current_milli_time():
    return round(time.time() * 1000)


start = current_milli_time()
print("start::", start)
redshift_tempdir = "s3a://db-6e5564b8abd47a6f78a0237b2654bc92-s3-root-bucket/rdt-databricks"
webhook_url = "http://54.243.34.74:9090/run_update"

#############################
#### input parameters starts here####


try:
    parser = argparse.ArgumentParser(description="PySpark Job with Named Parameters")
    parser.add_argument("--master_url")
    parser.add_argument("--inputSourceType")
    parser.add_argument("--submission_id")
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
    parser.add_argument("--targetHost", default="None")
    parser.add_argument("--targetPort", default="1433")
    parser.add_argument("--targetUserName", default="rd_usr_sprk")
    parser.add_argument("--targetPassword", default="RDExtUser12345")
    parser.add_argument("--targetNumPartitions", default=5)
    parser.add_argument("--targetBatchSize", default=50000)
    parser.add_argument("--targetReliabilityLevel", default="BEST_EFFORT")
    parser.add_argument("--targetSchemaCheckEnabled", default="false")
    parser.add_argument("--targetTableLock", default=True)

    args = parser.parse_args()
    MASTER_URL = args.master_url

    ACCESS_KEY_ID = "AKIAUNQOQD6U5XOECP6V"
    SECRET_ACCESS_KEY = "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"
    region = "ap-south-1"

    input_source_type = args.inputSourceType
    input_url = args.inputUrl
    print("input_url :::: ",input_url)
    inputSpark = args.inputSpark
    submission_id = args.submission_id
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
print(MASTER_URL)
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

application_id = spark.sparkContext.applicationId

submission_id = args.submission_id


def write_application_id(submission_id, application_id):
    db = next(get_db())
    #update application_id in db for submission_id
    session = db.query(Session).filter(Session.id == submission_id).first()
    session.application_id = application_id
    db.commit()
    db.close()
    
write_application_id(submission_id, application_id)
    
print("application_id :::: ",application_id)
# write_application_id(submission_id, application_id)

    


    
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