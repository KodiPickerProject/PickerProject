import json
import os
import requests
from src import lib_provider
import xbmcvfs


def get_movie_titles():
    movies = lib_provider.get_movies_arrs()
    movie_titles = []
    for movie in movies:
        movie_titles.append(movie["title"])
    return movie_titles


def get_movie_paths():
    movies = lib_provider.get_movies_arrs()
    movie_paths = []
    for movie in movies:
        movie_paths.append(movie["path"])
    return movie_paths

# Call this from addon.py, give the user the choice to rerun the api
def call_media_api():
    response = requests.get("http://127.0.0.1:5000/?", params={
        'movie_list': get_movie_titles(),
        'kodi_ids': get_movie_paths()})
    return response


def write_media_json():
    root_path = xbmcvfs.translatePath("special://home/addons/script.quick.picker/UserData/")
    media_json_file_path = root_path + 'media.json'
    response = call_media_api()
    json_string = response.content.decode('utf-8')
    data = json.loads(json_string)
    json_obj = json.dumps(data)
    json_file = open(media_json_file_path, "w")
    json_file.write(json_obj)
    json_file.close()


# Returns False if media.json is empty, returns true otherwise
def check_if_mood_analysis_can_be_performed():
    root_path = xbmcvfs.translatePath("special://home/addons/script.quick.picker/UserData/")
    media_json_file_path = root_path + 'media.json'
    return os.stat(media_json_file_path).st_size != 0


def play_random_media_with_mood(happy_sad, scary_relaxed, romantic_platonic, mindless_thought_provoking,
                                slow_paced_action_packed):
    root_path = xbmcvfs.translatePath("special://home/addons/script.quick.picker/UserData/")
    media_json_file_path = root_path + 'media.json'
    happy = sad = 0
    scary = relaxed = romantic = platonic = mindless = thought_provoking = slow_paced = action_packed = -1
    if happy_sad < 50:
        happy = happy_sad / 50
    else:
        sad = happy_sad / 100
    if scary_relaxed < 50:
        scary = scary_relaxed / 50
    else:
        relaxed = scary_relaxed / 100
    if romantic_platonic < 50:
        romantic = romantic_platonic / 50
    else:
        platonic = romantic_platonic / 100
    if mindless_thought_provoking < 50:
        mindless = mindless_thought_provoking / 50
    else:
        thought_provoking = mindless_thought_provoking / 100
    if slow_paced_action_packed < 50:
        slow_paced = slow_paced_action_packed / 50
    else:
        action_packed = slow_paced_action_packed / 100
    mood_vals_inp = [happy, sad, scary, relaxed, romantic, platonic, mindless, thought_provoking, slow_paced,
                     action_packed]
    file = open(media_json_file_path)
    movies = json.load(file)
    movie_objs = []
    for movie in movies:
        # Compare each movie to the normalized slider values, take the movies with the highest vals
        movie_title = movie["title"]
        movie_path = movie["path"]
        movie_mood_vals = [movie["happy"], movie["sad"], movie["scary"], movie["relaxed"], movie["romantic"],
                           movie["platonic"], movie["mindless"], movie["thought-provoking"], movie["slow-paced"],
                           movie["action-packed"]]
        distance = euclidean_dist(mood_vals_inp, movie_mood_vals)
        # Add distance to list and find the three smallest values (most similar)
        temp_movie = Movie(movie_title, movie_path, distance)
        movie_objs.append(temp_movie)

    # Sort list in descending order based on euclidean distance
    movie_objs.sort(key=lambda x: x.distance, reverse=False)
    if len(movie_objs) == 0:
        return
    elif len(movie_objs) < 3:
        movies_ = [movie_objs[0]]
        return movies_
    elif len(movie_objs) < 10:
        movies_ = []
        i = 0
        while i < 3:
            movies_.append(movie_objs[i])
            i += 1
        return movies_
    else:
        movies_ = []
        i = 0
        while i < 5:
            movies_.append(movie_objs[i])
            i += 1
        return movies_


class Movie:
    def __init__(self, title, path, distance):
        self.title = title
        self.path = path
        self.distance = distance

    def get_path(self):
        return self.title

    def get_title(self):
        return self.title

    def get_distance(self):
        return self.distance


def euclidean_dist(movie_list1, movie_list2):
    assert len(movie_list1) == len(movie_list2)
    s = 0
    for i in range(len(movie_list1)):
        s += (movie_list1[i] - movie_list2[i]) ** 2
    return s ** .5




