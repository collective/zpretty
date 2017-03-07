# coding=utf-8
from argparse import ArgumentParser
from sys import stdout
from zpretty.prettifier import ZPrettifier
from zpretty.xml import XMLPrettifier
from zpretty.zcml import ZCMLPrettifier


def get_parser():
    parser = ArgumentParser(
        prog='zpretty',
        description='An opinionated HTML/XML soup formatter',
        epilog=None,
    )
    parser.add_argument(
        '--encoding',
        help='The file encoding (defaults to utf8)',
        action='store',
        dest='encoding',
        default='utf8',
    )
    parser.add_argument(
        '-i',
        '--inplace',
        help='Format files in place (overwrite existing file)',
        action='store_true',
        dest='inplace',
        default=False,
    )
    parser.add_argument(
        '-x',
        '--xml',
        help='Render xml',
        action='store_true',
        dest='xml',
        default=False,
    )
    parser.add_argument(
        '-z',
        '--zcml',
        help='Follow the ZCML styleguide',
        action='store_true',
        dest='zcml',
        default=False,
    )
    parser.add_argument(
        'file',
        nargs='*',
        default='-',
        help='The list of files to prettify (defaults to stdin)',
    )
    return parser


def run():
    ''' Prettify each filename passed in the command line
    '''
    parser = get_parser()
    config = parser.parse_args()
    encoding = config.encoding
    for infile in config.file:
        if config.zcml:
            Prettifier = ZCMLPrettifier
        elif config.xml:
            Prettifier = XMLPrettifier
        else:
            Prettifier = ZPrettifier
        prettifier = Prettifier(infile, encoding=encoding)
        prettified = prettifier().encode(encoding)
        if config.inplace and not infile == '-':
            with open(infile, 'w') as f:
                f.write(prettified)
        else:
            stdout.write(prettified)


if __name__ == '__main__':
    run()
