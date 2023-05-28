import aiohttp

class HTTP:

    @staticmethod
    async def is_user_exist(token: str, ua: str, timeout: int = 10) -> bool:
        try:
            url: str = "https://discord.com/api/v10/users/@me"
            headers = {
                'Authorization': token,
                'Content-Type': 'application/json',
                'User-Agent': ua,
            }
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, timeout=timeout) as response:
                    status_code: int = response.status
                    return True if status_code == 200 else False
        except Exception:
            return False
    
    @staticmethod
    async def is_guild_exist(token: str, ua: str, guild_id: int, timeout: int = 10) -> bool:
        try:
            url: str = f"https://discord.com/api/v10/guilds/{guild_id}"
            headers = {
                'Authorization': token,
                'Content-Type': 'application/json',
                'User-Agent': ua,
            }
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, timeout=timeout) as response:
                    status_code: int = response.status
                    return True if status_code == 200 else False
        except Exception:
            return False
    
    @staticmethod
    async def is_channel_exist(token: str, ua: str, channel_id: int, loadlimit: int = 5, timeout: int = 10) -> bool:
        try:
            url: str = f"https://discord.com/api/v10/channels/{channel_id}/messages?limit={loadlimit}"
            headers = {
                'Authorization': token,
                'Content-Type': 'application/json',
                'User-Agent': ua,
            }
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, timeout=timeout) as response:
                    status_code: int = response.status
                    return True if status_code == 200 else False
        except Exception:
            return False
