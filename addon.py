import xbmc
import xbmcaddon
import xbmcgui
import pyxbmct

from src import json_utils, providers

addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
dialog = xbmcgui.Dialog()
window = pyxbmct.AddonDialogWindow(addonname)

# User configuration data that will be used throughout the program
preset_name = ""
watch_status_choice = -1
genre_choice = []
length_choice = []
release_year_choice = []
ratings_choice = []
languages_choice = []
parental_advisory_choice = []
closed_captions_choice = False

mood_choice = {}

# Displays main page where the user can choose to randomly select, configure, or choose preset
def display_home_page():
    # user_choice is assigned based on the user's choice. 
    # -1 : Canceled
    # 0 : Presets
    # 1 : Random Select
    # 2 : Search Across Streaming Services
    user_choice = dialog.yesnocustom(addonname, "What would you like to do?", "Search Services", "Presets", "Random Select")
    if user_choice == -1:
        xbmc.executebuiltin("Dialog.Close(%s, true)" % dialog) 
    elif user_choice == 0:
        display_preset_page()
    elif user_choice == 1:
        user_choice = dialog.yesno(addonname, "Would you like to choose media based on your mood today?")
        if user_choice:
            display_mood_page()
        else:
            play_random_media()
    else:
        display_streaming_service_page()

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

# Displays the configuration home page       
def display_configuration_page():
    reset_config()
    config_choice = dialog.contextmenu(['Watch Status','Genre','Length','Release Year','Rating','Language','Parental Advisory','Closed Captions', 'Save', 'Exit'])
    if config_choice == 0:
        display_watch_status_page()
        display_configuration_page()
    if config_choice == 1:
        display_genre_page()
        display_configuration_page()
    if config_choice == 2:
        display_length_page()
        display_configuration_page()
    if config_choice == 3:
        display_release_year_page()
        display_configuration_page()
    if config_choice == 4:
        display_ratings_page()
        display_configuration_page()
    if config_choice == 5:
        display_languages_page()
        display_configuration_page()
    if config_choice == 6:
        display_parental_advisory_page()
        display_configuration_page()
    if config_choice == 7:
        display_closed_captions_page()
        display_configuration_page()
    if config_choice == 8:
        display_preset_save_page()
        display_home_page()
    if config_choice == 9:
        display_preset_exit_page()
        display_home_page()

def display_streaming_service_page():
    media_name = dialog.input("What media do you want to find today?")
    try:
        providers_with_media = providers.searchProvider(media_name)
        output_text = "This media is available on "
        if len(providers_with_media) == 1:
            output_text = "This media is available on " + providers_with_media[0]
        elif len(providers_with_media) == 2:
            output_text = "This media is available on " + providers_with_media[0] + " and " + providers_with_media[1]
        else:
            for provider in providers_with_media[:-1]:
                output_text = output_text + provider + ", "
            output_text = output_text + "and " + providers_with_media[-1]
    except Exception:
        output_text = "This media couldn't be found! Please make sure capitalization and spelling is correct."
        
    dialog.ok(addonname, output_text)
    display_home_page()

