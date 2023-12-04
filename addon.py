import xbmc
import xbmcaddon
import xbmcgui
import pyxbmct
import src.lib_provider as library

import datetime
import requests
import random
import socket

from src import json_utils, providers, mood_analysis



addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
dialog = xbmcgui.Dialog()

# User configuration data that will be used throughout the program
preset_name = ""
watch_status_choice = "any"
media_type_choice = "movie"
genre_choice = ["Action", "Adventure" , "Animation" , "Comedy" , "Crime" , "Drama" , "Fantasy" , "Horror", "Mystery" , "Romance" , "Sci-Fi" , "Western" , "Thriller" , "Documentary" , "History" , "Sport"]
length_choice = ["0","100000"]
release_year_choice = ["0","100000"]
ratings_choice = ["0","10"]
parental_advisory_choice = ["Rated G", "Rated PG", "Rated PG-13", "Rated R", "Rated NC-17", "Rated TV-Y", "Rated TV-Y7", "Rated TV-G", "Rated TV-PG", "Rated TV-14", "Rated TV-MA"]

mood_choice = {}


def backToHome():
    window.close()
    display_home_page()


# Displays main page where the user can choose to randomly select, configure, or choose preset
def display_home_page():
    # user_choice is assigned based on the user's choice. 
    # -1 : Canceled
    # 0 : Presets
    # 1 : Random Select
    # 2 : Search Across Streaming Services
    ui_message = "Would you like to play from your library or watch something based on your mood?\n"
    if json_utils.does_current_config_exist():
        ui_message += "Current Preset: {}".format(json_utils.get_current_config_name())
    else:
        ui_message += "Current Preset: Default"
    user_choice = dialog.yesnocustom(addonname, ui_message, "Others", "Mood", "Play")
    if user_choice == -1:
        xbmc.executebuiltin("Dialog.Close(%s, true)" % dialog)
    elif user_choice == 0:
        window.doModal()
    elif user_choice == 1:
        play_random_media()
    else:
        display_others_page()


