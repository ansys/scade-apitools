# Copyright © 2023 ANSYS, Inc. Unauthorized use, distribution or duplication is prohibited.

from pygments import token
from pygments.lexer import RegexLexer, words


class SwanLexer(RegexLexer):
    """Lexer for SCADE One."""

    name = 'swan'
    aliases = 'Scade One'
    filenames = ['*.swan', '*.swani']

    tokens = {
        'root': [
            (
                words(
                    (
                        # iterators
                        'fold',
                        'foldi',
                        'foldw',
                        'foldwi',
                        'forward',
                        'forwardi',
                        'map',
                        'mapfold',
                        'mapfoldi',
                        'mapfoldw',
                        'mapfoldwi',
                        'mapi',
                        'mapw',
                        'mapwi',
                        'restart',
                    ),
                    suffix=r'\b',
                ),
                token.Keyword.Builtin,
            ),
            (
                words(
                    (
                        # declarations
                        'function',
                        'node',
                        'package',
                        'sensor',
                        'type',
                        'const' 'guarantee',
                        'use',
                        'returns',
                        'specialize',
                        'where',
                        'expr',
                        'def',
                        'block',
                        'wire',
                        'group',
                        'var',
                        'let',
                        'emit',
                        'assume',
                        'guarantee',
                        'diagram',
                        'automaton',
                        'state',
                    ),
                    suffix=r'\b',
                ),
                token.Keyword.Declaration,
            ),
            (
                words(
                    (
                        # control
                        #'else',
                        'elsif',
                        'match',
                        'resume',
                        'unless',
                        'until',
                        'activate',
                    ),
                    suffix=r'\b',
                ),
                token.Keyword.Builtin,
            ),
            (
                words(
                    (
                        'clock',
                        'final',
                        'initial',
                        'inline',
                        'probe',
                    ),
                    suffix=r'\b',
                ),
                token.Keyword.Namespace,
            ),
            (
                words(
                    (
                        'false',
                        'true',
                    ),
                    suffix=r'\b',
                ),
                token.Name.Builtin,
            ),
            (
                words(
                    (
                        # misc
                        'end',
                        'every',
                        'is',
                        'tel',
                    ),
                    suffix=r'\b',
                ),
                token.Keyword.Builtin,
            ),
            (
                words(
                    (
                        # operators
                        'and',
                        'not',
                        'or',
                        'xor' 'land',
                        'lnot',
                        'lor',
                        'lsl',
                        'lsr',
                        'lxor',
                        'byname',
                        'bypos',
                        'if',
                        'then',
                        'else',
                        'case',
                        'of',
                        'last',
                        'pre',
                        'reverse',
                        'pack',
                        'transpose',
                        'window',
                        'flatten',
                        'make',
                        'merge',
                        'mod',
                        'self',
                        'when',
                        'with',
                        'default',
                    ),
                    suffix=r'\b',
                ),
                token.Operator.Word,
            ),
            (
                words(
                    (
                        # types
                        'bool',
                        'char',
                        'enum',
                        'float32',
                        'float64',
                        'int8',
                        'int16',
                        'int32',
                        'int64',
                        'uint8',
                        'uint16',
                        'uint32',
                        'uint64',
                        'numeric',
                        'float',
                        'integer',
                        'signed',
                        'unsigned',
                    ),
                    suffix=r'\b',
                ),
                token.Keyword.Type,
            ),
            (
                words(
                    (
                        'imported',
                        'open',
                        'private',
                        'public',
                        'repeat',
                        'repeati',
                        'sig',
                        'synchro',
                        'times',
                        'abstract',
                        'do',
                        'onreset',
                        'parameter',
                    ),
                    suffix=r'\b',
                ),
                token.Keyword.Reserved,
            ),
            (r'#pragma', token.Comment.Preproc, 'pragma'),  # must be before LUID
            (r'/\*', token.Comment.Multiline, 'comment'),  # must be before operators
            (r'<<', token.Generic.Strong, 'chevron'),  # must be before operators
            (r'--.*$', token.Comment.Singleline),  # must be before operators
            (r'\+|-|\*|\/|\^|=|<>|<=?|>=?|->|@|:>', token.Operator),
            (r'[0-9]+\.[0-9]*([eE][+-]?[0-9]+)?(_f(32|64))?', token.Number.Float),  # TYPED_FLOAT
            (r'[0-9]*\.[0-9]+([eE][+-]?[0-9]+)?(_f(32|64))?', token.Number.Float),  # TYPED_FLOAT
            (r'0b[01]+(_u?i(8|16|32|64))?', token.Number.Bin),  # TYPED_INTEGER
            (r'0o[07]+(_u?i(8|16|32|64))?', token.Number.Hex),  # TYPED_INTEGER
            (r'0x[0-9A-Fa-f]+(_u?i(8|16|32|64))?', token.Number.Hex),  # TYPED_INTEGER
            (r'[0-9]+(_u?i(8|16|32|64))?', token.Number.Integer),  # TYPED_INTEGER
            (r'#[a-zA-Z0-9\-_]+', token.Name.Label),  # LUID
            (r'[a-zA-Z][a-zA-Z0-9_]*', token.Name),  # ID
            (r'\s', token.Text),
            (r'\S', token.Text),
        ],
        'comment': [
            (r'[^*/]', token.Comment.Multiline),
            (r'/\*', token.Comment.Multiline, '#push'),
            (r'\*/', token.Comment.Multiline, '#pop'),
            (r'[*/]', token.Comment.Multiline),
        ],
        'pragma': [
            (r'[^#]', token.Comment.Preproc),
            (r'##', token.Comment.Preproc),
            (r'#end', token.Comment.Preproc, '#pop'),
        ],
        'chevron': [(r'>>', token.Generic.Strong, '#pop'), (r'.', token.Generic.Strong)],
    }
