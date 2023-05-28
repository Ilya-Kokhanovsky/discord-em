from websockets.client import WebSocketClientProtocol
from .utils import *
import json
import asyncio

class WSS:

    @staticmethod
    async def identify(ws: WebSocketClientProtocol, token: str, device: DeviceProperties) -> dict:
        try:

            await ws.send(
                json.dumps(
                    {
                        "op": 2,
                        "d": {
                            "token": token,
                            "compress": True,
                            "intents": 1,
                            "large_threshold": 250,
                            "shard": [0, 1],
                            "presence":{
                                "status":"dnd",
                                "since":0,
                                "activities":[],
                                "afk": False
                            },
                            "properties": {
                                "os": device.os,
                                "device": "" ,
                                "system_locale": "en-US",
                                "browser": device.browser,
                                "browser_user_agent": device.ua,
                                "release_channel": "stable",
                            },
                        }
                    }
                )
            )
            
        except Exception:
            pass

    async def get_heartbeat_interval(ws: WebSocketClientProtocol) -> int:
        try:
            heartbeat_data = await NET.receive_json_response(ws)
            heartbeat_interval = heartbeat_data['d']['heartbeat_interval']
            return heartbeat_interval
        except Exception:
            pass

    async def send_activity_emulate(ws: WebSocketClientProtocol):
        try:
            await ws.send(
                json.dumps(
                    {
                        "op": 4,
                        "d": {
                            "guild_id": None,
                            "channel_id": None,
                            "self_mute": True,
                            "self_deaf": False,
                            "self_video": False,
                        }
                    }
                )
            )
        except Exception:
            pass

    async def send_first_fetch(ws: WebSocketClientProtocol, guild_id: int, channel_id: int):
        try:
            await ws.send(
                json.dumps(
                    {
                        "op": 14,
                        "d": {
                            "guild_id": guild_id,
                            "typing": True,
                            "threads": True,
                            "activities": True,
                            "members": [],
                            "channels": {channel_id: [[0, 99]]},
                            "thread_member_lists": [],
                        }
                    }
                )
            )
        except Exception:
            pass
    
    async def send_many_fetches(ws: WebSocketClientProtocol, guild_id: int, channel_id: int, max_presences: int = 100):
        try:

            algorithms = await Chunk.get_range_chunks(max_presences)
            for sequence in algorithms:
                try:
                    await ws.send(
                        json.dumps(
                            {
                                "op": 14,
                                "d": {
                                    "guild_id": guild_id,
                                    "channels": {channel_id: sequence},
                                }
                            }
                        )
                    )
                except Exception:
                    pass
                    
                await asyncio.sleep(1)

        except Exception:
            pass