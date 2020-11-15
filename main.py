import argparse
from pathlib import Path
from shutil import copyfile
from uuid import UUID

from mcuuid.api import GetPlayerData
from mcuuid.tools import is_valid_minecraft_username


def retrieve_user_uuids(old_username: str, new_username: str) -> (str, str):
    old_user_data = GetPlayerData(old_username)
    new_user_data = GetPlayerData(new_username)

    if not old_user_data.valid:
        # bad old user uuid
        pass
    elif not new_user_data.valid:
        # bad new user uuid
        pass

    return UUID(old_user_data.uuid), UUID(new_user_data.uuid)


def validate_usernames_syntax(old_username: str, new_username: str) -> bool:
    valid_usernames: bool = True

    if not is_valid_minecraft_username(old_username):
        print(f'Old username {old_username} is invalid!')
        valid_usernames = False

    if not is_valid_minecraft_username(new_username):
        print(f'New username {new_username} is invalid!')
        valid_usernames = False

    return valid_usernames


def main():
    parser = argparse.ArgumentParser(description='Witchcraft & Wizardry: Change Minecraft account')
    parser.add_argument('-o', '--old-username', help='Old username', required=True)
    parser.add_argument('-n', '--new-username', help='New username', required=True)
    parser.add_argument('-w', '--world-path', help='Full path to the world folder', required=True)
    args = vars(parser.parse_args())

    old_username, new_username = args['old_username'], args['new_username']
    world_folder_location = args['world_path']

    if not validate_usernames_syntax(old_username, new_username):
        exit(1)

    old_user_uuid, new_user_uuid = retrieve_user_uuids(old_username, new_username)

    for old_path in Path(world_folder_location).rglob(f'*{old_user_uuid}*'):
        new_path = Path(f'{old_path.parent}\\{new_user_uuid}{old_path.suffix}')
        # Attempt to delete new UUID file if it existed before copy
        new_path.unlink(missing_ok=True)
        # Copy old UUID file into new UUID file
        copyfile(old_path, new_path)
        print(f'Copying {old_path} to {new_path}')

    print('Success!')


if __name__ == '__main__':
    main()