class MoodPage(pyxbmct.AddonDialogWindow):
    def __init__(self, title=''):
        super(MoodPage, self).__init__(title)
        self.setGeometry(500, 500, 17, 2, padding=20)
        self.setControls()
        self.set_navigation()

        self.connect(pyxbmct.ACTION_NAV_BACK, backToHome)

    def setControls(self):
        self.happy_sad_slider =  pyxbmct.Slider(textureback=None, texture=None, texturefocus=None,
                                                           orientation=xbmcgui.HORIZONTAL)
        self.happy_label =  pyxbmct.Label("Happy", font='font13', textColor='0xFFFFFFFF',
                                                     disabledColor='0xFFFF3300',
                                                     alignment=0, hasPath=False, angle=0)
        self.sad_label =  pyxbmct.Label("Sad", font='font13', textColor='0xFFFFFFFF',
                                                   disabledColor='0xFFFF3300',
                                                   alignment=1, hasPath=False, angle=0)

        self.placeControl(self.happy_sad_slider, 0, 0, rowspan=1, columnspan=2)
        self.placeControl(self.happy_label, 1, 0, rowspan=1, columnspan=2)
        self.placeControl(self.sad_label, 1, 1, rowspan=1, columnspan=1)
        self.scary_relaxed_slider =  pyxbmct.Slider(textureback=None, texture=None, texturefocus=None,
                                                          orientation=xbmcgui.HORIZONTAL)
        self.scary_label =  pyxbmct.Label("Scary", font='font13', textColor='0xFFFFFFFF',
                                                disabledColor='0xFFFF3300',
                                                alignment=0, hasPath=False, angle=0)
        self.relaxed_label =  pyxbmct.Label("Relaxed", font='font13', textColor='0xFFFFFFFF',
                                                  disabledColor='0xFFFF3300', alignment=1, hasPath=False, angle=0)
        self.placeControl(self.scary_relaxed_slider, 3, 0, rowspan=1, columnspan=2)
        self.placeControl(self.scary_label, 4, 0, rowspan=1, columnspan=2)
        self.placeControl(self.relaxed_label, 4, 1, rowspan=1, columnspan=1)
        self.romantic_platonic_slider =  pyxbmct.Slider(textureback=None, texture=None, texturefocus=None,
                                                              orientation=xbmcgui.HORIZONTAL)
        self.romantic_label =  pyxbmct.Label("Romantic", font='font13', textColor='0xFFFFFFFF',
                                                   disabledColor='0xFFFF3300', alignment=0, hasPath=False, angle=0)
        self.platonic_label =  pyxbmct.Label("Platonic", font='font13', textColor='0xFFFFFFFF',
                                                   disabledColor='0xFFFF3300', alignment=1, hasPath=False, angle=0)
        self.placeControl(self.romantic_platonic_slider, 6, 0, rowspan=1, columnspan=2)
        self.placeControl(self.romantic_label, 7, 0, rowspan=1, columnspan=2)
        self.placeControl(self.platonic_label, 7, 1, rowspan=1, columnspan=1)
        self.mindless_thought_provoking_slider =  pyxbmct.Slider(textureback=None, texture=None,
                                                                       texturefocus=None,
                                                                       orientation=xbmcgui.HORIZONTAL)
        self.mindless_label =  pyxbmct.Label("Mindless", font='font13', textColor='0xFFFFFFFF',
                                                   disabledColor='0xFFFF3300', alignment=0, hasPath=False, angle=0)
        self.thought_provoking_label =  pyxbmct.Label("Thought-provoking", font='font13', textColor='0xFFFFFFFF',
                                                            disabledColor='0xFFFF3300', alignment=1, hasPath=False,
                                                            angle=0)
        self.placeControl(self.mindless_thought_provoking_slider, 9, 0, rowspan=1, columnspan=2)
        self.placeControl(self.mindless_label, 10, 0, rowspan=1, columnspan=2)
        self.placeControl(self.thought_provoking_label, 10, 1, rowspan=1, columnspan=1)
        self.slow_paced_action_packed_slider =  pyxbmct.Slider(textureback=None, texture=None, texturefocus=None,
                                                                     orientation=xbmcgui.HORIZONTAL)
        self.slow_paced_label =  pyxbmct.Label("Slow-paced", font='font13', textColor='0xFFFFFFFF',
                                                     disabledColor='0xFFFF3300', alignment=0, hasPath=False, angle=0)
        self.action_packed_label =  pyxbmct.Label("Action-packed", font='font13', textColor='0xFFFFFFFF',
                                                        disabledColor='0xFFFF3300', alignment=1, hasPath=False, angle=0)
        self.placeControl(self.slow_paced_action_packed_slider, 12, 0, rowspan=1, columnspan=2)
        self.placeControl(self.slow_paced_label, 13, 0, rowspan=1, columnspan=2)
        self.placeControl(self.action_packed_label, 13, 1, rowspan=1, columnspan=1)

        self.update_button =  pyxbmct.Button('Update Movie Info', font='font14')
        self.placeControl(self.update_button, 15, 1, rowspan=2, columnspan=1)
        self.connect(self.update_button, lambda: display_update_movies_page())

        self.submit_button =  pyxbmct.Button('Submit', font='font14')
        self.placeControl(self.submit_button, 15, 0, rowspan=2, columnspan=1)
        self.connect(self.submit_button,
                     lambda:
                     play_random_media_with_mood(self.happy_sad_slider.getPercent(), self.scary_relaxed_slider.getPercent(),
                                                 self.romantic_platonic_slider.getPercent(),
                                                 self.mindless_thought_provoking_slider.getPercent(),
                                                 self.slow_paced_action_packed_slider.getPercent()))

        self.happy_sad_slider.setPercent(50)
        self.scary_relaxed_slider.setPercent(50)
        self.romantic_platonic_slider.setPercent(50)
        self.mindless_thought_provoking_slider.setPercent(50)
        self.slow_paced_action_packed_slider.setPercent(50)

    def set_navigation(self):
        """Set up keyboard/remote navigation between controls."""

        self.happy_sad_slider.controlUp(self.submit_button)
        self.happy_sad_slider.controlDown(self.scary_relaxed_slider)
        self.scary_relaxed_slider.controlDown(self.romantic_platonic_slider)
        self.scary_relaxed_slider.controlUp(self.happy_sad_slider)
        self.romantic_platonic_slider.controlDown(self.mindless_thought_provoking_slider)
        self.romantic_platonic_slider.controlUp(self.scary_relaxed_slider)
        self.mindless_thought_provoking_slider.controlUp(self.romantic_platonic_slider)
        self.mindless_thought_provoking_slider.controlDown(self.slow_paced_action_packed_slider)
        self.slow_paced_action_packed_slider.controlDown(self.submit_button)
        self.slow_paced_action_packed_slider.controlUp(self.mindless_thought_provoking_slider)
        self.submit_button.setNavigation(self.slow_paced_action_packed_slider, self.happy_sad_slider, self.update_button, self.update_button)
        self.update_button.setNavigation(self.slow_paced_action_packed_slider, self.happy_sad_slider, self.submit_button, self.submit_button)
        self.setFocus(self.happy_sad_slider)


