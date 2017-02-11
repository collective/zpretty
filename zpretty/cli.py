# coding=utf-8
from argparse import ArgumentParser
from sys import stdout
from zpretty.prettifier import ZPrettifier


def get_parser():
    parser = ArgumentParser(
        prog='zpretty',
        description='An opinionated HTML/XML soup formatter',
        epilog=None,
    )
    parser.add_argument(
        '-i',
        '--inplace',
        help='Format in place (overwrite existing file)',
        action='store_true',
        dest='inplace',
    )
    parser.add_argument(
        'file',
        nargs='*',
        default=None,
        help='The list of files to prettify',
    )
    return parser


def run():
    ''' Prettify each filename passed in the command line
    '''
    parser = get_parser()
    config = parser.parse_args()
    for infile in config.file:
        prettifier = ZPrettifier(infile)
        prettified = prettifier().encode('utf8')
        if config.inplace:
            with open(infile, 'w') as f:
                f.write(prettified)
        else:
            stdout.write(prettified)


if __name__ == '__main__':
    run()