def display_mood_page():
    window.setGeometry(500, 500, 17, 1, padding=20)
    happy_sad_slider = pyxbmct.addonwindow.Slider(textureback=None, texture=None, texturefocus=None, orientation=xbmcgui.HORIZONTAL)
    happy_label = pyxbmct.addonwindow.Label("Happy", font='font13', textColor='0xFFFFFFFF', disabledColor='0xFFFF3300', alignment=0, hasPath=False, angle=0)
    sad_label = pyxbmct.addonwindow.Label("Sad", font='font13', textColor='0xFFFFFFFF', disabledColor='0xFFFF3300', alignment=1, hasPath=False, angle=0)
    window.placeControl(happy_sad_slider, 0, 0, rowspan=1, columnspan=1)
    window.placeControl(happy_label, 1, 0, rowspan=1, columnspan=1)
    window.placeControl(sad_label, 1, 0, rowspan=1, columnspan=1)
    scary_relaxed_slider = pyxbmct.addonwindow.Slider(textureback=None, texture=None, texturefocus=None, orientation=xbmcgui.HORIZONTAL)
    scary_label = pyxbmct.addonwindow.Label("Scary", font='font13', textColor='0xFFFFFFFF', disabledColor='0xFFFF3300', alignment=0, hasPath=False, angle=0)
    relaxed_label = pyxbmct.addonwindow.Label("Relaxed", font='font13', textColor='0xFFFFFFFF', disabledColor='0xFFFF3300', alignment=1, hasPath=False, angle=0)
    window.placeControl(scary_relaxed_slider, 3, 0, rowspan=1, columnspan=1)
    window.placeControl(scary_label, 4, 0, rowspan=1, columnspan=1)
    window.placeControl(relaxed_label, 4, 0, rowspan=1, columnspan=1)
    romantic_platonic_slider = pyxbmct.addonwindow.Slider(textureback=None, texture=None, texturefocus=None, orientation=xbmcgui.HORIZONTAL)
    romantic_label = pyxbmct.addonwindow.Label("Romantic", font='font13', textColor='0xFFFFFFFF', disabledColor='0xFFFF3300', alignment=0, hasPath=False, angle=0)
    platonic_label = pyxbmct.addonwindow.Label("Platonic", font='font13', textColor='0xFFFFFFFF', disabledColor='0xFFFF3300', alignment=1, hasPath=False, angle=0)
    window.placeControl(romantic_platonic_slider, 6, 0, rowspan=1, columnspan=1)
    window.placeControl(romantic_label, 7, 0, rowspan=1, columnspan=1)
    window.placeControl(platonic_label, 7, 0, rowspan=1, columnspan=1)
    mindless_thought_provoking_slider = pyxbmct.addonwindow.Slider(textureback=None, texture=None, texturefocus=None, orientation=xbmcgui.HORIZONTAL)
    mindless_label = pyxbmct.addonwindow.Label("Mindless", font='font13', textColor='0xFFFFFFFF', disabledColor='0xFFFF3300', alignment=0, hasPath=False, angle=0)
    thought_provoking_label = pyxbmct.addonwindow.Label("Thought-provoking", font='font13', textColor='0xFFFFFFFF', disabledColor='0xFFFF3300', alignment=1, hasPath=False, angle=0)
    window.placeControl(mindless_thought_provoking_slider, 9, 0, rowspan=1, columnspan=1)
    window.placeControl(mindless_label, 10, 0, rowspan=1, columnspan=1)
    window.placeControl(thought_provoking_label, 10, 0, rowspan=1, columnspan=1)
    slow_paced_action_packed_slider = pyxbmct.addonwindow.Slider(textureback=None, texture=None, texturefocus=None, orientation=xbmcgui.HORIZONTAL)
    slow_paced_label = pyxbmct.addonwindow.Label("Slow-paced", font='font13', textColor='0xFFFFFFFF', disabledColor='0xFFFF3300', alignment=0, hasPath=False, angle=0)
    action_packed_label = pyxbmct.addonwindow.Label("Action-packed", font='font13', textColor='0xFFFFFFFF', disabledColor='0xFFFF3300', alignment=1, hasPath=False, angle=0)
    window.placeControl(slow_paced_action_packed_slider, 12, 0, rowspan=1, columnspan=1)
    window.placeControl(slow_paced_label, 13, 0, rowspan=1, columnspan=1)
    window.placeControl(action_packed_label, 13, 0, rowspan=1, columnspan=1)
    submit_button = pyxbmct.addonwindow.Button('Submit', font='font14')
    window.placeControl(submit_button, 15, 0, rowspan=2, columnspan=1)
    window.connect(submit_button, lambda:
        play_random_media_with_mood(happy_sad_slider, scary_relaxed_slider, romantic_platonic_slider, mindless_thought_provoking_slider, slow_paced_action_packed_slider)
    )
    window.doModal()

# Displays a page where the user can choose if they want to see media they've already seen
def display_watch_status_page():
    global watch_status_choice
    watch_status_choice = dialog.yesnocustom(addonname, "Do you want to see media you've already watched?", "Unwatched", "Any", "Watched")

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
    lengths = ["0-30 Minutes", "31-60 minutes", "61-90 minutes","91-120 minutes","121-180 minutes",">180 minutes"]
    length_labels = [f"{length}" for length in lengths]
    length_choice_nums = dialog.multiselect("Select Movie Length", length_labels)
    if length_choice_nums == None:
        pass
    else:
        length_choice = convert_indexes_to_strings(length_choice_nums, length_labels)

# Displays a page where the user can choose what release years they would like to watch
def display_release_year_page():
    global release_year_choice
    min_year = 1900
    max_year = 2030
    years = [str(year) for year in range(min_year, max_year + 1)][::-1]
    min_year_input = min_year - dialog.select("Choose Minimum Year", years)
    max_year_input = max_year - dialog.select("Choose Maximum Year", years)
    if min_year_input == min_year + 1:
        min_year_input = min_year
    if max_year_input == max_year + 1:
        max_year_input = max_year
    release_year_choice = []
    release_year_choice.append(min_year_input)
    release_year_choice.append(max_year_input)