# Displays the others page of the addon
def display_others_page():
    user_choice = dialog.yesnocustom(addonname, "What would you like to do?\nThe Preset page allows you to configure your play button.\nThe Search Services page lets you search streaming services for media.", "About", "Search Services", "Presets")
    if user_choice == -1:
        display_home_page()
    elif user_choice == 0:
        display_streaming_service_page()
    elif user_choice == 1:
        display_preset_page()
    else:
        display_about_page()

# Displays the about page of the addon
def display_about_page():
    dialog.ok(addonname,"Created by Harley Wakeman, William Stone, and Mio Mahoney for the CSC380 class during the Fall 2023 semester at SUNY Oswego")
    display_others_page()

# Displays a page where the user can choose what preset they want to use
def display_preset_page():
    preset_names = json_utils.get_preset_names()
    preset_labels_without_options = [f"{preset}" for preset in preset_names]
    preset_labels = preset_labels_without_options
    preset_labels.insert(0, "Edit Preset")
    preset_labels.insert(0, "Delete Preset")
    preset_labels.insert(0, "Add Preset")
    preset_choice_num = dialog.select("Choose Preset", preset_labels)
    if preset_choice_num == -1:
        display_home_page()
    elif preset_choice_num == 0:
        display_configuration_page()
    elif preset_choice_num == 1:
        display_preset_delete_page()
    elif preset_choice_num == 2:
        display_preset_edit_page()
    else:
        preset_choice = preset_labels[preset_choice_num]
        json_utils.update_current_config(preset_choice)
        dialog.ok(addonname, f"Your random play button is now configured to {preset_choice}!")
        display_home_page()

def display_preset_delete_page():
    preset_names = json_utils.get_preset_names()
    preset_labels = [f"{preset}" for preset in preset_names]
    preset_choice_num = [dialog.select("Choose what preset to delete", preset_labels)]
    if preset_choice_num[0] != -1:
        preset_choice = convert_indexes_to_strings(preset_choice_num, preset_labels)[0]
        json_utils.delete_preset(preset_choice)
        if preset_choice == json_utils.get_current_config()["name"]:
            json_utils.delete_current_config()
        dialog.ok(addonname, f"You have deleted the preset {preset_choice}!")
        display_preset_page()
    else:
        display_preset_page()

def display_preset_edit_page():
    preset_names = json_utils.get_preset_names()
    preset_labels = [f"{preset}" for preset in preset_names]
    preset_choice_num = [dialog.select("Choose what preset to edit", preset_labels)]
    if preset_choice_num[0] != -1:
        preset_choice = convert_indexes_to_strings(preset_choice_num, preset_labels)[0]
        preset_dict = json_utils.get_preset(preset_choice)
        load_preset(preset_dict)
        display_configuration_page()
    else:
        display_preset_page()

# Displays the configuration page. The page displays individual configuration
# pages based on user choice and returns to main configuration page after the 
# user submits, unless the user saves the preset or exits.     
def display_configuration_page():
    config_choice = dialog.contextmenu(['Watch Status','Media Type','Genre','Length','Release Year','Rating','Parental Advisory', 'Save', 'Exit'])
    if config_choice == 0:
        display_watch_status_page()
        display_configuration_page()
    elif config_choice == 1:
        display_media_type_page()
        display_configuration_page()
    elif config_choice == 2:
        display_genre_page()
        display_configuration_page()
    elif config_choice == 3:
        display_length_page()
        display_configuration_page()
    elif config_choice == 4:
        display_release_year_page()
        display_configuration_page()
    elif config_choice == 5:
        display_ratings_page()
        display_configuration_page()
    elif config_choice == 6:
        display_parental_advisory_page()
        display_configuration_page()
    elif config_choice == 7:
        display_preset_save_page()
        display_home_page()
    else:
        display_preset_exit_page()
        display_home_page()

