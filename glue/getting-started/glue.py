from __future__ import print_function

import os
import sys
from datetime import datetime


from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

print(os.environ)
## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
print(args)

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)
## @type: DataSource
## @args: [database = "glue-database-glue", table_name = "flights_kinesis_data", transformation_ctx = "datasource0"]
## @return: datasource0
## @inputs: []

datasource0 = glueContext.create_dynamic_frame.from_catalog(database='glue-database-glue',
                                                            table_name='flights_kinesis_data',
                                                            transformation_ctx='datasource0')
## @type: ApplyMapping
## @args: [mapping = [("state", "struct", "state", "struct"), ("deviceid", "string", "deviceid", "string"), ("timestamp", "long", "timestamp", "long"), ("test1", "boolean", "test1", "boolean")], transformation_ctx = "applymapping1"]
## @return: applymapping1
## @inputs: [frame = datasource0]
mappings = [
    ("state", "struct", "state", "struct"),
    ("deviceid", "string", "deviceid", "string"),
    ("timestamp", "long", "timestamp", "long"),
    ("test1", "boolean", "test1", "boolean")
]

applymapping1 = ApplyMapping.apply(frame=datasource0,
                                   mappings=mappings,
                                   transformation_ctx='applymapping1')
## @type: ResolveChoice
## @args: [choice = "make_struct", transformation_ctx = "resolvechoice2"]
## @return: resolvechoice2
## @inputs: [frame = applymapping1]
resolvechoice2 = ResolveChoice.apply(frame=applymapping1,
                                     choice='make_struct',
                                     transformation_ctx='resolvechoice2')
## @type: DropNullFields
## @args: [transformation_ctx = "dropnullfields3"]
## @return: dropnullfields3
## @inputs: [frame = resolvechoice2]
dropnullfields3 = DropNullFields.apply(frame=resolvechoice2,
                                       transformation_ctx='dropnullfields3')
## @type: DataSink
## @args: [connection_type = "s3", connection_options = {"path": "s3://glue-target-bucket-glue"}, format = "parquet", transformation_ctx = "datasink4"]
## @return: datasink4
## @inputs: [frame = dropnullfields3]
connection_options = {
    'path': 's3://glue-target-bucket-glue/{}'.format(datetime.strftime(datetime.now(), '%Y-%m-%d'))
}
datasink4 = glueContext.write_dynamic_frame.from_options(frame=dropnullfields3,
                                                         connection_type='s3',
                                                         connection_options=connection_options,
                                                         format='parquet',
                                                         transformation_ctx='datasink4')
job.commit()