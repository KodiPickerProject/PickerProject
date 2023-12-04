import requests

def getTMDBid(term, media_type):
    url = "https://api.themoviedb.org/3/search/{media_type}?query={term}&include_adult=true&language=en-US".format(media_type=media_type, term=term)
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5Y2NmM2YwNjEzOWNjMGQ4ZTUzYTViZDVlMjg4NmYxZCIsInN1YiI6IjY1M2ZhYTIzYmMyY2IzMDEyYzMyOGU2MCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.X6L4WchIsUuFyTZ-ZzvRCcI5NldeOZBkDzdWgQmKzGo"
    }
    response = requests.get(url, headers=headers)
    return response.json()["results"][0]["id"]

def getMediaItem(term, media_type):
    url = "https://api.themoviedb.org/3/search/{media_type}?query={term}&include_adult=true&language=en-US".format(media_type=media_type, term=term)
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5Y2NmM2YwNjEzOWNjMGQ4ZTUzYTViZDVlMjg4NmYxZCIsInN1YiI6IjY1M2ZhYTIzYmMyY2IzMDEyYzMyOGU2MCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.X6L4WchIsUuFyTZ-ZzvRCcI5NldeOZBkDzdWgQmKzGo"
    }
    return requests.get(url, headers=headers).json()["results"][0]


def getProvider(id, media_type):
    url = "https://api.themoviedb.org/3/{media_type}/{id}/watch/providers".format(id=id, media_type=media_type)
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5Y2NmM2YwNjEzOWNjMGQ4ZTUzYTViZDVlMjg4NmYxZCIsInN1YiI6IjY1M2ZhYTIzYmMyY2IzMDEyYzMyOGU2MCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.X6L4WchIsUuFyTZ-ZzvRCcI5NldeOZBkDzdWgQmKzGo"
    }
    response = requests.get(url, headers=headers)
    return response.json()

def searchName(term, media_type):
    response = getMediaItem(term, media_type)
    if media_type == "tv":
        return response["name"]
    return response["title"]

def searchProvider(term, media_type):
    idOfMedia = getTMDBid(term, media_type)
    providers = getProvider(idOfMedia, media_type)
    providerList = []
    for provider in providers["results"]["US"]["flatrate"]:
            providerList.append(provider["provider_name"])
    return providerList

