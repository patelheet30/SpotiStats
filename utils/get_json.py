from utils.models import User


def get_json(dict_of_json_data):
    info_needed_for_user = {}
    for json_data in dict_of_json_data:
        if json_data in ['Follow.json', 'MyData/Follow.json']:
            info_needed_for_user["followers"] = dict_of_json_data[json_data]['followerCount']
            info_needed_for_user["following"] = dict_of_json_data[json_data]['followingUsersCount']
        if json_data in ['Userdata.json', 'MyData/Userdata.json']:
            info_needed_for_user["username"] = dict_of_json_data[json_data]['username']
            info_needed_for_user["email"] = dict_of_json_data[json_data]['email']
            info_needed_for_user["country"] = dict_of_json_data[json_data]['country']
            info_needed_for_user["birth_date"] = dict_of_json_data[json_data]['birthdate']
            info_needed_for_user["creation_date"] = dict_of_json_data[json_data]['creationTime']
            info_needed_for_user["gender"] = dict_of_json_data[json_data]['gender']

    return info_needed_for_user


