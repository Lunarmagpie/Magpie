from pincer import Client
from pincer.core import Gateway

from magpie.config import Config
from magpie.utils.command import command

class Bot(Client):

    @Client.event
    async def on_ready(self, shard: Gateway):
        print(f"Shard {shard.shard_key} logged in")

    @command
    async def join(self):
        return "Bot joined the channel"

Bot(token=Config.get_env("TOKEN")).run()
