from vrchatapi.exceptions import ApiException

class WebsocketEventError(Exception):
    """Base Websocket Event Error"""
    pass

class NotVRChatURLException(ApiException):
    def __init__(self, status=None, reason=None, http_resp=None):
        super().__init__(status, reason, http_resp)
        
class InvalidEvent(ApiException):
    def __init__(self, event_name):
        super().__init__("Event does not exist: '%s'" % event_name)