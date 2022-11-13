# -*- coding: utf-8 -*-
"""Post top 3 artists from last.fm to Twitter."""

__author__ = "Eric Mesa"
__version__ = "0.0.1"
__license__ = "GNU GPL v3.0"
__copyright__ = "(c) 2022 Eric Mesa"
__email__ = "ericsbinaryworld at gmail dot com"

import argparse
import json
import pylast  # type: ignore
import sys
from mastodon import Mastodon
from xdgenvpy import XDGPackage


def parse_args():
    """Parse the commandline arguments."""
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-w", "--weekly", action="store_true",
                       help="post your top weekly artists (default)")
    group.add_argument("-y", "--yearly", action="store_true",
                       help="post your top yearly artists")
    return parser.parse_args()


def get_secrets() -> dict:
    """Return the secrets needed to connect to twitter and last.fm

    :return: A dictionary containing the secrets read from the JSON file.
    """
    path = xdg.XDG_CONFIG_HOME
    try:
        with open(path) as file:
            secrets = json.load(file)
            return secrets
    except FileNotFoundError:
        sys.tracebacklimit = 0
        print(f"Could not find secrets.json! Make sure to place it in {path}")
        raise


def get_last_fm_top_artists(secrets, args):
    """Return top artists from last.fm."""
    API_KEY = secrets["lastfm"]["key"]
    API_SECRET = secrets["lastfm"]["secret"]
    network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET)
    user = network.get_user("djotaku")
    if args.yearly:
        return user.get_top_artists(period='12month')
    else:
        return user.get_top_artists(period='7day')
    # debugging
    # print "Artist:", topartists[0].item
    # print "Plays:", topartists[0].weight


def setup_mastodon(secrets):
    """Return Mastodon API to use for post."""
    access_token = secrets.get("mastodon").get('access_token')
    api_base_url = secrets.get("mastodon").get("api_base_url")
    api = Mastodon(access_token=access_token, api_base_url=api_base_url)
    return api


def make_post(api, top_artists, args):
    """Post weekly or yearly top 3 artists to Twitter.

    :param api: The twitter API setup in the setup_twitter function.
    :type api: cls twitter..api.Api

    :param top_artists: contains the top artists retrieved from last.fm API.
    :type top_artists: list

    :param args: The args from the commandline, here used to determine yr|wk
    :type args: cls argparse.Namespace
    """
    if args.yearly:
        post = f"My top 3 #lastfm artists for the past 12 months: " \
               f"{top_artists[0].item}({str(top_artists[0].weight)})," \
               f"{top_artists[1].item}({str(top_artists[1].weight)})," \
               f"{top_artists[2].item}({str(top_artists[2].weight)})"

    else:
        post = f"My top 3 #lastfm artists for the past 7 days: " \
               f"{top_artists[0].item}({str(top_artists[0].weight)})," \
               f"{top_artists[1].item}({str(top_artists[1].weight)})," \
               f"{top_artists[2].item}({str(top_artists[2].weight)})"
    status = api.statuses.update(status=post)
    print(status)


def main():
    """Run the loop."""
    args = parse_args()
    xdg = XDGPackage('lastfmmastodon')
    secrets = get_secrets()
    top_artists = get_last_fm_top_artists(secrets, args)
    twitter_api = setup_twitter(secrets)
    make_post(twitter_api, top_artists, args)


if __name__ == "__main__":
    main()
