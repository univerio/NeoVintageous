from .tokens import TOKEN_COMMAND_GLOBAL
from .tokens import TokenEof
from .tokens import TokenOfCommand
from NeoVintageous.nv import ex


@ex.command('global', 'g')
class TokenCommandGlobal(TokenOfCommand):
    def __init__(self, params, *args, **kwargs):
        super().__init__(params, TOKEN_COMMAND_GLOBAL, 'global', *args, **kwargs)
        self.addressable = True
        self.target_command = 'ex_global'

    @property
    def pattern(self):
        return self.params['pattern']

    @property
    def subcommand(self):
        return self.params['subcommand']


def scan_cmd_global(state):
    params = {'pattern': None, 'subcommand': None}

    c = state.consume()

    bang = c == '!'
    sep = c if not bang else c.consume()

    # TODO: we're probably missing legal separators.
    assert c in '!:?/\\&$', 'bad separator'

    state.ignore()

    while True:
        c = state.consume()

        if c == state.EOF:
            raise ValueError('unexpected EOF in: ' + state.source)

        if c == sep:
            state.backup()

            params['pattern'] = state.emit()

            state.consume()
            state.ignore()
            break

    command = state.match(r'.*$').group(0).strip()
    if command:
        params['subcommand'] = command

    return None, [TokenCommandGlobal(params, forced=bang), TokenEof()]