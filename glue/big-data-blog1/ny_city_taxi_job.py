import sys

from pyspark.sql.functions import lit
from awsglue.dynamicframe import DynamicFrame
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'target_bucket', 'color'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)
## @type: DataSource
## @args: [database = "nycitytaxianalysis", table_name = "blog_args['color']", transformation_ctx = "datasource0"]
## @return: datasource0
## @inputs: []
datasource0 = glueContext.create_dynamic_frame.from_catalog(database = "nycitytaxianalysis", table_name = "blog_{}".format(args['color']), transformation_ctx = "datasource0")
## @type: ApplyMapping
## @args: [mapping = [("vendorid", "long", "vendorid", "long"), ("tpep_pickup_datetime", "string", "pickup_datetime", "timestamp"), ("tpep_dropoff_datetime", "string", "dropoff_datetime", "timestamp"), ("passenger_count", "long", "passenger_count", "long"), ("trip_distance", "double", "trip_distance", "double"), ("pickup_longitude", "double", "pickup_longitude", "double"), ("pickup_latitude", "double", "pickup_latitude", "double"), ("ratecodeid", "long", "ratecodeid", "long"), ("store_and_fwd_flag", "string", "store_and_fwd_flag", "string"), ("dropoff_longitude", "double", "dropoff_longitude", "double"), ("dropoff_latitude", "double", "dropoff_latitude", "double"), ("payment_type", "long", "payment_type", "long"), ("fare_amount", "double", "fare_amount", "double"), ("extra", "double", "extra", "double"), ("mta_tax", "double", "mta_tax", "double"), ("tip_amount", "double", "tip_amount", "double"), ("tolls_amount", "double", "tolls_amount", "double"), ("improvement_surcharge", "double", "improvement_surcharge", "double"), ("total_amount", "double", "total_amount", "double")], transformation_ctx = "applymapping1"]
## @return: applymapping1
## @inputs: [frame = datasource0]
applymapping1 = ApplyMapping.apply(frame = datasource0, mappings = [("vendorid", "long", "vendorid", "long"), ("tpep_pickup_datetime", "string", "pickup_datetime", "timestamp"), ("tpep_dropoff_datetime", "string", "dropoff_datetime", "timestamp"), ("passenger_count", "long", "passenger_count", "long"), ("trip_distance", "double", "trip_distance", "double"), ("pickup_longitude", "double", "pickup_longitude", "double"), ("pickup_latitude", "double", "pickup_latitude", "double"), ("ratecodeid", "long", "ratecodeid", "long"), ("store_and_fwd_flag", "string", "store_and_fwd_flag", "string"), ("dropoff_longitude", "double", "dropoff_longitude", "double"), ("dropoff_latitude", "double", "dropoff_latitude", "double"), ("payment_type", "long", "payment_type", "long"), ("fare_amount", "double", "fare_amount", "double"), ("extra", "double", "extra", "double"), ("mta_tax", "double", "mta_tax", "double"), ("tip_amount", "double", "tip_amount", "double"), ("tolls_amount", "double", "tolls_amount", "double"), ("improvement_surcharge", "double", "improvement_surcharge", "double"), ("total_amount", "double", "total_amount", "double")], transformation_ctx = "applymapping1")
## @type: ResolveChoice
## @args: [choice = "make_struct", transformation_ctx = "resolvechoice2"]
## @return: resolvechoice2
## @inputs: [frame = applymapping1]
resolvechoice2 = ResolveChoice.apply(frame = applymapping1, choice = "make_struct", transformation_ctx = "resolvechoice2")
## @type: DropNullFields
## @args: [transformation_ctx = "dropnullfields3"]
## @return: dropnullfields3
## @inputs: [frame = resolvechoice2]
dropnullfields3 = DropNullFields.apply(frame = resolvechoice2, transformation_ctx = "dropnullfields3")

##----------------------------------
#convert to a Spark DataFrame...
customDF = dropnullfields3.toDF()
#add a new column for "type"
customDF = customDF.withColumn("type", lit(args['color']))
# Convert back to a DynamicFrame for further processing.
customDynamicFrame = DynamicFrame.fromDF(customDF, glueContext, "customDF_df")
##----------------------------------

## @type: DataSink
## @args: [connection_type = "s3", connection_options = {"path": "s3://args['target_bucket']"}, format = "parquet", transformation_ctx = "datasink4"]
## @return: datasink4
## @inputs: [frame = dropnullfields3]
datasink4 = glueContext.write_dynamic_frame.from_options(frame = customDynamicFrame, connection_type = "s3", connection_options = {"path": "s3://{}/{}".format(args['target_bucket'], args['color'])}, format = "parquet", transformation_ctx = "datasink4")

job.commit()
