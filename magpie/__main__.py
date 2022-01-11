from typing import Annotated, Dict, Optional, NamedTuple

from pincer import Client
from pincer.commands import ChannelTypes
from pincer.commands.arg_types import Description
from pincer.objects import MessageContext, Channel, ChannelType
from pincer.core import Gateway
from pincer.utils.snowflake import Snowflake

from songbird import ytdl, Queue
from songbird.pincer import Voicebox
from songbird.songbird import YtdlError

from magpie.config import Config
from magpie.utils.command import command


class ChannelVoiceInfo(NamedTuple):
    voice: Voicebox
    queue: Queue


class Bot(Client):

    def __init__(self, token: str):
        self.shard: Optional[Gateway] = None
        self.voice: Dict[Snowflake, ChannelVoiceInfo] = {}

        super().__init__(token)

    @Client.event
    async def on_ready(self, shard: Gateway):
        print(f"Shard {shard.shard_key} logged in")
        self.shard = shard

    @command
    async def join(
        self,
        ctx: MessageContext,
        channel: Annotated[
            Channel,
            Description("The voice channel to join"),
            ChannelTypes(ChannelType.GUILD_VOICE)
        ]
    ):
        if not self.shard or not ctx.guild_id:
            return f"Cannot join {channel.mention}"

        voice = await Voicebox.connect(
            self, self.shard, ctx.guild_id, channel.id
        )
        self.voice[ctx.guild_id] = ChannelVoiceInfo(
            voice=voice,
            queue=Queue(voice)
        )

        return f"I joined {channel.mention}"

    @command
    async def play(
        self,
        ctx: MessageContext,
        url: Annotated[
            str,
            Description("A youtube video to play")
        ]
    ):
        await ctx.ack()

        if not ctx.guild_id:
            return "This command can only be run in a guild"

        try:
            source = await ytdl(url)
        except YtdlError:
            return f"Could not find song ({url})"

        queue = self.voice[ctx.guild_id].queue

        queue.append(source)

        if len(queue) == 1:
            return "Playing song"
        return "Added song to queue"


Bot(token=Config.get_env("TOKEN")).run()
