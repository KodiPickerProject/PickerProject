import json
import time
import random
import os
import xbmc
import xbmcvfs
from src import json_utils

default_config = {
    "name": "Default",
    "watch-status": "any",
    "media-type": "movie",
    "genres": [
        "Action", "Adventure", "Animation", "Comedy", "Crime", "Drama", "Fantasy",
        "Horror", "Mystery", "Romance", "Sci-Fi", "Western", "Thriller", "Documentary",
        "History", "Sport"
    ],
    "media-length": ["0", "100000"],
    "release-year": ["0", "100000"],
    "ratings": ["0", "10"],
    "parental-advisory": [
        "Rated G", "Rated PG", "Rated PG-13", "Rated R", "Rated NC-17", "Rated TV-Y",
        "Rated TV-Y7", "Rated TV-G", "Rated TV-PG", "Rated TV-14", "Rated TV-MA"
    ]
}

config_path = xbmcvfs.translatePath("special://home/addons/script.quick.picker/UserData/current_config.json")
config_file = open(config_path, "r")
config_data = json.load(config_file)

watch_status = None
media_type = None
genres = None
media_length = None
release_year = None 
ratings = None
parental_advisory = None

try:
    watch_status = config_data["watch-status"]
    media_type = config_data["media-type"]
    genres = config_data["genres"]
    media_length = config_data["media-length"]
    release_year = config_data["release-year"]
    ratings = config_data["ratings"]
    parental_advisory = config_data["parental-advisory"]
except:
    watch_status = default_config["watch-status"]
    media_type = default_config["media-type"]
    genres = default_config["genres"]
    media_length = default_config["media-length"]
    release_year = default_config["release-year"]
    ratings = default_config["ratings"]
    parental_advisory = default_config["parental-advisory"]

def update_config():
    global watch_status, media_type, genres, media_length, release_year, ratings, parental_advisory
    with open(config_path, "r") as config_file:
        config_data = json.load(config_file)
        watch_status = config_data["watch-status"]
        media_type = config_data["media-type"]
        genres = config_data["genres"]
        media_length = config_data["media-length"]
        release_year = config_data["release-year"]
        ratings = config_data["ratings"]
        parental_advisory = config_data["parental-advisory"]
    
def update_config_to_default():
    global watch_status, media_type, genres, media_length, release_year, ratings, parental_advisory
    watch_status = default_config["watch-status"]
    media_type = default_config["media-type"]
    genres = default_config["genres"]
    media_length = default_config["media-length"]
    release_year = default_config["release-year"]
    ratings = default_config["ratings"]
    parental_advisory = default_config["parental-advisory"]

def get_filtered_media():
    global watch_status, media_type, genres, media_length, release_year, ratings, parental_advisory
    if json_utils.does_current_config_exist():
        update_config()
    else:
        update_config_to_default()
    request = {
        "jsonrpc": "2.0",
        "method": "VideoLibrary.GetMovies",
        "params": {
            "filter": {
                "and": [
                    {
                        "field": "genre",
                        "operator": "contains",
                        "value": genres
                    },
                    {
                        "field": "year",
                        "operator": "between",
                        "value": [release_year[0], release_year[1]]
                    },
                    {
                        "field": "rating",
                        "operator": "between",
                        "value": [ratings[0], ratings[1]]
                    }
                ]
            },
            "properties": [
                "file",
                "genre",
                "playcount",
                "runtime",
                "year",
                "rating",
                "mpaa"
            ]
        },
        "id": "libMedia"
    }

    if media_type == "tvshow":
        request["method"] = "VideoLibrary.GetTVShows"

    response_json = xbmc.executeJSONRPC(json.dumps(request))
    response = json.loads(response_json)
    response["result"][media_type + "s"] = [item for item in response["result"].get(media_type + "s", []) if item.get("mpaa") in parental_advisory]
    response["result"][media_type + "s"] = [item for item in response["result"].get(media_type + "s", []) if float(media_length[0]) <= float(item.get("runtime")) / 60.0 <= float(media_length[1])]
    response["result"][media_type + "s"] = [item for item in response.get("result", {}).get(media_type + "s", []) if (watch_status == "unwatched" and item.get("playcount", 0) == 0) or (watch_status == "watched" and item.get("playcount", 0) > 0) or (watch_status == "any")]
    return json.dumps(response).encode("utf-8")


def get_movies_arrs():
    repo = json.loads(get_filtered_media())["result"]["movies"]
    media_list = []
    for entry in repo:
        media = {}
        media["title"] = entry["label"]
        media["path"] = entry["file"]
        media_list.append(media)
    return media_list

# Chooses random media from filtered library
def randomize_media():
    repo = json.loads(get_filtered_media())["result"][media_type + "s"]
    media_list = []
    for entry in repo:
        media = {}
        media["title"] = entry["label"]
        media["path"] = entry["file"]
        media_list.append(media)
    randIndex = random.randint(0, len(media_list) - 1)
    randomMedia = media_list[randIndex]
    if media_type == "tvshow":
        randomMedia["path"] = get_random_episode(randomMedia["path"])
    return randomMedia

# Chooses a random episode of a tv show that the user has downloaded
def get_random_episode(path):
     # List all files recursively in the folder
    all_files = [os.path.join(root, file) for root, dirs, files in os.walk(path) for file in files]

    if all_files:
        # Choose a random file from the list
        random_file = random.choice(all_files)
        while random_file.lower().endswith("ds_store"):
            random_file = random.choice(all_files)
        return random_file
    else:
        return None

def play_media(i):
    xbmc.log("media path: " + i, xbmc.LOGINFO)
    xbmc.Player().play(i)
