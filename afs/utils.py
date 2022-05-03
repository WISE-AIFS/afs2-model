import sys
import time
import json
import requests
import logging
import boto3
import hashlib
import threading
from botocore.client import Config
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
                    "[ConnectionError] Put object error {} time, exception: {}".format(retry, e)
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
            progress = ProgressPercentage(blob_client, bucket_name, key)
            blob_client.download_file(
                bucket_name, 
                key, 
                filename, 
                Callback=progress)
            # Download file success
            break
        except Exception as e:
            print("[ConnectionError] Get object error {} time, exception: {}".format(retry, e))
            if retry == 3:
                raise ConnectionError(
                    "[ConnectionError] Get object error after retry 3 times."
                )
            retry += 1
            time.sleep(1)

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

    if any(response is None for response in res):
        raise ValueError('decrypt_key is invalid.')

    model = b''.join(res)

    return model

class ProgressPercentage(object):
    ''' Progress Class
    Class for calculating and displaying download progress
    '''
    def __init__(self, client, bucket, filename):
        ''' Initialize
        initialize with: file name, file size and lock.
        Set seen_so_far to 0. Set progress bar length
        '''
        self._filename = filename
        self._size = client.head_object(Bucket=bucket, Key=filename)['ContentLength']
        self._seen_so_far = 0
        self._lock = threading.Lock()
        self.prog_bar_len = 80

    def __call__(self, bytes_amount):
        ''' Call
        When called, increments seen_so_far by bytes_amount,
        calculates percentage of seen_so_far/total file size 
        and prints progress bar.
        '''
        # To simplify we'll assume this is hooked up to a single filename.
        with self._lock:
            self._seen_so_far += bytes_amount
            ratio = round((float(self._seen_so_far) / float(self._size)) * (self.prog_bar_len - 6), 1)
            current_length = int(round(ratio))

            percentage = round(100 * ratio / (self.prog_bar_len - 6), 1)

            bars = '+' * current_length
            output = bars + ' ' * (self.prog_bar_len - current_length - len(str(percentage)) - 1) + str(percentage) + '%'

            if self._seen_so_far != self._size:
                sys.stdout.write(output + '\r')
            else:
                sys.stdout.write(output + '\n')
            sys.stdout.flush()
            