def display_streaming_service_page():
    user_wants_movies = dialog.yesno(addonname, "What type of media do you want to search for?", "TV Shows", "Movies")
    media_name_input = dialog.input("What media do you want to find today?")
    media_type = "tv"
    if user_wants_movies:
        media_type = "movie"
    media_name = ""
    providers_with_media = ""
    if media_name_input == "":
        display_home_page()
        return
    try:
        media_name = providers.searchName(media_name_input, media_type)
        providers_with_media = providers.searchProvider(media_name_input, media_type)
        output_text = "{} is available on ".format(media_name)
        if len(providers_with_media) == 1:
            output_text = output_text + providers_with_media[0]
        elif len(providers_with_media) == 2:
            output_text = output_text + providers_with_media[0] + " and " + providers_with_media[1]
        else:
            for provider in providers_with_media[:-1]:
                output_text = output_text + provider + ", "
            output_text = output_text + "and " + providers_with_media[-1]
    except IndexError:
        output_text = "{} couldn't be found! Please make sure spelling is correct.".format(media_name_input)
    except KeyError:
        output_text = "{} isn't available on any streaming services! It may be available for purchase or rent.".format(media_name)

    dialog.ok(addonname, output_text)
    display_home_page()

def is_api_running():
    url = "http://127.0.0.1:5000"
    response = requests.get(url)
    if response.status_code == 200:
        return True
    else:
        return False

def display_update_movies_page():
    update_button = dialog.yesno('Kodi', 'Would you like to update your movie information for your library? If so, make sure the '
                                         'MoodAnalysisAPI is running on https://local.host/5000/')
    if update_button and is_api_running():
        p_dialog = xbmcgui.DialogProgress()
        p_dialog.create('Kodi', 'Gathering movie info...')
        mood_analysis.write_media_json()
        p_dialog.close()
        window.doModal()
    elif update_button and not is_api_running():
        dialog.ok('Error', 'Make sure the API is running')
        window.doModal()
    else:
        window.doModal()

# Displays a page where the user can choose if they want to see media they've already seen
def display_watch_status_page():
    global watch_status_choice
    watch_status_choice_temp = dialog.yesnocustom(addonname, "Do you want to see media you've already watched?", "Unwatched", "Any", "Watched")
    if watch_status_choice_temp == -1:
        pass
    elif watch_status_choice_temp == 0:
        watch_status_choice = "any"
    elif watch_status_choice_temp == 1:
        watch_status_choice = "watched"
    else:
        watch_status_choice = "unwatched"

# Displays a page where the user can choose if they want to watch TV Shows or Movies
def display_media_type_page():
    global media_type_choice
    media_type_choice_num = dialog.yesno(addonname, "What type of media do you want to watch?", "Movies", "TV Shows")
    if media_type_choice_num == 0:
        media_type_choice = "movie"
    elif media_type_choice_num == 1:
        media_type_choice = "tvshow"

# Displays a page where the user can choose what genres they want to watch
def display_genre_page():
    global genre_choice
    genres = ["Action", "Adventure" , "Animation" , "Comedy" , "Crime" , "Drama" , "Fantasy" , "Horror", "Mystery" , "Romance" , "Sci-Fi" , "Western" , "Thriller" , "Documentary" , "History" , "Sport"]
    genre_labels = [f"{genre}" for genre in genres]
    genre_choice_nums = dialog.multiselect("Select Movie Genres", genre_labels)
    if genre_choice_nums == None:
        pass
    else:
        genre_choice = convert_indexes_to_strings(genre_choice_nums, genre_labels)

