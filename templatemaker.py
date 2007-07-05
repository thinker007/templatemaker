r"""
templatemaker.py

Copyright (c) 2007 Adrian Holovaty
License: BSD

See readme.txt for full documentation.
"""

from _templatemaker import make_template, marker
import re

# The marker character lives in _templatemaker.marker() so we don't have
# to define it in more than one place.
MARKER = marker()

unwanted_tags_re = re.compile(r'(?si)<\s*?(script|style|noscript)\b.*?</\1>')

class NoMatch(Exception):
    pass

class Template(object):
    def __init__(self, tolerance=0):
        self._brain = None
        self._tolerance = tolerance
        self.version = 0

    def clean(self, text):
        """
        Strips any unwanted stuff from the given Sample String, in order to
        make templates more streamlined.
        """
        text = unwanted_tags_re.sub('', text)
        text = re.sub(r'\r\n', '\n', text)
        return text

    def learn(self, text):
        """
        Learns the given Sample String.

        Returns True if this Sample String created more holes in the template.
        Returns None if this is the first Sample String in this template.
        Otherwise, returns False.
        """
        text = self.clean(text)
        text = text.replace(MARKER, '')
        self.version += 1
        if self._brain is None:
            self._brain = text
            return None
        old_holes = self.num_holes()
        self._brain = make_template(self._brain, text, self._tolerance)
        return self.num_holes() > old_holes

    def as_text(self, custom_marker='{{ HOLE }}'):
        """
        Returns a display-friendly version of the template, using the
        given custom_marker to mark template holes.
        """
        return self._brain.replace(MARKER, custom_marker)

    def num_holes(self):
        """
        Returns the number of holes in this template.
        """
        return self._brain.count(MARKER)

    def extract(self, text):
        """
        Given a bunch of text that is marked up using this template, extracts
        the data.

        Returns a tuple of the raw data, in the order in which it appears in
        the template. If the text doesn't match the template, raises NoMatch.
        """
        text = self.clean(text)
        regex = '(?s)' + re.escape(self._brain).replace(re.escape(MARKER), '(.*?)')
        m = re.search(regex, text)
        if m:
            return m.groups()
        raise NoMatch

    def from_directory(cls, dirname, tolerance=0):
        """
        Classmethod that learns all of the files in the given directory name.
        Returns the Template object.
        """
        import os
        t = cls(tolerance)
        for f in os.listdir(dirname):
            print t.learn(open(os.path.join(dirname, f)).read())
        return t
    from_directory = classmethod(from_directory)
