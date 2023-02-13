import asyncio
import aiohttp
import json

from .async_util import BlockingAsync
from .exceptions import InvalidEvent

class WebsocketHandler:
    valid_event_list = [
        "on_connect",
        "on_disconnect"
    ]
    
    def __init__(self, client, loop=None, user_agent=None):
        self.client = client
        
        self.loop = loop
        self.user_agent = user_agent or "AIOHTTP/%S (vrchatapi-py)"
        self.session = aiohttp.ClientSession(headers={"user-agent": self.user_agent})
        self.ws = None
        
        if loop is None:
            try:
                self.loop = asyncio.get_running_loop()
            except RuntimeError:
                self.loop = asyncio.new_event_loop()
                
    async def _preload(self):
        wrapped_func = BlockingAsync.wrap(self.client.system.get_config)
        config = await wrapped_func()
        
        self.api_key = config.api_key
        self.session.cookie_jar.update_cookies({"apiKey": self.api_key})
        
    async def run_websocket_loop(self):       
        await self._preload()
        
        wrapped_func = BlockingAsync.wrap(self.client.authentication.verify_auth_token)
        auth_token = await wrapped_func()
        
        if auth_token.ok:
            auth_token = auth_token.token
        else:
            # TODO: Use right exception class
            raise Exception("Not logged in!")
        
        self.session.cookie_jar.update_cookies({"auth": auth_token})
        self.ws = await self.session.ws_connect(
            "wss://pipeline.vrchat.cloud/?authToken="+auth_token)
        
        del wrapped_func
        del auth_token
        
        self.loop.create_task(self.on_connect())
        
        async for message in self.ws:
            message = message.json()
            
            switch = {
                
            }
            
            if message["type"] in switch:
                # Load json content and create event handler task
                self.loop.create_task(switch[message["type"]](json.loads(message["content"])))
            
        self.loop.create_task(self.on_disconnect())
                    
    # Public events
    def event(self, func):
        """
        Decorator that sets websocket event hooks
        Example::
        
            @clinet.event
            def on_connect():
                print("Connected to wss pipeline.")
        """
        
        if func.__name__ in WebsocketHandler.valid_event_list:
            setattr(self, func.__name__, func)
            return func
        
        raise InvalidEvent(func.__name__)
    
    async def on_connect(self):
        """Called when connected to vrchat websocket pipeline"""
        pass
    
    async def on_disconnect(self):
        """Called whem disconnected from vrchat websocket pipeline"""
        pass