# Displays a page where the user can choose what lengths of media they want to watch
def display_length_page():
    global length_choice
    lengths = [15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180]
    length_labels = [f"{length}" for length in lengths]
    length_choice_num_1 = dialog.select("Select Minimum Movie Length (Minutes)", length_labels)
    lengths_2 = lengths[length_choice_num_1:]
    length_labels_2 = [f"{length}" for length in lengths_2]
    length_choice_num_2 = dialog.select("Select Maximum Movie Length (Minutes)", length_labels_2)
    if length_choice_num_1 == None or length_choice_num_2 == None:
        pass
    else:
        length_choice_nums = [length_choice_num_1, length_choice_num_1 + length_choice_num_2]
        length_choice = convert_indexes_to_strings(length_choice_nums, length_labels)

# Displays a page where the user can choose what release years they would like to watch
def display_release_year_page():
    global release_year_choice
    min_year = 1900
    max_year = datetime.date.today().year
    years = [str(year) for year in range(min_year, max_year + 1)][::-1]
    min_year_input = max_year - dialog.select("Choose Minimum Year", years)
    years = [str(year) for year in range(min_year_input, max_year + 1)][::-1]
    max_year_input = max_year - dialog.select("Choose Maximum Year", years)
    if min_year_input == min_year + 1:
        min_year_input = min_year
    if max_year_input == max_year + 1:
        max_year_input = max_year
    release_year_choice = []
    release_year_choice.append(str(min_year_input))
    release_year_choice.append(str(max_year_input))

# Displays a page where the user can choose what ratings they would like to watch
def display_ratings_page():
    global ratings_choice
    ratings = [0,1,2,3,4,5,6,7,8,9,10]
    ratings_labels = [f"{rating}" for rating in ratings]
    ratings_choice_num_1 = dialog.select("Select Minimum Movie Rating", ratings_labels)
    ratings_2 = ratings[ratings_choice_num_1:]
    ratings_labels_2 = [f"{rating}" for rating in ratings_2]
    ratings_choice_num_2 = dialog.select("Select Maximum Movie Rating", ratings_labels_2)
    if ratings_choice_num_1 == None or ratings_choice_num_2 == None:
        pass
    else:
        length_choice_nums = [ratings_choice_num_1, ratings_choice_num_1 + ratings_choice_num_2]
        ratings_choice = convert_indexes_to_strings(length_choice_nums, ratings_labels)

# Displays a page where the user can choose what parental advisory ratings they would like to watch
def display_parental_advisory_page():
    global parental_advisory_choice
    parent_ratings = ["Rated G", "Rated PG", "Rated PG-13", "Rated R", "Rated NR"]
    parent_rating_labels = [f"{parent_rating}" for parent_rating in parent_ratings]
    parent_rating_choice_nums = dialog.multiselect("Select Parental Advisory Ratings", parent_rating_labels)
    if parent_rating_choice_nums == None:
        pass
    else:
        parental_advisory_choice = convert_indexes_to_strings(parent_rating_choice_nums, parent_rating_labels)

# Controls for user to save configuration as preset
def display_preset_save_page():
    global preset_name
    if preset_name == "":
        preset_name = dialog.input("What do you want the name of the preset to be?")
        preset_names = json_utils.get_preset_names()
        while preset_name in preset_names:
            preset_name = dialog.input("That name already exists! What do you want the name of the preset to be?")
        preset_dict = create_preset_dict()
        json_utils.add_preset(preset_dict)
    else:
        preset_dict = create_preset_dict()
        json_utils.replace_preset(preset_dict)
    json_utils.update_current_config(preset_name)
    dialog.ok(addonname,"Your preset is now ready to play random media!")
    reset_config()

def display_preset_exit_page():
    user_choice = dialog.yesno(addonname, "Do you want to stop configuring this preset? Your current configurations won't be saved.")
    if user_choice:
        display_preset_page()
    else:
        display_configuration_page()

# This function will use the user configuration data arrays to randomly choose from media
def play_random_media():
    media_title = ""
    media = ""
    try:
        media = library.randomize_media()
        media_title = media["title"]
        window.close()
        time_remaining = 5
        user_choice = dialog.yesnocustom(addonname, f"Do you want to watch {media_title}? Media will automatically play in {time_remaining} seconds.", "Cancel", "Play", "Randomize again" ,autoclose = 5000)
        # If the user clicks exit button or cancel button, go back to home page
        # If the user clicks Play or doesn't choose, play the media
        # If the user clicks Randomize again, randomize again with the same mood values
        if user_choice == 2 or user_choice == -1:
            display_home_page()
        elif user_choice == 1:
            play_random_media()
        elif user_choice == 0:
                library.play_media(media["path"])
    except Exception:
        dialog.ok(addonname, "No media that matches your configuration. Please modify it!")
        display_home_page()

