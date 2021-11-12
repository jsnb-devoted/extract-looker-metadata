""" To be imported to extraction scripts to push data to S3. """

import os
import shutil
import tempfile
import boto3
import json
import logging

BUCKET_NAME = os.getenv("bucket_name")

def load_s3_json(dataframe, local_file_name, output_filename, s3_bucket=BUCKET_NAME):
    """ This saves a json locally to a temporary file and then uploads it """

    temp_dir = tempfile.TemporaryDirectory()
    input_filename = os.path.join(temp_dir.name, local_file_name)
    if isinstance(dataframe, dict) or isinstance(dataframe, list):
        with open(input_filename, 'w') as f:
            json.dump(dataframe, f)
    else:
        print("Invalid instance type; please use only JSON or Dataframe")
        return
    load_s3(s3_bucket, input_filename, output_filename)
    # remove temp directory if done
    if os._exists(temp_dir.name):
        shutil.rmtree(temp_dir.name)

def load_s3(s3_bucket, input_filename, output_filename):

    """ Pushes file to S3. """

    s3_storage = boto3.resource("s3")
    s3_storage.meta.client.upload_file(input_filename, s3_bucket, output_filename)
    logging.info(
        f"COMPLETE: {input_filename} loaded into \
    s3:// {s3_bucket} as {output_filename}"
    )

def read_json(key, s3_bucket=BUCKET_NAME):
    s3_storage = boto3.resource("s3")
    content_object = s3_storage.Object(s3_bucket, key)
    file_content = content_object.get()['Body'].read().decode('utf-8')
    json_content = [json.loads(line) for line in file_content.splitlines()]
    return json_content