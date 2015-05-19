# -*- coding: utf-8 -*-
import unittest
from parser import parse

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
Ну и немного символов в другой кодировке на всякий случай
@шапка @водка @балалайка
"""

INPUT_4 = u"""
Finally, many links in a single message:
http://hackertyper.com/
http://google.com
http://twitter.com
http://wikipedia.org
http://hipchat.com
http://yahoo.com
http://example.com
http://example.org/and/some/path/here?with=params
http://and-some-404.org
And even 10mb file
http://ipv4.download.thinkbroadband.com/10MB.zip
"""


class ParserTestCase(unittest.TestCase):

# IMPORTANT NOTE:
# This test case actually calls real world internet endpoint
# Which is of course really bad.
# In real system I would assume that I have some test utils
# That provide me an urllib2 interceptor, so I can actually
# Mock all those requests.

    def test_input_1(self):
        result = parse(INPUT_1)
        self.assertIn('peter', result['mentions'])
        self.assertIn('boss', result['mentions'])
        self.assertIn('fry', result['emoticons'])

    def test_input_2(self):
        result = parse(INPUT_2)
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
        result = parse(INPUT_3)
        self.assertIn(u'шапка', result['mentions'])
        self.assertIn(u'водка', result['mentions'])
        self.assertIn(u'балалайка', result['mentions'])
        self.assertIn(
            u'bsod90/hipchat_test \xb7 GitHub',
            result['links'][0]['title']
        )

    def test_input_4(self):
        result = parse(INPUT_4)
        links = [link['link'] for link in result['links']]
        titles = [link['title'] for link in result['links']]

        self.assertIn('http://hackertyper.com/', links)
        self.assertIn('http://google.com', links)
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
            'http://ipv4.download.thinkbroadband.com/10MB.zip',
            links
        )

        self.assertIn('Google', titles)
        self.assertIn('Yahoo', titles)
        self.assertIn('Example Domain', titles)
        self.assertIn(
            'http://ipv4.download.thinkbroadband.com/10MB.zip',
            titles
        )
