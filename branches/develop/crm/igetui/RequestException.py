class RequestException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

    def getRequestId(self):
        return self.value
