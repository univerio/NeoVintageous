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

from .state import EOF
from .tokens import TokenEof
from .tokens_base import TOKEN_COMMAND_WRITE_AND_QUIT_ALL
from .tokens_base import TokenOfCommand
from NeoVintageous.nv import ex


plus_plus_translations = {
    'ff': 'fileformat',
    'bin': 'binary',
    'enc': 'fileencoding',
    'nobin': 'nobinary',
}


@ex.command('wqall', 'wqa')
@ex.command('xall', 'xa')
class TokenCommandWriteAndQuitAll(TokenOfCommand):
    def __init__(self, params, *args, **kwargs):
        super().__init__(params, TOKEN_COMMAND_WRITE_AND_QUIT_ALL, 'wqall', *args, **kwargs)
        self.addressable = True
        self.target_command = 'ex_write_and_quit_all'

    @property
    def options(self):
        return self.params['++']


def scan_command_write_and_quit_all(state):
    params = {
        '++': '',
    }

    state.skip(' ')
    state.ignore()

    c = state.consume()

    if c == '+':
        state.expect('+')
        state.ignore()
        # TODO: expect_match should work with emit()
        # https://vimhelp.appspot.com/editing.txt.html#[++opt]
        m = state.expect_match(
            r'(?:f(?:ile)?f(?:ormat)?|(?:file)?enc(?:oding)?|(?:no)?bin(?:ary)?|bad|edit)(?=\s|$)',
            lambda: Exception("E474: Invalid argument"))
        name = m.group(0)
        params['++'] = plus_plus_translations.get(name, name)
        state.ignore()

    state.expect(EOF)

    return None, [TokenCommandWriteAndQuitAll(params), TokenEof()]
