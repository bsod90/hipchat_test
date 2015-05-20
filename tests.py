# -*- coding: utf-8 -*-
import mock
import unittest
from StringIO import StringIO

INPUT_1 = u"""
Hey @boss,
how about raising my and @peter's salary? (fry)
"""

INPUT_2 = u"""
Congratulations, it's Friday already!
(beer) (beer) (beer) to all and some cats to finish the day:
http://procatinator.com
(pizza) (pizza) (pizza)
"""

INPUT_3 = u"""
Here's the link to my HipChat test task solution:
https://github.com/bsod90/hipchat_test
Ну и немного не ACSII символов на всякий случай
@водка @матрешка @балалайка
"""

INPUT_4 = u"""
Finally, many links in a single message:
http://hackertyper.com
https://google.com
http://twitter.com
http://wikipedia.org
http://hipchat.com
http://yahoo.com
http://example.com
http://example.org/and/some/path/here?with=params
http://and-some-404.org
And even 5mb file
http://web4host.net/5MB.zip
"""


def urlopen_file_mock(link):
    """
        This mock helps avoiding making real HTTP requests.
        Instead of opening the internet connection it just looks for
        a corresponding file in ./test_data folder.
        Returns empty file-like object if file has not been found.
    """
    # Cut off the schema prefix
    link = link.replace("http://", "").replace("https://", "").strip()

    # Append index.html when URL does not have a file suffix
    suffixes = ("/", ".com", ".org", ".net", ".ru")
    for suffix in suffixes:
        if link.endswith(suffix):
            if link[-1] != "/":
                link += "/"
            link = link + "index.html"
    try:
        test_file = open("./test_data/" + link, 'r')
        return test_file
    except IOError:
        return StringIO("")


@mock.patch('eventlet.green.urllib2.urlopen', urlopen_file_mock)
class ParserTestCase(unittest.TestCase):

    def setUp(self):
        # This is actually a hack.
        # For some reason @mock.patch('parser.urllib2') does not work.
        # So, we have to mock eventlet.green.urllib2 insted and we
        # Should do it before loading parser module
        from parser import parse
        self.parse = parse

    def test_input_1(self):
        result = self.parse(INPUT_1)

        self.assertIn('peter', result['mentions'])
        self.assertIn('boss', result['mentions'])
        self.assertIn('fry', result['emoticons'])

    def test_input_2(self):
        result = self.parse(INPUT_2)

        self.assertIn('beer', result['emoticons'])
        self.assertIn('pizza', result['emoticons'])
        self.assertIn(
            'http://procatinator.com',
            result['links'][0]['link']
        )
        self.assertIn(
            'procatinator',
            result['links'][0]['title']
        )

    def test_input_3(self):
        result = self.parse(INPUT_3)

        self.assertIn(u'матрешка', result['mentions'])
        self.assertIn(u'водка', result['mentions'])
        self.assertIn(u'балалайка', result['mentions'])
        self.assertIn(
            u'bsod90/hipchat_test \xb7 GitHub',
            result['links'][0]['title']
        )

    def test_input_4(self):
        result = self.parse(INPUT_4)

        links = [link['link'] for link in result['links']]
        titles = [link['title'] for link in result['links']]

        self.assertIn('http://hackertyper.com', links)
        self.assertIn('https://google.com', links)
        self.assertIn('http://twitter.com', links)
        self.assertIn('http://wikipedia.org', links)
        self.assertIn('http://hipchat.com', links)
        self.assertIn('http://yahoo.com', links)
        self.assertIn('http://example.com', links)
        self.assertIn(
            'http://example.org/and/some/path/here?with=params',
            links
        )
        self.assertIn('http://and-some-404.org', links)
        self.assertIn(
            'http://web4host.net/5MB.zip',
            links
        )

        self.assertIn('Google', titles)
        self.assertIn('Yahoo', titles)
        self.assertIn('Wikipedia', titles)
        self.assertIn('Example Domain', titles)
        self.assertIn(
            'http://web4host.net/5MB.zip',
            titles
        )
