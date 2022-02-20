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


def removeDuplicates(existingTracks, tracksToAdd):
    for track in existingTracks:
        if track in tracksToAdd:
            tracksToAdd.remove(track)
    return tracksToAdd


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

    # Check if tracks already exist in playlist
    # If they do, remove them from tracksListToAdd
    existingTrackIds = spotify.getPlaylistTracks()
    if existingTrackIds:
        tracksListToAdd = removeDuplicates(existingTrackIds, tracksListToAdd)

    # Add tracks to playlist
    if tracksListToAdd:
        print(spotify.addTracksToPlaylist(tracksListToAdd, spotify.playlistId))
    else:
        print("Your Spotify playlist is already up to date")


if __name__ == "__main__":
    main()
