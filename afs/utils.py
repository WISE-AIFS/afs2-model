import json
import requests
import logging
import botocore.session
from botocore.client import Config

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
        config = Config(signature_version="s3")
        session = botocore.session.get_session()
        blob_client = session.create_client(
            "s3",
            region_name="",
            endpoint_url=blob_endpoint,
            aws_access_key_id=blob_accessKey,
            aws_secret_access_key=blob_secretKey,
            config=config,
        )
    except Exception as e:
        raise ConnectionError(f"Connect to blob {blob_endpoint} error, exception: {e}")

    retry = 0
    while retry < 3:
        try:
            resp = blob_client.put_object(
                Bucket=bucket_name, Key=key, Body=open(filename, "rb").read()
            )
        except Exception as e:
            resp = {}
            print(
                ConnectionError(
                    f"[ConnectionError] Put object error {retry} time, exeception: {e}"
                )
            )

        if not resp or resp["ResponseMetadata"]["HTTPStatusCode"] != 200:
            retry = retry + 1
            if retry == 3:
                raise ConnectionError(
                    f"[ConnectionError] Put object error after retry 3 times, check response {resp}"
                )
        else:
            break

    resp_get = blob_client.list_objects(Bucket=bucket_name, Prefix=key)
    if not resp_get or resp["ResponseMetadata"]["HTTPStatusCode"] != 200:
        raise ConnectionError(f"List blob key has some error, check response {resp}")

    object_size = resp_get["Contents"][0]["Size"]
    return object_size
