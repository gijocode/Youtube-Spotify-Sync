# -*- coding: utf-8 -*-

# Sample Python code for youtube.playlistItems.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python


import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]


class YoutubeClient:
    def __init__(self):

        self.api_service_name = "youtube"
        self.api_version = "v3"
        self.client_secrets_file = "data/yt_secret.json"
        self.youtube = self.login()

    def login(self):
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        try:
            # Get credentials and create an API client
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                self.client_secrets_file, scopes
            )
            credentials = flow.run_console()
            youtube = googleapiclient.discovery.build(
                self.api_service_name, self.api_version, credentials=credentials
            )
            return youtube

        except Exception as e:
            print(f"Error: {e}")
            raise SystemExit(1)

    def getPlaylistsData(self, playlistId, nextPageToken=None):
        request = self.youtube.playlistItems().list(
            part="snippet,id,contentDetails",
            playlistId=playlistId,
            pageToken=nextPageToken,
        )

        response = request.execute()
        return response
