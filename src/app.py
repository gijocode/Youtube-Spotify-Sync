import json
from spotifyClient import SpotifyClient
from youtubeClient import YoutubeClient


def getYoutubePlaylistItems(yt_obj, playlistId):
    playlistData = []
    pageToken = None
    while True:
        response = yt_obj.getPlaylistsData(playlistId, pageToken)
        pageToken = response.get("nextPageToken")

        for item in response["items"]:
            playlistData.append(item)
        if not pageToken:
            break

    return playlistData


def main():
    # Initialize variables
    tracksListToAdd = []
    playlistsIds = json.load(open("data/playlists.json"))
    youtubeWatchUrl = "https://www.youtube.com/watch?v={}"

    # Initialize YoutubeClient and SpotifyClient
    yt = YoutubeClient()
    spotify = SpotifyClient()

    # Get playlist items from youtube
    playlistData = getYoutubePlaylistItems(yt, playlistsIds["youtubePlaylistId"])

    # get spotify links to add to playlist
    for item in playlistData:
        trackDetails, msg = spotify.findTrack(
            youtubeWatchUrl.format(item["contentDetails"]["videoId"])
        )
        print(msg)
        if trackDetails:
            tracksListToAdd.append(trackDetails["id"])

    # check if playlist exists, else create new playlist
    print(spotify.createPlaylist())

    # Get list of existing tracks in playlist
    existingTrackIds = spotify.getPlaylistTracks()

    # remove duplicates from existing tracks
    if existingTrackIds:
        tracksListToAdd = [
            track for track in tracksListToAdd if track not in existingTrackIds
        ]

    # Add tracks to playlist
    if tracksListToAdd:
        print(spotify.addTracksToPlaylist(tracksListToAdd, spotify.playlistId))
    else:
        print("Your Spotify playlist is already up to date")


if __name__ == "__main__":
    main()
