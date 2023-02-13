import asyncio
import threading

class BlockingAsync:
    def __init__(self, sync_func, *args, **kwargs):
        self.sync_func = sync_func
        
        self.thread = threading.Thread(target=self._task, args=args, kwargs=kwargs)
        self.thread.daemon = True
        self.thread.start()
        
        self.result = None
        
    def _task(self, *args, **kwargs):
        self.result = self.sync_func(*args, **kwargs)
        
    async def _task_wrap(self):
        while self.thread.is_alive():
            await asyncio.sleep(0)
            
        return self.result
        
    @staticmethod
    def wrap(sync_funcs, *args, loop=None, **kwargs):
        if loop is None:
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                
        wrapper = BlockingAsync(sync_funcs, *args, **kwargs)
        return loop.create_task(wrapper._task_wrap())