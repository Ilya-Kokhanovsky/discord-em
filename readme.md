
[![Stand With Ukraine](https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/banner2-direct.svg)](https://vshymanskyy.github.io/StandWithUkraine/)


# DiscordEM 0.0.1 (alpha)
**DiscordEM** is a simple asynchronous parser written in Python, it uses a direct connection via sockets, so it is very fast and does not stop the main thread, which allows you to handle a large number of requests at the same time.

[![Made in Ukraine](https://img.shields.io/badge/made_in-ukraine-ffd700.svg?labelColor=0057b7)](https://stand-with-ukraine.pp.ua)
[![StandWithUkraine](https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/badges/StandWithUkraine.svg)](https://github.com/vshymanskyy/StandWithUkraine/blob/main/docs/README.md)

## Warning

This code is intended for educational and purely personal use, and this code is still under development, so it may contain bugs or errors that can lead to account blocking, use it at your own risk.


## Installing

All dependencies are recommended to be installed only in a virtual environment, more details: [Link](https://docs.python.org/3/library/venv.html)

Clone the project

```bash
  git clone https://github.com/Ilya-Kokhanovsky/discord-em.git
```

Enter the virtual environment and install the necessary dependencies

```bash
  pip install -r requirements.txt
```

## Usage/Examples

The `example.py` file already contains this example of using the code.

```python
from discord_em import DiscordParser
import asyncio

token: str = "YOUR_DISCORD_TOKEN"
guild_id: int = 727195657261285477
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
```

*The result of the fetch_members function is a numeric list containing user IDs, for example:*

```
    [419842539030446082, 474248047929589772, 588648449562509315, 336972836344168449]
```
## License

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)

[(MIT)](https://choosealicense.com/licenses/mit/)
We invite you to cooperate and improve this parser together!

