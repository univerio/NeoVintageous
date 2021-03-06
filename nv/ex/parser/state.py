# Copyright (C) 2018 The NeoVintageous Team (NeoVintageous).
#
# This file is part of NeoVintageous.
#
# NeoVintageous is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# NeoVintageous is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NeoVintageous.  If not, see <https://www.gnu.org/licenses/>.

import re


EOF = '__EOF__'


class ScannerState():

    # Args:
    #   :source: The string to be scanned.
    #
    # Attributes:
    #   :source (str): The string to be scanned.
    #   :position (int): The current scan position. Default is 0.
    #   :start (int): The most recent scan start. Default is 0.

    def __init__(self, source):
        self.source = source
        self.position = 0
        self.start = 0

    def consume(self):
        # Consume one character from source.
        #
        # Returns:
        #   str: One character or EOF constant ("__EOF__") if no characters left
        #       in source.
        if self.position >= len(self.source):
            return EOF

        c = self.source[self.position]

        self.position += 1

        return c

    def backup(self):
        """Backs up scanner position by 1 character."""
        self.position -= 1

    def ignore(self):
        """Discards the current span of characters that would normally be `.emit()`ted."""
        self.start = self.position

    def emit(self):
        """
        Return the `source` substring spanning from [`start`, `position`).

        Also advances `start`.
        """
        content = self.source[self.start:self.position]
        self.ignore()

        return content

    def skip(self, character):
        """Consumes @character while it matches."""
        while True:
            c = self.consume()
            if c == EOF or c != character:
                break

        if c != EOF:
            self.backup()

    def skip_run(self, characters):
        """Skips @characters while there's a match."""
        while True:
            c = self.consume()
            if c == EOF or c not in characters:
                break

        if c != EOF:
            self.backup()

    def expect(self, item, on_error=None):
        """
        Require @item to match at the current `position`.

        Raises a ValueError if @item does not match.

        @item
          A character.

        @on_error
          A function that returns an error. The error returned overrides
          the default ValueError.
        """
        c = self.consume()
        if c != item:
            if on_error:
                raise on_error()
            raise ValueError('expected {0}, got {1} instead'.format(item, c))

        return c

    def expect_match(self, pattern, on_error=None):
        """
        Require @item to match at the current `position`.

        Raises a ValueError if @item does not match.

        @pattern
          A regular expression.

        @on_error
          A function that returns an error. The error returned overrides the
          default ValueError.
        """
        m = re.compile(pattern).match(self.source, self.position)
        if m:
            self.position += m.end() - m.start()

            return m

        if not on_error:
            raise ValueError('expected match with \'{0}\', at \'{1}\''.format(pattern, self.source[self.position:]))

        raise on_error()

    def peek(self, item):
        """
        Return `True` if @item matches at the current position.

        @item
          A string.
        """
        return self.source[self.position:self.position + len(item)] == item

    def match(self, pattern):
        """
        Return the match obtained by searching @pattern.

        The current `position` will advance as many characters as the match's
        length.

        @pattern
          A regular expression.
        """
        m = re.compile(pattern).match(self.source, self.position)
        if m:
            self.position += m.end() - m.start()

            return m

        return
