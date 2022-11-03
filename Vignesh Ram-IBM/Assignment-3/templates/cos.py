from flask import Flask, redirect, url_for, render_template, request
import ibm_boto3
from ibm_botocore.client import Config, ClientError

COS_ENDPOINT = "https://s3.jp-tok.cloud-object-storage.appdomain.cloud"
COS_API_KEY_ID = "wdIP-Aa536jlvnQUSF_WIwotjo3XA_4_bOSHVmM8s9Nl"
COS_INSTANCE_CRN = "crn:v1:bluemix:public:cloud-object-storage:global:a/c5ba1788996742a1926acd04ffb7be3d:5cf71ca3-172c-4ca0-b073-d52788a0a9ff:bucket:cricketers"
COS_BUCKET_LOCATION = "jp-tok-standard"

# Create resource https://s3.ap.cloud-object-storage.appdomain.cloud
cos = ibm_boto3.resource("s3",
                         ibm_api_key_id=COS_API_KEY_ID,
                         ibm_service_instance_id=COS_INSTANCE_CRN,
                         config=Config(signature_version="oauth"),
                         endpoint_url=COS_ENDPOINT)

app = Flask(__name__)


def get_buckets():
    print("Retrieving list of buckets")
    try:
        buckets = cos.buckets.all()
        for bucket in buckets:
            print("Bucket Name: {0}".format(bucket.name))
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to retrieve list buckets: {0}".format(e))


def create_bucket(bucket_name):
    print("Creating new bucket: {0}".format(bucket_name))
    try:
        cos.Bucket(bucket_name).create(
            CreateBucketConfiguration={
                "LocationConstraint": COS_BUCKET_LOCATION
            })
        print("Bucket: {0} created!".format(bucket_name))
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to create bucket: {0}".format(e))


create_bucket("cricketers")
get_buckets()

if __name__ == '_main_':
    app.run(host='0.0.0.0', port=8080, debug=True)
