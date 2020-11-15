import argparse
from pathlib import Path
from shutil import copyfile
from uuid import UUID

from mcuuid.api import GetPlayerData
from mcuuid.tools import is_valid_minecraft_username


def validate_user_data(old_user_data: GetPlayerData, new_user_data: GetPlayerData) -> None:
    if not old_user_data.valid:
        print('Old user data is invalid!')
        raise Exception
    elif not new_user_data.valid:
        print('New user data is invalid!')
        raise Exception


def validate_usernames_syntax(old_username: str, new_username: str) -> None:
    if not is_valid_minecraft_username(old_username):
        print(f'Old username {old_username} is invalid!')
        raise Exception
    elif not is_valid_minecraft_username(new_username):
        print(f'New username {new_username} is invalid!')
        raise Exception
    elif old_username == new_username:
        print("Username can't be the same")
        raise Exception


def handle(old_username: str, new_username: str, world_folder_location: str) -> None:
    try:
        validate_usernames_syntax(old_username, new_username)
    except e:
        exit(1)

    old_user_data, new_user_data = GetPlayerData(old_username), GetPlayerData(new_username)

    try:
        validate_user_data(old_user_data, new_user_data)
    except e:
        exit(1)

    old_user_uuid, new_user_uuid = UUID(old_user_data.uuid), UUID(new_user_data.uuid)

    for old_path in Path(world_folder_location).rglob(f'*{old_user_uuid}*'):
        new_path = Path(f'{old_path.parent}\\{new_user_uuid}{old_path.suffix}')
        new_path.unlink(missing_ok=True)
        copyfile(old_path, new_path)
        print(f'Copying {old_path} to {new_path}')

    print('Success!')


def main():
    parser = argparse.ArgumentParser(description='Witchcraft & Wizardry: Change Minecraft account')
    parser.add_argument('-o', '--old-username', help='Old username', required=True)
    parser.add_argument('-n', '--new-username', help='New username', required=True)
    parser.add_argument('-w', '--world-path', help='Full path to the world folder', required=True)
    args = vars(parser.parse_args())
    handle(args['old_username'], args['new_username'], args['world_path'])


if __name__ == '__main__':
    main()
