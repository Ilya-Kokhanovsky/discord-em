from discord_em import DiscordParser
import asyncio

token: str = "YOUR_DISCORD_TOKEN"
guild_id: int = 727195657261285814
channel_id: int = 727202600520384552
max_presences: int = 100

# We create a parser object specifically for parsing data, such as discord server members.
parser = DiscordParser(token, guild_id, channel_id)

async def main():

    members: list[int] = await parser.fetch_members(max_presences)
    print(f"Total users parsed: {len(members)}")
    print(f"Parameters for parsing: guild_id[{guild_id}], channel_id[{channel_id}]")

if __name__ == "__main__":
    asyncio.run(main())