from vrchatapi.exceptions import ApiException

class NotVRChatURLException(ApiException):
    def __init__(self, status=None, reason=None, http_resp=None):
        super().__init__(status, reason, http_resp)