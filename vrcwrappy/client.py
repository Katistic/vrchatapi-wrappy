from vrchatapi.api import *

from vrchatapi import Configuration, ApiClient as _ApiClient
from http.cookiejar import LWPCookieJar
from io import IOBase

from .exceptions import NotVRChatURLException
from .authentication_api import AuthenticationApi
from .ws import WebsocketHandler

## We overwrite previous import of AuthenticationApi, and thats ok!

class ApiClient(_ApiClient):
    def __init__(self, configuration=None, header_name=None, header_value=None,
                 cookie=None, pool_threads=1):
        
        super().__init__(configuration=configuration, header_name=header_name,
                         header_value=header_value, cookie=cookie,
                         pool_threads=pool_threads)
        
        # Make import/api usage flow simpler
        # We can do this because it doesn't take much memory
        apis = {
            "authentication": AuthenticationApi,
            "avatars": AvatarsApi,
            "economy": EconomyApi,
            "favorites": FavoritesApi,
            "files": FilesApi,
            "friends": FriendsApi,
            "instances": InstancesApi,
            "invites": InviteApi,
            "notifications": NotificationsApi,
            "permissions": PermissionsApi,
            "player_moderations": PlayermoderationApi,
            "system": SystemApi,
            "users": UsersApi,
            "worlds": WorldsApi
        }
        
        for key, value in apis.items():
            setattr(self, key, value(self))
            
        self._ws = WebsocketHandler(self)
        self.event = self._ws.event
    
    def save_cookies(self, filename: str):
        """Save current session cookies

        Args:
            filename (str): Path to save cookies to
        """
        
        cookie_jar = LWPCookieJar(filename=filename)
        
        for cookie in self.rest_client.cookie_jar:
            cookie_jar.set_cookie(cookie)
            
        cookie_jar.save()
        
    def load_cookies(self, filename: str):
        """Load cached session cookies from file

        Args:
            filename (str): Path to load cookies from
        """
        
        cookie_jar = LWPCookieJar(filename=filename)
        try:
            cookie_jar.load()
        except FileNotFoundError:
            cookie_jar.save()
            return
        
        for cookie in cookie_jar:
            self.rest_client.cookie_jar.set_cookie(cookie)
            
    def save_file(self, url: str, filename: str):
        """Save file from vrchat cdn servers

        Args:
            url (str): URL of the file to save, must start with `https://cloud.vrchat.api`
            filename (str): Path to save file
        """
        
        if not url.startswith("https://cloud.vrchat.api") and "/api/1/" not in url:
            raise NotVRChatURLException(404, "URL '%s' is not a valid vrchat.api url", None)
        
        url = url.split("/api/1")[1]
        resp = self.call_api(url, "GET", _preload_content=False, response_types_map=(IOBase,))
        
        with open(filename, "wb+") as file:
            file.write(resp.data)
            
    ## Little function for maintaining simplicity
    def set_login_credentials(self, username: str, password: str):
        """Set login credentials
        
        Simplifies pre-making a Configuration object and passing it in on ApiClient instantiation
        
        Args:
            username (str): Username of VRChat user
            password (str): Password of VRChat user
        """
        
        self.configuration = Configuration(username=username, password=password)
        
    async def run_websocket_loop(self):
        await self._ws.run_websocket_loop()
        
    ## Event hooks
        
    async def on_connect(self):
        """Called when connected to vrchat websocket pipeline"""
        pass
    
    async def on_disconnect(self):
        """Called whem disconnected from vrchat websocket pipeline"""
        pass