from typing import Any
from pincer import command as _command

from magpie.config import Config


def command(*args, **kwargs) -> Any:
    return _command(*args, guild=int(Config.get_env("GUILD")), **kwargs)
