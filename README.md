# lastfm-mastodon
Toot your weekly and/or yearly last.fm stats to Mastodon

This app is written with the assumption that you're Tooting from your own account rather than a bot account (although the steps might be similar).

- Go to your Mastodon settings page and click on Development
- Create a new app - give it whatever name you want. 
- You need the following permissions for your app:
  - read:statuses
  - write:statuses
- Then go into the settings for your application. you will the need the access token. 
- For last.fm get your key and secret at: https://www.last.fm/api/account/create (more about their API at: https://www.last.fm/api)
- At $HOME/.config/lastfm_mastodon create a secrets.json file that looks like:


```json

{
        "lastfm":
                {
                        "key": "last.fm key",
                        "secret": "last.fm secret",
                        "username": "last.fm username"
                },
        "mastodon":
            {
                    "access_token": "Mastodon Access Token",
                    "api_base_url": "URL of your Mastodon instance"
            }
}


```

For now I haven't yet created a package, so install the dependencies from requirements.txt.

Everything should be ready to go.