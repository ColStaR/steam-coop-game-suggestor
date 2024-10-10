import requests
import json

def get_api_key_from_file():
    try:
        with open("info/steam_api_key.txt", 'r') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        return f"The file '{filename}' was not found."
    except Exception as e:
        return f"An error occurred: {str(e)}"

def get_steam_id_from_file():
    try:
        with open("info/steam_id.txt", 'r') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        return f"The file '{filename}' was not found."
    except Exception as e:
        return f"An error occurred: {str(e)}"

def get_player_game_list(api_key, steam_id):
    list_of_game_appid = []
    url = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={api_key}&steamid={steam_id}"
    print(url)
    response = requests.get(url)
    data = response.json()

    for game_info in data["response"]["games"]:
        list_of_game_appid.append(game_info["appid"])
    return list_of_game_appid

# Note: steam_id user must have profile set to public.
def get_friends_list(api_key, steam_id):
    list_of_friend_steamid = []
    url = f"http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={api_key}&steamid={steam_friend}&relationship=friend"
    print(url)
    response = requests.get(url)
    print(response)
    data = response.json()
    for friend_info in data["friendslist"]["friends"]:
        list_of_friend_steamid.append(friend_info["steamid"])
    return list_of_friend_steamid

def get_shared_games(api_key, list_of_steamid):
    list_of_games_per_user = []

    for steam_id in list_of_steamid:
        game_list = get_player_game_list(api_key, steam_id)
        game_list_set = set(game_list)
        list_of_games_per_user.append(game_list_set)
    
    shared_games_set = list_of_games_per_user[0]

    for game_set in list_of_games_per_user[1:]:
        shared_games_set = shared_games_set.intersection(game_set)

    return list(shared_games_set)
    

api_key = get_api_key_from_file()
steam_id = get_steam_id_from_file()

example_steamid = 76561198322674805

print(get_shared_games(api_key, [steam_id, example_steamid]))



