import json


class MockResponse(object):
    def __init__(self, url=None, headers=None, text=None, status_code=None):
        self.url = url
        self.headers = headers
        self.text = text
        self.status_code = status_code

    def json(self):
        return json.loads(self.text)
