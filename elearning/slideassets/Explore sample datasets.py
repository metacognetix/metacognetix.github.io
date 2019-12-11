# Databricks notebook source
# DBTITLE 1,List sample datasets available in Databricks CE
display(dbutils.fs.ls("/databricks-datasets"))


# COMMAND ----------

selected_dataset = "sample_logs"
selected_dataset_path = "/databricks-datasets/" + selected_dataset

print(selected_dataset_path)

# COMMAND ----------

# DBTITLE 1,List the files in a dataset
filelist = dbutils.fs.ls(selected_dataset_path)
display(filelist)

# COMMAND ----------

from pyspark.sql import *

filelistDF = sqlContext.createDataFrame(filelist)

# COMMAND ----------

just_readme = filelistDF.filter((filelistDF.name == "README.md") | (filelistDF.name == "readme.md"))
display(just_readme)

# COMMAND ----------

filelistDF.createOrReplaceTempView("filelist_view")


# COMMAND ----------

# MAGIC 
# MAGIC %sql
# MAGIC select `path` from filelist_view where `name` like 'README%'

# COMMAND ----------

#print(filelist)
print(filelist[0][1])

with open("/dbfs/" + selected_dataset_path + "/part-00004") as f:
  x = ''.join(f.readlines())
  
print(x)

# COMMAND ----------

 export_json = filelistDF.toJSON()
print(export_json.take(2))

# COMMAND ----------

import re
from pyspark.sql import Row

apache_access_log_format = '^(\S+) (\S+) (\S+) \[([\w:/]+\s[+\-]\d{4})\] "(\S+) (\S+) (\S+)" (\d{3}) (\d+)'

#Return a dictionary containing the parts of the Apache access log
def parse_apache_log_line(line):
  match = re.search(apache_access_log_format, line)
  if match is None:
    # Might want to just ignore, since it'a common to have dirty logs
    raise Error("Invalid log line format: %s" % line)
  return Row(
    ipAddress = match.group(1),
    clientIdentd = match.group(2),
    userId = match.group(3),
    dateTime = match.group(4),
    method = match.group(5),
    endpoint = match.group(6),
    protocol = match.group(7),
    responseCode = int(match.group(8)),
    contentSize = long(match.group(9)))
    

# COMMAND ----------

logfileload = sc.textfile(selected_dataset_path + "/part-00004")
#accesslogs = (sc.textfile(selected_dataset_path + "/part-00004").map(parse_apache_log_line).cache())

# COMMAND ----------


