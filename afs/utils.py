import json
import requests
import logging
# import botocore.session
from botocore.client import Config
import boto3
import hashlib

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5

_logger = logging.getLogger(__name__)


class InvalidStatusCode(Exception):
    def __init__(self, status_code, body):
        self.status_code = status_code
        self.body = body

    def __str__(self):
        if self.body is None:
            return "%d" % self.status_code
        elif type(self.body) == str:
            return "%d : %s" % (self.status_code, self.body)
        else:
            return "%d : %s" % (self.status_code, json.dumps(self.body))


def _check_response(response):
    if int(response.status_code / 100) == 2:
        return response
    else:
        try:
            body = response.json()
        except Exception:
            body = response.text
        raise InvalidStatusCode(response.status_code, body)


def urljoin(*args, extra_paths):
    url = "/".join(v[:-1] if v.endswith("/") else v for v in args)
    if len(extra_paths) > 0:
        url = url + "/" + "/".join(extra_paths)
    return url


def upload_file_to_blob(
    blob_endpoint, blob_accessKey, blob_secretKey, bucket_name, key, filename
):
    try:
        blob_client = boto3.client(
            "s3",
            endpoint_url=blob_endpoint,
            aws_secret_access_key=blob_secretKey,
            aws_access_key_id=blob_accessKey,
            verify=False,
            config=Config(signature_version="s3"),
        )
    except Exception as e:
        raise ConnectionError("Connect to blob {} error, exception: {}".format(blob_endpoint, e))

    retry = 0
    while retry < 3:
        try:
            with open(filename, 'rb') as data:
                blob_client.upload_fileobj(Fileobj=data, Bucket=bucket_name, Key=key)
            # Upload file success
            break
        except Exception as e:
            print(
                ConnectionError(
                    "[ConnectionError] Put object error {} time, exeception: {}".format(retry, e)
                )
            )
            retry += 1
            if retry == 3:
                raise ConnectionError(
                    "[ConnectionError] Put object error after retry 3 times."
                )

    resp_get = blob_client.list_objects(Bucket=bucket_name, Prefix=key)
    if not resp_get or resp_get["ResponseMetadata"]["HTTPStatusCode"] != 200:
        raise ConnectionError("List blob key has some error, check response {}".format(resp_get))

    object_size = resp_get["Contents"][0]["Size"]
    return object_size


def dowload_file_from_blob(
    blob_endpoint, blob_accessKey, blob_secretKey, bucket_name, key, filename
):
    try:
        blob_client = boto3.client(
            "s3",
            endpoint_url=blob_endpoint,
            aws_secret_access_key=blob_secretKey,
            aws_access_key_id=blob_accessKey,
            verify=False,
            config=Config(signature_version="s3"),
        )
    except Exception as e:
        raise RuntimeError("Write download file error. Exception: {}".format(e))

    retry = 0
    while retry < 3:
        try:
            blob_client.download_file(bucket_name, key, filename)
            # Download file success
            break
        except Exception as e:
            print(
                ConnectionError(
                    "[ConnectionError] Put object error {} time, exeception: {}".format(retry, e)
                )
            )
            retry += 1
            if retry == 3:
                raise ConnectionError(
                    "[ConnectionError] Put object error after retry 3 times."
                )


def encrypt(
    data, key
):
    rsakey = RSA.importKey(key)
    cipher = Cipher_PKCS1_v1_5.new(rsakey)
    length = 100 

    res = []
    for i in range(0, len(data), length):
        res.append(cipher.encrypt(data[i:i+length]))

    encrypted = b''.join(res)
    return encrypted

def decrypt(
    data, key
):
    rsakey = RSA.importKey(key)
    decipher = Cipher_PKCS1_v1_5.new(rsakey)
    length = 128

    res = []
    for i in range(0, len(data), length):
        res.append(decipher.decrypt(data[i:i+length], None))

    model = b''.join(res)

    return model