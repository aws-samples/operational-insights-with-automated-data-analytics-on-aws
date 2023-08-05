# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import pandas as pd
import re
import json
import ast
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql import SparkSession

# This script transforms the CloudWatch Logs in JSON format in to the Apache Log Format fields.

def apply_transform(input_frame, input_args, glue_context, **kwargs):
    print(f"Input args: {input_args}")
    df = input_frame.toDF()
    pandas_df = df.toPandas()

    ip = "ip"
    username = "username"
    log_time = "log_time"
    http_request = "http_request"
    endpoint = "endpoint"
    http_version = "http_version"
    status_code = "status_code"
    request_size = "request_size"
    referrer = "referrer"
    user_agent = "user_agent"
    message = "message"

    regex_ip = "^((?:[0-9]{1,3}\.){3}[0-9]{1,3}).*$"
    regex_username = "^(?:[0-9]{1,3}\.){3}[0-9]{1,3} - (\w+) .*$"
    regex_log_time = "^(?:[0-9]{1,3}\.){3}[0-9]{1,3} - \w+ \[(.+)\] .*$"
    regex_http_request = '^(?:[0-9]{1,3}\.){3}[0-9]{1,3} - \w+ \[.+\] "([A-Z]+).*$'
    regex_endpoint = (
        '^(?:[0-9]{1,3}\.){3}[0-9]{1,3} - \w+ \[.+\] "[A-Z]+ ([a-zA-Z0-9\/]*) .*$'
    )
    regex_http_version = '^(?:[0-9]{1,3}\.){3}[0-9]{1,3} - \w+ \[.+\] "[A-Z]+ [a-zA-Z0-9\/]* (\w+\/[0-9\.]+).*$'
    regex_status_code = '^(?:[0-9]{1,3}\.){3}[0-9]{1,3} - \w+ \[.+\] "[A-Z]+ [a-zA-Z0-9\/]* \w+\/[0-9\.]+" (\d+) .*$'
    regex_request_size = '^(?:[0-9]{1,3}\.){3}[0-9]{1,3} - \w+ \[.+\] "[A-Z]+ [a-zA-Z0-9\/]* \w+\/[0-9\.]+" \d+ (\d+).*$'
    regex_referrer = '^(?:[0-9]{1,3}\.){3}[0-9]{1,3} - \w+ \[.+\] "[A-Z]+ [a-zA-Z0-9\/]* \w+\/[0-9\.]+" \d+ \d+ "([-.\w]+)".*$'
    regex_user_agent = '^(?:[0-9]{1,3}\.){3}[0-9]{1,3} - \w+ \[.+\] "[A-Z]+ [a-zA-Z0-9\/]* \w+\/[0-9\.]+" \d+ \d+ "[-.\w]+" "(.*)"$'

    pandas_df[ip] = pandas_df[message].str.extract(regex_ip, expand=True)
    pandas_df[username] = pandas_df[message].str.extract(regex_username, expand=True)
    pandas_df[log_time] = pandas_df[message].str.extract(regex_log_time, expand=True)
    pandas_df[http_request] = pandas_df[message].str.extract(
        regex_http_request, expand=True
    )
    pandas_df[endpoint] = pandas_df[message].str.extract(regex_endpoint, expand=True)
    pandas_df[http_version] = pandas_df[message].str.extract(
        regex_http_version, expand=True
    )
    pandas_df[status_code] = pandas_df[message].str.extract(
        regex_status_code, expand=True
    )
    pandas_df[request_size] = pandas_df[message].str.extract(
        regex_request_size, expand=True
    )
    pandas_df[referrer] = pandas_df[message].str.extract(regex_referrer, expand=True)
    pandas_df[user_agent] = pandas_df[message].str.extract(
        regex_user_agent, expand=True
    )
    pandas_df = pandas_df.drop(columns=[message])
    pandas_df = pandas_df.dropna(thresh=5)

    spark = SparkSession.builder.master("local[1]").appName("ada").getOrCreate()

    fin_sp_df = spark.createDataFrame(pandas_df)
    output_frame = DynamicFrame.fromDF(fin_sp_df, glue_context, "output_frame")

    return [output_frame]
