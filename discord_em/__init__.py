from .https import *
from .wss import *
from .exceptions import *
from .utils import *

import asyncio
import websockets

GATEWAY_URL: str = "wss://gateway.discord.gg/?v=9&encoding=json"

class DiscordParser:
        
    def __init__(self, token: str, guild_id: int, channel_id: int) -> None:
        self.token: str = token
        self.guild_id: int = guild_id
        self.channel_id: int = channel_id
        self.device: DeviceProperties = DeviceProperties()
        self.ready: bool = False
        self.members: list[int] = []
     
    async def fetch_members(self, max_presences: int = 100) -> list:

        if not await HTTP.is_user_exist(self.token, self.device.ua):
            raise InvalidToken
        
        await asyncio.sleep(1)

        if not await HTTP.is_guild_exist(self.token, self.device.ua, self.guild_id):
            raise InvalidGuild
        
        await asyncio.sleep(1)

        if not await HTTP.is_channel_exist(self.token, self.device.ua, self.channel_id):
            raise InvalidChannel
        
        await asyncio.sleep(1)
            
        async with websockets.connect(GATEWAY_URL, user_agent_header=self.device.ua) as ws:
            try:

                await WSS.identify(ws, self.token, self.device)
                heartbeat_interval = await WSS.get_heartbeat_interval(ws)
                await WSS.send_activity_emulate(ws)

                l_event = asyncio.ensure_future( self._loop_event(ws) )
                l_heartbeat = asyncio.ensure_future( self._loop_heartbeat(ws, heartbeat_interval) )

                while not self.ready:
                    await asyncio.sleep(2)
                
                await WSS.send_first_fetch(ws, self.guild_id, self.channel_id)
                await WSS.send_many_fetches(ws, self.guild_id, self.channel_id, max_presences)

                await asyncio.sleep(3)
                
                l_event.cancel()
                l_heartbeat.cancel()

            except Exception:
                pass
            
        return self.members

    async def _loop_heartbeat(self, ws: WebSocketClientProtocol, heartbeat_interval: int):
        try:
            timeout: float = (heartbeat_interval/1000)
            while True:
                await ws.send(
                    json.dumps(
                        {
                            "op": 1,
                            "d": None,
                        }
                    )
                )
                await asyncio.sleep(timeout)
        except Exception:
            pass

    async def _loop_event(self, ws: WebSocketClientProtocol):
        while True:
            event: dict = await NET.receive_json_response(ws)
            if event:
                try:
                    
                    event_type = event['t']
                    event_data = event['d']
                    
                    if 'READY' == event_type:
                        self.ready = True

                    if 'GUILD_MEMBER_LIST_UPDATE' == event_type:
                        ops = event_data['ops']
                        for op_data in ops:
                            operator = op_data['op']
                            if operator == "SYNC":
                                members_list = op_data['items']
                                for i in range( 1, len(members_list) ):
                                    member = members_list[i]
                                    if 'member' in member:
                                        user = member['member']['user']
                                        user_id = int(user['id'])
                                        is_bot = user['bot']
                                        if not is_bot:
                                            if not user_id in self.members:
                                                self.members.append(user_id)

                            if operator in ["INSERT","UPDATE"]:
                                user = op_data['item']['member']['user']
                                is_bot = user['bot']
                                if not is_bot:
                                    user_id = int(user['id'])
                                    if not user_id in self.members:
                                        self.members.append(user_id)

                except Exception:
                    pass