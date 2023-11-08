import requests


def getTMDBid(term):
    url = "https://api.themoviedb.org/3/search/movie?query={term}&include_adult=true&language=en-US".format(term=term)
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5Y2NmM2YwNjEzOWNjMGQ4ZTUzYTViZDVlMjg4NmYxZCIsInN1YiI6IjY1M2ZhYTIzYmMyY2IzMDEyYzMyOGU2MCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.X6L4WchIsUuFyTZ-ZzvRCcI5NldeOZBkDzdWgQmKzGo"
    }
    response = requests.get(url, headers=headers)
    results = response.json()["results"]
    return response.json()["results"][0]


def getProvider(id):
    url = "https://api.themoviedb.org/3/movie/{id}/watch/providers".format(id=id)
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5Y2NmM2YwNjEzOWNjMGQ4ZTUzYTViZDVlMjg4NmYxZCIsInN1YiI6IjY1M2ZhYTIzYmMyY2IzMDEyYzMyOGU2MCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.X6L4WchIsUuFyTZ-ZzvRCcI5NldeOZBkDzdWgQmKzGo"
    }
    response = requests.get(url, headers=headers)
    return response.json()["results"]["US"]


def searchProvider(term):
    response = getTMDBid(term)
    idOfMovie = response["id"]
    providers = getProvider(idOfMovie)
    providerList = []
    priority = 0
    for provider in providers["flatrate"]:
            providerList.append(provider["provider_name"])
    return providerList
