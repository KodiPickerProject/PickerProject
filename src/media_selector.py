import json
import xbmc

def play_media(mood_y_n):
    if (mood_y_n == 0): # 0 indicates there is no mood selection need
        get_random_movie(get_filtered_library())
    # play the movie in here
    if (mood_y_n == 1):
        movie = get_random_movie()
    # play the movie


def get_random_movie(movie_list):
    filtered_movie_list = get_filtered_library()


def get_filtered_library():
    filtered_library = [] # <- jsonRPC stuff

    # do some filtering stuff
    return filtered_library



def get_library():
    json_request = {"jsonrpc": "2.0",
                    "method": "VideoLibrary.GetMovies",
                    "params":
                        {"properties": ["file"]}, "id": "libMovies"}
    response = xbmc.executeJSONRPC(json.dumps(json_request))
    return response.encode("utf-8")