#----------------------------------------------------------
# Import
#----------------------------------------------------------
# Standard library
import logging
import os

# Additional library
import discord

# Original library
import lib.log

# Other module
import env


#----------------------------------------------------------
# Init
#----------------------------------------------------------
# Get logger
lib.log.init(env.DEBUG)
_logger = lib.log.get_logger(__name__)

# Get discord instance
_intents = discord.Intents.default()
_client = discord.Client(intents=_intents)

@_client.event
async def on_error(event, *args, **kwargs):
    import traceback
    error = traceback.format_exc()
    print(f"Error occurred: {error}")

_OVERWRITE_PERM = {
    'priority_speaker': True,   # 有線スピーカー
    'manage_messages': True,    # メッセージの管理
    'connect': True,  # チャンネルへの接続を許可
    'speak': True,  # 音声の送信を許可
    'mute_members': True,   # メンバーのミュート
    'deafen_members': True, # メンバーのディスコードミュート
    'move_members': True,   # メンバーの移動
    'use_voice_activation': True,  # 音声アクティビティの使用を許可
    'manage_channels': True,  # チャンネルの管理を許可
}

_created_vc = list();


#----------------------------------------------------------
# Events
#----------------------------------------------------------
@_client.event
async def on_voice_state_update(member, before, after):
    if member.guild.id == env.GUILD_ID and (before.channel != after.channel):
        if before.channel is not None:
            _logger.debug(f'Leave: member={member.name} channel={before.channel.name}')
            for channel in _created_vc:
                if len(channel.members) == 0:
                    await channel.delete()
                    _created_vc.remove(channel)
                    _logger.info(f'Delete "{channel.name}" ({channel.id})')

        if after.channel is not None:   # VCにJoin
            if after.channel.id == env.GENERATOR_VC_ID:
                _logger.info(f'Join {member.name}({member.id}) to generator channel')

                args = {
                    'name': f'{member.name}\'s {env.VC_NAME}',
                    'category': after.channel.category,
                }
                new_channel = await member.guild.create_voice_channel(**args)
                _created_vc.append(new_channel)

                overwrites = dict()
                for overwrites_role, perm in after.channel.overwrites.items():
                    overwrites[overwrites_role] = perm
                overwrites[member] = discord.PermissionOverwrite(**_OVERWRITE_PERM)
                await new_channel.edit(overwrites=overwrites)

                _logger.info(f'Created "{new_channel.name}"')

                await member.move_to(new_channel)
                _logger.info(f'Move {member.name}({member.id}) to {new_channel.name}({new_channel.id}')


#----------------------------------------------------------
# Main
#----------------------------------------------------------
def main():
    _client.run(env.TOKEN, log_handler=logging.NullHandler())

if __name__ == '__main__':
    main()
