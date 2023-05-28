from websockets.client import WebSocketClientProtocol
from fake_useragent import UserAgent
import json
import zlib
import httpagentparser

class NET:

    @staticmethod
    async def receive_json_response(ws: WebSocketClientProtocol) -> dict:
        resp = None
        try:
            resp = await ws.recv()
            if type(resp) is str:
                resp = json.loads(resp)
            elif type(resp) is bytes:
                resp = json.loads( zlib.decompress(resp) )
        except Exception:
            pass
        finally:
            return resp

class Chunk:

    @staticmethod
    async def get_range_chunks(search_limit: int) -> list:
        try:

            search_range: list = []
            large_threshold: int = 100
            count_threshold = round(search_limit / large_threshold)
            result = count_threshold if count_threshold > 0 else 1
            
            for i in range(result):
                index = i-1 
                j = [[100*index, 100*index+99]] if len(search_range) > 1 else []
                item = [ *j, [100*i, 100*i+99] ]
                search_range.append(item)
            
            for i in range(1, result):
                item = [0,99]
                search_range[i].insert(0, item)
            
            return search_range
                
        except Exception:
            pass

class DeviceProperties:
    
    def __init__(self) -> None:
        self.ua = UserAgent()
        self._gen_rand_properties()

    def _gen_rand_properties(self):
        try:
            self.ua = self.ua.random
            unique_data = httpagentparser.detect(self.ua)
            self.os = unique_data['os']['name']
            self.browser = unique_data['browser']['name']
        except Exception:
            pass
