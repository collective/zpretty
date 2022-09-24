from argparse import ArgumentParser
from os.path import splitext
from sys import stderr
from sys import stdout
from zpretty.prettifier import ZPrettifier
from zpretty.xml import XMLPrettifier
from zpretty.zcml import ZCMLPrettifier


try:
    # Python >= 3.8
    from importlib.metadata import version

    version = version("zpretty")
except ImportError:
    # Python < 3.8
    from pkg_resources import get_distribution

    version = get_distribution("zpretty").version


def get_parser():
    parser = ArgumentParser(
        prog="zpretty",
        description="An opinionated HTML/XML soup formatter",
        epilog=None,
    )
    parser.add_argument(
        "--encoding",
        help="The file encoding (defaults to utf8)",
        action="store",
        dest="encoding",
        default="utf8",
    )
    parser.add_argument(
        "-i",
        "--inplace",
        help="Format files in place (overwrite existing file)",
        action="store_true",
        dest="inplace",
        default=False,
    )
    parser.add_argument(
        "-v",
        "--version",
        help="Show zpretty version number",
        action="version",
        version=f"zpretty {version}",
    )
    parser.add_argument(
        "-x",
        "--xml",
        help="Threat the input file(s) as XML",
        action="store_true",
        dest="xml",
        default=False,
    )
    parser.add_argument(
        "-z",
        "--zcml",
        help="Threat the input file(s) as XML. Follow the ZCML styleguide",
        action="store_true",
        dest="zcml",
        default=False,
    )
    parser.add_argument(
        "--check",
        help=(
            "Return code 0 if nothing would be changed, "
            "1 if some files would be reformatted"
        ),
        action="store_true",
        dest="check",
        default=False,
    )
    parser.add_argument(
        "file",
        nargs="*",
        default="-",
        help="The list of files to prettify (defaults to stdin)",
    )
    return parser


def choose_prettifier(config, infile):
    """Choose the best prettifier given the config and the input file"""
    if config.zcml:
        return ZCMLPrettifier
    if config.xml:
        return XMLPrettifier
    ext = splitext(infile)[-1].lower()
    if ext == ".xml":
        return XMLPrettifier
    if ext == ".zcml":
        return ZCMLPrettifier
    return ZPrettifier


def run():
    """Prettify each filename passed in the command line"""
    parser = get_parser()
    config = parser.parse_args()
    encoding = config.encoding
    for infile in config.file:
        Prettifier = choose_prettifier(config, infile)
        prettifier = Prettifier(infile, encoding=encoding)
        if config.check:
            if not prettifier.check():
                stderr.write(f"This file would be rewritten: {infile}\n")
                exit(1)
            continue
        prettified = prettifier()
        if config.inplace and not infile == "-":
            with open(infile, "w") as f:
                f.write(prettified)
            continue
        stdout.write(prettified)


if __name__ == "__main__":
    run()  # pragma: no cover