# Displays a page where the user can choose what ratings they would like to watch
def display_ratings_page():
    global ratings_choice
    ratings = ["0-1", "1.1-2", "2.1-3", "3.1-4", "4.1-5", "5.1-6", "6.1-7", "7.1-8", "8.1-9", "9.1-10"]
    ratings_labels = [f"{rating}" for rating in ratings]
    ratings_choice_nums = dialog.multiselect("Select Movie Ratings", ratings_labels)
    if ratings_choice_nums == None:
        pass
    else:
        ratings_choice = convert_indexes_to_strings(ratings_choice_nums, ratings_labels)

# Displays a page where the user can choose what languages they would like to watch
def display_languages_page():
    global languages_choice
    languages = ["English", "Spanish", "German", "French", "Mandarin", "Hindi", "Arabic", "Portuguese", "Bengali", "Russian", "Japanese"]
    language_labels = [f"{language}" for language in languages]
    language_choice_nums = dialog.multiselect("Select Movie Languages", language_labels)
    if language_choice_nums == None:
        pass
    else:
        languages_choice = convert_indexes_to_strings(language_choice_nums, language_labels)

# Displays a page where the user can choose what parental advisory ratings they would like to watch
def display_parental_advisory_page():
    global parental_advisory_choice
    parent_ratings = ["G", "PG", "PG-13", "R", "NR"]
    parent_rating_labels = [f"{parent_rating}" for parent_rating in parent_ratings]
    parent_rating_choice_nums = dialog.multiselect("Select Parental Advisory Ratings", parent_rating_labels)
    if parent_rating_choice_nums == None:
        pass
    else:
        parental_advisory_choice = convert_indexes_to_strings(parent_rating_choice_nums, parent_rating_labels)

# Displays a page where the user can choose if they want to only watch media with closed captions
def display_closed_captions_page():
    global closed_captions_choice
    closed_captions_choice = dialog.yesno(addonname, "Do you want to only watch media with closed captions?")

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
    reset_config()
    dialog.ok(addonname,"Your preset is now ready to play random media!")

def display_preset_exit_page():
    user_choice = dialog.yesno(addonname, "Do you want to stop configuring this preset? Your current configurations won't be saved.")
    if user_choice:
        display_preset_page()
    else:
        display_configuration_page()

# This function will use the user configuration data arrays to randomly choose from media
def play_random_media():
    dialog.ok(addonname, "This is where our app will randomly play a movie.")

# This function will use the user configuration data arrays to randomly choose from media
def play_random_media_with_mood(happy_sad, scary_relaxed, romantic_platonic, mindless_thought_provoking, slow_paced_action_packed):
    dialog.ok(addonname, "Happy/Sad value: " + str(happy_sad.getPercent()) + "\n" +
                         "Scary/Relaxed value: " + str(scary_relaxed.getPercent()) + "\n" +
                         "Romantic/Platonic value: " + str(romantic_platonic.getPercent()) + "\n" +
                         "Mindless/Thought Provoking value: " + str(mindless_thought_provoking.getPercent()) + "\n" +
                         "Slow Paced/Action Packed value: " + str(slow_paced_action_packed.getPercent()) + "\n")
    dialog.ok(addonname, "This is where our app will randomly play a movie.")

# This function takes the indices that the multiselect controls produce and fills 
# them with the corresponding strings. This will make it much easier to program with
# (Example: the index 0 will instead be "Science Fiction" in genre_choice variable)
def convert_indexes_to_strings(int_arr, string_arr):
    result_arr = []
    for index in int_arr:
        result_arr.append(string_arr[index])
    return result_arr

def reset_config():
    preset_name = ""
    watch_status_choice = -1
    genre_choice = []
    length_choice = []
    release_year_choice = []
    ratings_choice = []
    languages_choice = []
    parental_advisory_choice = []
    closed_captions_choice = -1

def load_preset(preset_dict):
    global preset_name, watch_status_choice, genre_choice, length_choice, release_year_choice, ratings_choice, languages_choice, parental_advisory_choice, closed_captions_choice
    preset_name = preset_dict["name"]
    watch_status_choice = preset_dict["watch-status"]
    genre_choice = preset_dict["genres"]
    length_choice = preset_dict["media-length"]
    release_year_choice = preset_dict["release-year"]
    ratings_choice = preset_dict["ratings"]
    languages_choice = preset_dict["languages"]
    parental_advisory_choice = preset_dict["parental-advisory"]
    closed_captions_choice = preset_dict["closed-captions"]
    

def create_preset_dict():
    return {
        "name": preset_name,
        "watch-status": watch_status_choice,
        "genres": genre_choice,
        "media-length": length_choice,
        "release-year": release_year_choice,
        "ratings": ratings_choice,
        "languages": languages_choice,
        "parental-advisory": parental_advisory_choice,
        "closed-captions": closed_captions_choice
    }

# -----------------------------------------------------------------------------------------------------
# Starts Program
# -----------------------------------------------------------------------------------------------------

display_home_page()
