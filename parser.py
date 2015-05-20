#!/usr/bin/env python

import re
import sys
import json
import logging
import eventlet
from bs4 import BeautifulSoup
from eventlet.green import urllib2
from eventlet.timeout import Timeout

logger = logging.getLogger(__name__)


def fetch_titles(links):
    """
        Receives url list
        Returns list of dictionaries where each element has two keys:
        {
            "link": "http://original_url",
            "title": "Page tile or original_url if title can not be fetched"
        }
    """

    def fetch(link):
        response = ""
        logger.debug("Start fetching {}".format(link))
        with Timeout(10, False):
            try:
                # Read up to 50K of the page
                fd = urllib2.urlopen(link)
                response = fd.read(51200)
                fd.close()
            except:
                return {
                    "link": link,
                    "title": link
                }
        logger.debug("Fetched {}".format(link))
        # Make some soup from what we got, hope <title> tag
        # is in the first 50K of the page.
        # Beautifoul soup is prefered over the simple regexp
        # because it should handle more edge cases and
        # should try to deal with encodings.
        soup = BeautifulSoup(response)
        return {
            "link": link,
            "title": soup.title.string if soup.title else link
        }

    logger.debug("Fetching titles for: {}".format(links))

    # Use GreenPool to asyncronously fetch up to ten pages
    pool = eventlet.GreenPool(size=10)
    return list(pool.imap(fetch, links))


def parse(msg):
    """
        Takes string message on input and returns information about 
        - mentions
        - emoticons
        - urls
        contained in message.
        Returns dictionary that looks as following:
        {
            "mentions": [
                "john", "jane",
            ],
            "emoticons": [
                "megusta",
                "coffe",
            ],
            "links": [
                {
                    "url": "google.com",
                    "title": "Google"
                },
            ]
        }

        - "Hi @john!" - example of mention
        - "I'm new to the team (borat)" - example of emoticon
        - "Check out http://coub.com/view/5u5n1" - example of link
    """

    mentions = set()
    emoticons = set()
    links = set()

    # Single regex should work a bit faster than 3 separate
    # Sub-regexes are joined by | operator
    regex = re.compile(
        r'(?:@(\w+))|(?:\((\w+)\))|((?:http|https)://[^\s\t\n]+)',
        re.IGNORECASE | re.UNICODE
    )

    for match in re.finditer(regex, msg):
        # For each match try to figure out which of the combined regexes
        # worked and add the captured result to the corresponding set()
        for group_number, bucket in enumerate((mentions, emoticons, links)):
            if match.group(group_number + 1):
                bucket.add(match.group(group_number + 1))

    return {
        "mentions": list(mentions),
        "emoticons": list(emoticons),
        "links": fetch_titles(links)
    }


def main():
    while True:
        try:
            msg = raw_input(
                "Please, enter message to parse or Ctr+D to quit:\n"
            )
        except:
            sys.exit(0)
        print json.dumps(parse(msg), 4)


if __name__ == "__main__":
    main()
