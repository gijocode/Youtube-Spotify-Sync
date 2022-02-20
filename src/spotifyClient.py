import json, youtube_dl
from urllib import response
from unicodedata import name
import requests


class SpotifyClient:
    def __init__(self) -> None:
        self.tracksToAdd = []
        userDetails = json.load(open("data/spotify_secret.json"))
        self.userId, self.token = userDetails["userId"], userDetails["oauthToken"]
        self.headersList = {"Accept": "*/*", "Authorization": f"Bearer {self.token}"}
        self.playlistId = None

    def getPlaylistTracks(self):
        reqUrl = f"https://api.spotify.com/v1/playlists/{self.playlistId}/tracks"
        trackList = []
        while True:
            response = requests.request("GET", reqUrl, headers=self.headersList)
            if response.status_code == 200:
                trackList.extend(
                    [track["track"]["id"] for track in response.json()["items"]]
                )
                reqUrl = response.json()["next"]
                if not reqUrl:
                    break
            else:
                break
        return trackList

    def createPlaylist(self):
        # Initialize variables
        playlistsList = []
        reqUrl = f"https://api.spotify.com/v1/users/{self.userId}/playlists"
        payload = json.dumps(
            {
                "name": "Youtube Playlist",
                "description": "Synced Playlist between Youtube and Spotify",
                "public": False,
            }
        )
        # Return all playlists of user
        while True:
            response = requests.request("GET", reqUrl, headers=self.headersList)
            playlistData = response.json()
            playlistsList.extend(playlistData["items"])

            if playlistData["next"]:
                reqUrl = playlistData["next"]
            else:
                break

        # Check if playlist already exists, else create new playlist
        for playlist in playlistsList:
            if playlist.get("name") == "Youtube Playlist":
                self.playlistId = playlist["id"]
                return f"Playlist already exists with id {self.playlistId}"
        reqUrl = f"https://api.spotify.com/v1/users/{self.userId}/playlists"
        response = requests.request(
            "POST", reqUrl, data=payload, headers=self.headersList
        )
        if response.status_code == 201:
            self.playlistId = response.json()["id"]
            return f"Playlist created with id {self.playlistId}"
        raise Exception(f"Error: {response.status_code}")

    def findTrack(self, youtubeUrl):
        trackDetails = {}
        video = youtube_dl.YoutubeDL({}).extract_info(youtubeUrl, download=False)
        song_name = video["track"]
        artist = video["artist"]
        reqUrl = f"https://api.spotify.com/v1/search?q={song_name} {artist}&type=track&limit=1"
        response = requests.request("GET", reqUrl, headers=self.headersList)

        if response.status_code == 200 and response.json()["tracks"]["items"]:
            trackDetails["id"] = response.json()["tracks"]["items"][0]["id"]
            trackDetails["name"] = response.json()["tracks"]["items"][0]["name"]
            return trackDetails, f"Track {song_name} found"
        return trackDetails, f"Unable to find track '{song_name}'"

    def addTracksToPlaylist(self, trackIds, playlistId):
        reqUrl = f"https://api.spotify.com/v1/playlists/{playlistId}/tracks"
        payload = json.dumps(
            {"uris": [f"spotify:track:{trackId}" for trackId in trackIds]}
        )
        response = requests.request(
            "PUT", reqUrl, data=payload, headers=self.headersList
        )
        if response.status_code == 201:
            return f"Tracks added to playlist"
        return f"Couldn't add tracks, Error: {response.status_code}"
