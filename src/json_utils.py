import json
import xbmcvfs

root_path = xbmcvfs.translatePath("special://home/addons/script.episode.picker/UserData/")
presets_file_path = root_path+'presets.json'
current_config_file_path = root_path+'current_config.json'

presets_file = ""
current_config_file = ""
presets_data = ""
current_config_data = ""

try:
    presets_file = open(presets_file_path, "r+")
    current_config_file = open(current_config_file_path, "r+")
    presets_data = json.load(presets_file)
    current_config_data = json.load(current_config_file)
        
except (FileNotFoundError, json.decoder.JSONDecodeError):
    pass


# This function will get a preset with the given name
def get_preset(preset_name):
    global presets_data, presets_file
    for item in presets_data:
        if item["name"] == preset_name:
            return item
    return None

#Adds a preset to presets.json
def add_preset(preset_dict):
    global presets_data, presets_file
    try:
        with open(presets_file_path, 'r') as json_file:
            presets_data = json.load(json_file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        presets_data = []
    presets_data.append(preset_dict)
    with open(presets_file_path, 'w') as json_file:
        json.dump(presets_data, json_file, indent=4)
    presets_file = open(presets_file_path, "r+")
    presets_data = json.load(open(presets_file_path, 'r'))

#Deletes a preset from presets.json
def delete_preset(config_name):
    global presets_data, presets_file
    for preset in presets_data:
        if preset.get("name") == config_name:
            presets_data.remove(preset)
    with open(presets_file_path, 'w') as json_file:
            json.dump(presets_data, json_file, indent=4)
    presets_file = open(presets_file_path, "r+")
    presets_data = json.load(presets_file)

def replace_preset(preset_dict):
    global presets_data, presets_file
    delete_preset(preset_dict["name"])
    add_preset(preset_dict)
    presets_file = open(presets_file_path, "r+")
    presets_data = json.load(presets_file)

#Gets the current config being used
def get_current_config():
    global current_config_data
    return current_config_data

def delete_current_config():
    global current_config_data, current_config_file
    with open(current_config_file_path, 'w') as json_file:
        json.dump("", json_file, indent=4)
    current_config_file = open(current_config_file_path, "r+")
    current_config_data = json.load(current_config_file)
        


#Updates the current config being used and writes it to current_config.json
def update_current_config(config_name):
    global presets_data, presets_file, current_config_data, current_config_file
    config_to_update = {}
    name_exists = False
    for preset in presets_data:
        if preset["name"] == config_name:
            config_to_update = preset
            name_exists = True
            break
    if name_exists:
        with open(current_config_file_path, 'w') as json_file:
            json.dump(config_to_update, json_file, indent=4)
    else:
        pass
    current_config_file = open(current_config_file_path, "r+")
    current_config_data = json.load(current_config_file)

# This function will obtain the names of all of the user presets from our UserData json files
def get_preset_names():
    global presets_data
    names = []
    for item in presets_data:
        names.append(item["name"])
    return names
    