# This function will use the user configuration data arrays as well as the given mood values
# to randomly choose from media
def play_random_media_with_mood(happy_sad, scary_relaxed, romantic_platonic, mindless_thought_provoking,
                                slow_paced_action_packed):
    if not mood_analysis.check_if_mood_analysis_can_be_performed():
        dialog.notification('Error', 'Update Movie Information.')
    movies = mood_analysis.play_random_media_with_mood(happy_sad, scary_relaxed, romantic_platonic,
                                                       mindless_thought_provoking, slow_paced_action_packed)
    if len(movies) == 0:
        xbmc.log("play_random_media_with_mood error")
    rand_index = random.randint(0, len(movies) - 1)
    random_movie = movies[rand_index]
    media_title = random_movie.title
    window.close()
    time_remaining = 5
    user_choice = dialog.yesnocustom(addonname, f"Do you want to watch {media_title}? Media will automatically play in {time_remaining} seconds.", "Cancel", "Play", "Randomize again" ,autoclose = 5000)
    # If the user clicks exit button or cancel button, go back to home page
    # If the user clicks Play or doesn't choose, play the movie
    # If the user clicks Randomize again, randomize again with the same mood values
    if user_choice == 2 or user_choice == -1:
        display_home_page()
    elif user_choice == 1: #PLAY MEDIA
        play_random_media_with_mood(happy_sad, scary_relaxed, romantic_platonic, mindless_thought_provoking, slow_paced_action_packed)
    elif user_choice == 0:
        library.play_media(random_movie.path)


# This function takes the indices that the multi-select controls produce and fills
# them with the corresponding strings. This will make it much easier to program with
# (Example: the index 0 will instead be "Science Fiction" in genre_choice variable)
def convert_indexes_to_strings(int_arr, string_arr):
    result_arr = []
    for index in int_arr:
        result_arr.append(string_arr[index])
    return result_arr

def reset_config():
    global preset_name, watch_status_choice, media_type_choice, genre_choice, length_choice, release_year_choice, ratings_choice, parental_advisory_choice
    preset_name = ""
    watch_status_choice = "any"
    media_type_choice = "movie"
    genre_choice = ["Action", "Adventure" , "Animation" , "Comedy" , "Crime" , "Drama" , "Fantasy" , "Horror", "Mystery" , "Romance" , "Sci-Fi" , "Western" , "Thriller" , "Documentary" , "History" , "Sport"]
    length_choice = ["0","100000"]
    release_year_choice = ["0","100000"]
    ratings_choice = ["0","10"]
    parental_advisory_choice = ["Rated G", "Rated PG", "Rated PG-13", "Rated R", "Rated NC-17", "Rated TV-Y", "Rated TV-Y7", "Rated TV-G", "Rated TV-PG", "Rated TV-14", "Rated TV-MA"]

def load_preset(preset_dict):
    global preset_name, watch_status_choice, media_type_choice, genre_choice, length_choice, release_year_choice, ratings_choice, parental_advisory_choice
    preset_name = preset_dict["name"]
    watch_status_choice = preset_dict["watch-status"]
    media_type_choice = preset_dict["media-type"]
    genre_choice = preset_dict["genres"]
    length_choice = preset_dict["media-length"]
    release_year_choice = preset_dict["release-year"]
    ratings_choice = preset_dict["ratings"]
    parental_advisory_choice = preset_dict["parental-advisory"]


def create_preset_dict():
    return {
        "name": preset_name,
        "watch-status": watch_status_choice,
        "media-type": media_type_choice,
        "genres": genre_choice,
        "media-length": length_choice,
        "release-year": release_year_choice,
        "ratings": ratings_choice,
        "parental-advisory": parental_advisory_choice,
    }

def is_internet_available():
    try:
        response = requests.get("http://www.google.com", timeout=5)
        response.raise_for_status()
        return True
    except requests.RequestException:
        return False



window = MoodPage(addonname)


# -----------------------------------------------------------------------------------------------------
# Starts Program
# -----------------------------------------------------------------------------------------------------

display_home_page()
