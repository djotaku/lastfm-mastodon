# -*- coding: utf-8 -*-
"""Post top 3 artists from last.fm to Twitter."""

__author__ = "Eric Mesa"
__version__ = "0.7.3"
__license__ = "GNU GPL v3.0"
__copyright__ = "(c) 2010-2020 Eric Mesa"
__email__ = "ericsbinaryworld at gmail dot com"

import argparse
import json
import pylast  # type: ignore
import sys
import twitter  # type: ignore


def parse_args():
    """Parse the commandline arguments."""
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-w", "--weekly", action="store_true",
                       help="post your top weekly artists (default)")
    group.add_argument("-y", "--yearly", action="store_true",
                       help="post your top yearly artists")
    parser.add_argument("-j", "--json",
                        help="optional path to secrets.json file with\
                        api keys")
    return parser.parse_args()


def get_secrets(secret_location: str) -> dict:
    """Return the secrets needed to connect to twitter and last.fm

    :param secret_location: the folder containing the secrets.json file.

    :return: A dictionary containing the secrets read from the JSON file.
    """
    if secret_location:
        path = f"{secret_location}/secrets.json"
    else:
        path = "secrets.json"
    try:
        with open(path) as file:
            secrets = json.load(file)
            return secrets
    except FileNotFoundError:
        sys.tracebacklimit = 0
        print("Could not find secrets.json! Did you give the right path?")
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


def setup_twitter(secrets):
    """Return twitter API to use for post."""
    CONSUMER_KEY = secrets["twitter"]["consumer_key"]
    CONSUMER_SECRET = secrets["twitter"]["consumer_secret"]
    ACCESS_TOKEN_KEY = secrets["twitter"]["token_key"]
    ACCESS_TOKEN_SECRET = secrets["twitter"]["token_secret"]
    api = twitter.Twitter(auth=twitter.OAuth(consumer_key=CONSUMER_KEY,
                                             consumer_secret=CONSUMER_SECRET,
                                             token=ACCESS_TOKEN_KEY,
                                             token_secret=ACCESS_TOKEN_SECRET))
    return api
    # debugging
    # print api.VerifyCredentials()


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
        post = f"My top 3 #lastfm artists for the past 12 months: "\
                    f"{top_artists[0].item}({str(top_artists[0].weight)}),"\
                    f"{top_artists[1].item}({str(top_artists[1].weight)}),"\
                    f"{top_artists[2].item}({str(top_artists[2].weight)})"

    else:
        post = f"My top 3 #lastfm artists for the past 7 days: "\
                    f"{top_artists[0].item}({str(top_artists[0].weight)}),"\
                    f"{top_artists[1].item}({str(top_artists[1].weight)}),"\
                    f"{top_artists[2].item}({str(top_artists[2].weight)})"
    status = api.statuses.update(status=post)
    print(status)


def main():
    """Run the loop."""
    args = parse_args()
    secrets = get_secrets(args.json)
    top_artists = get_last_fm_top_artists(secrets, args)
    twitter_api = setup_twitter(secrets)
    make_post(twitter_api, top_artists, args)


if __name__ == "__main__":
    main()
