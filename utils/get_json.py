from utils.models import Song
from itertools import chain


def get_json(dict_of_json_data):
    info_needed_for_user = { }
    potential_song_lists = { }
    all_songs_in_parts = []
    all_songs_in_one = []
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
        else:
            if json_data.startswith('StreamingHistory'):
                continue
            elif json_data.startswith('MyData/StreamingHistory'):
                continue
            elif json_data in ['Follow.json'
                               'YourLibrary.json',
                               'Identity.json',
                               'Identifiers.json',
                               'Inferences.json',
                               'Marquee.json',
                               'Payments.json',
                               'Playlist1.json',
                               'PlaylistInABottle.json',
                               'SearchQueries.json',
                               'MyData/Follow.json',
                               'MyData/YourLibrary.json',
                               'MyData/Identity.json',
                               'MyData/Identifiers.json',
                               'MyData/Inferences.json',
                               'MyData/Marquee.json',
                               'MyData/Payments.json',
                               'MyData/Playlist1.json',
                               'MyData/PlaylistInABottle.json',
                               'MyData/SearchQueries.json'
                               ]:
                continue
            else:
                potential_song_lists[json_data] = dict_of_json_data[json_data]

    all_songs_in_parts = [
        create_song_classes(song)
        for song in potential_song_lists.values()
    ]
    all_songs_in_one = list(chain.from_iterable(all_songs_in_parts))

    print(len(all_songs_in_one))
    return info_needed_for_user, all_songs_in_one


def create_song_classes(songs) -> list[Song]:
    song_classes = []
    for song in songs:
        if song['episode_name'] or not song['spotify_track_uri']:
            continue
        else:
            song_classes.append(
                    Song(
                            name=song['master_metadata_track_name'],
                            artist=song['master_metadata_album_artist_name'],
                            album=song['master_metadata_album_album_name'],
                            uri=song['spotify_track_uri'],
                            duration=song['ms_played'],
                            time=song['ts']
                    )
            )
    return song_classes
