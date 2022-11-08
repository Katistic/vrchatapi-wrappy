from vrchatapi import Configuration, ApiClient as _ApiClient
from http.cookiejar import LWPCookieJar
from io import IOBase

from exceptions import NotVRChatURLException

class ApiClient(_ApiClient):
    def save_cookies(self, filename: str):
        """Load current sessions cookies

        Args:
            filename (str): Path to save cookies to
        """
        
        cookie_jar = LWPCookieJar(filename=filename)
        
        for cookie in self.rest_client.cookie_jar:
            cookie_jar.set_cookie(cookie)
            
        cookie_jar.save()
        
    def load_cookies(self, filename: str):
        """Load current sessions cookies

        Args:
            filename (str): Path to load cookies from
        """
        
        cookie_jar = LWPCookieJar(filename=filename)
        cookie_jar.load()
        
        for cookie in cookie_jar:
            self.rest_client.cookie_jar.set_cookie(cookie)
            
    def save_file(self, url: str, filename: str):
        """Save current sessions cookies

        Args:
            url (str): URL of the file to save, must start with `https://cloud.vrchat.api`
            filename (str): Path to save file
        """
        
        if not url.startswith("https://cloud.vrchat.api") and "/api/1/" not in url:
            raise NotVRChatURLException(404, "URL '%s' is not a valid vrchat.api url", None)
        
        url = url.split("/api/1")[0]
        resp = self.call_api(url, "GET", _preload_content=True, response_type=(IOBase,))
        
        with open(filename, "wb+") as file:
            file.write(resp[0].read())
            
    ## Little function for maintaining simplicity
    def set_login_credentials(self, username: str, password: str):
        """Set login credentials
        
        Simplifies pre-making a Configuration object and passing it in on ApiClient instantiation
        
        Args:
            username (str): Username of VRChat user
            password (str): Password of VRChat user
        """
        
        self.configuration = Configuration(username=username, password=password)