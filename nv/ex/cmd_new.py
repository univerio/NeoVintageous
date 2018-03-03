from .tokens import TOKEN_COMMAND_NEW
from .tokens import TokenEof
from .tokens import TokenOfCommand
from NeoVintageous.nv import ex


plus_plus_translations = {
    'ff': 'fileformat',
    'bin': 'binary',
    'enc': 'fileencoding',
    'nobin': 'nobinary',
}


@ex.command('new', 'new')
class TokenCommandNew(TokenOfCommand):
    def __init__(self, params, *args, **kwargs):
        super().__init__(params, TOKEN_COMMAND_NEW, 'new', *args, **kwargs)
        self.target_command = 'ex_new'


def scan_cmd_new(state):
    params = {'++': None, 'cmd': None}

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

        raise NotImplementedError(':new not fully implemented')

    m = state.match(r'.+$')
    if m:
        params['cmd'] = m.group(0).strip()
        raise NotImplementedError(':new not fully implemented')

    return None, [TokenCommandNew(params), TokenEof()]