# SPDX-License-Identifier: MIT


# Imports.
import asyncio
from typing import List

import disnake
from disnake.ext import commands
from disnake.interactions import ApplicationCommandInteraction

from core.chain import keychain
from core.ui import TypicalEmbed


# Set up a custom class for core functionality.
class IgKnite(commands.AutoShardedInteractionBot):
    """
    A subclassed version of `commands.AutoShardedInteractionBot`.\n
    Basically works as the core class for all-things IgKnite!
    """

    def __init__(self, *args, initial_extensions: List[str], **kwargs) -> None:
        super().__init__(*args, **kwargs)

        for extension in initial_extensions:
            self.load_extension(extension)

    async def _update_presence(self) -> None:
        """
        Updates the rich presence of IgKnite.
        """

        await self.change_presence(
            status=disnake.Status.dnd,
            activity=disnake.Activity(
                type=disnake.ActivityType.listening,
                name=f'slashes inside {len(self.guilds)} server(s)!',
            ),
        )

    async def on_connect(self) -> None:
        print(f'\nConnected to Discord as {self.user}.')

    async def on_ready(self) -> None:
        print(f'Inside {len(self.guilds)} server(s) with {self.shard_count} shard(s) active.')
        await self._update_presence()

    async def on_guild_join(self, _: disnake.Guild) -> None:
        await self._update_presence()

    async def on_guild_remove(self, _: disnake.Guild) -> None:
        await self._update_presence()

    async def on_message(self, message: disnake.Message) -> None:
        if message.author == self.user:
            return

    # 23.02.2024 - The end.
    async def on_application_command(self, interaction: ApplicationCommandInteraction) -> None:
        embed = TypicalEmbed(inter=interaction, title='🌇 Sunsetting IgKnite.').add_field(
            name='Why?',
            value="It might sound unexpectedly straightforward, but we've taken this decision so that we can take the experience we've gained while building this awesome project and apply it to something that'd carry on it's legacy. It has been a very nice journey, and hopefully you'll stay around for updates. Something's on the way!",
        )
        await interaction.channel.send(embed=embed)

    async def on_message_delete(self, message: disnake.Message) -> None:
        keychain.snipeables.append(message)
        await asyncio.sleep(25)
        keychain.snipeables.remove(message)
