import json


class MockResponse(object):
    def __init__(self, url=None, text=None, headers={}, status_code=200):
        self.url = url
        self.text = text
        self.headers = headers
        self.status_code = status_code

    def json(self):
        # For status 204, it should return {}
        if not self.text:
            return {}
        return json.loads(self.text)
