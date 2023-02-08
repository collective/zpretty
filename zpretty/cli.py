from argparse import ArgumentParser
from os.path import splitext
from pathlib import Path
from sys import stderr
from sys import stdout
from zpretty.prettifier import ZPrettifier
from zpretty.xml import XMLPrettifier
from zpretty.zcml import ZCMLPrettifier

import re


try:
    # Python >= 3.8
    from importlib.metadata import version

    version = version("zpretty")
except ImportError:
    # Python < 3.8
    from pkg_resources import get_distribution

    version = get_distribution("zpretty").version


class CLIRunner:
    """A class to run zpretty from the command line"""

    _default_include = r"\.(html|pt|xml|zcml)$"
    _default_exclude = (
        r"/(\.direnv|\.eggs|\.git|\.hg|\.mypy_cache|\.nox|\.tox|\.venv|venv|"
        r"\.svn|\.ipynb_checkpoints|_build|buck-out|build|dist|__pypackages__)/"
    )

    def __init__(self):
        self.errors = []
        self.config = self.parser.parse_args()

    @property
    def parser(self):
        """The parser we are using to parse the command line arguments"""
        parser = ArgumentParser(
            prog="zpretty",
            description="An opinionated HTML/XML soup formatter",
            epilog=f"The default exclude pattern is: `{self._default_exclude}`",
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
            help="Treat the input file(s) as XML",
            action="store_true",
            dest="xml",
            default=False,
        )
        parser.add_argument(
            "-z",
            "--zcml",
            help="Treat the input file(s) as XML. Follow the ZCML styleguide",
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
            "--include",
            help=(
                f"A regular expression that matches files and "
                f" directories that should be included on recursive searches. "
                f"An empty value means all files are included regardless of the name. "
                f"Use forward slashes for directories on all platforms (Windows, too). "
                f"Exclusions are calculated first, inclusions later. "
                f"[default: {self._default_include}]"
            ),
            action="store",
            dest="include",
            default=self._default_include,
        )
        parser.add_argument(
            "--exclude",
            help=(
                f"A regular expression that matches files and "
                f"directories that should be excluded on "
                f"recursive searches. An empty value means no "
                f"paths are excluded. Use forward slashes for "
                f"directories on all platforms (Windows, too). "
                f"Exclusions are calculated first, inclusions "
                f"later. [default: {self._default_exclude}] "
            ),
            action="store",
            dest="exclude",
            default=self._default_exclude,
        )

        parser.add_argument(
            "--extend-exclude",
            help=(
                "Like --exclude,  but adds additional files "
                "and directories on top of the excluded ones. "
                "(Useful if you simply want to add to the default)"
            ),
            action="store",
            dest="extend_exclude",
            default=None,
        )
        parser.add_argument(
            "paths",
            nargs="*",
            default="-",
            help="The list of files or directory to prettify (defaults to stdin). "
            "If a directory is passed, all files and directories matching the regular "
            "expression passed to --include will be prettified.",
        )
        return parser

    def choose_prettifier(self, path):
        """Choose the best prettifier given the config and the input file"""
        config = self.config
        if config.zcml:
            return ZCMLPrettifier
        if config.xml:
            return XMLPrettifier
        ext = splitext(path)[-1].lower()
        if ext == ".xml":
            return XMLPrettifier
        if ext == ".zcml":
            return ZCMLPrettifier
        return ZPrettifier

    @property
    def good_paths(self):
        """Return a list of good paths"""
        good_paths = []

        try:
            exclude = re.compile(self.config.exclude)
        except re.error:
            exclude = re.compile(self._default_exclude)
            self.errors.append(
                f"Invalid regular expression for --exclude: {self.config.exclude!r}"
            )

        try:
            extend_exclude = self.config.extend_exclude and re.compile(
                self.config.extend_exclude
            )
        except re.error:
            extend_exclude = None
            self.errors.append(
                f"Invalid regular expression for --extend-exclude: "
                f"{self.config.extend_exclude!r}"
            )

        try:
            include = re.compile(self.config.include)
        except re.error:
            include = re.compile(self._default_include)
            self.errors.append(
                f"Invalid regular expression for --include: {self.config.include!r}"
            )

        for path in self.config.paths:
            # use Pathlib to check if the file exists and it is a file
            if path == "-":
                good_paths.append(path)
                continue
            if exclude.match(path) or (extend_exclude and extend_exclude.match(path)):
                continue

            path_instance = Path(path)
            if path_instance.is_file():
                good_paths.append(path)
            elif path_instance.is_dir():
                for file in path_instance.glob("**/*"):
                    if file.is_file():
                        if (
                            include.search(str(file))
                            and not exclude.search(str(file))
                            and not (
                                extend_exclude and extend_exclude.search(str(file))
                            )
                        ):
                            good_paths.append(str(file))
            else:
                self.errors.append(f"Cannot open: {path}")

        return sorted(good_paths)

    def run(self):
        """Prettify each filename passed in the command line"""
        encoding = self.config.encoding
        for path in self.good_paths:
            # use Pathlib to check if the file exists and it is a file
            Prettifier = self.choose_prettifier(path)
            prettifier = Prettifier(path, encoding=encoding)
            if self.config.check:
                if not prettifier.check():
                    self.errors.append(f"This file would be rewritten: {path}")
                continue
            prettified = prettifier()
            if self.config.inplace and not path == "-":
                with open(path, "w") as f:
                    f.write(prettified)
                continue
            stdout.write(prettified)

        if self.errors:
            message = "\n".join(self.errors)
            stderr.write(f"{message}\n")
            exit(1)


def run():
    CLIRunner().run()  # pragma: no cover


if __name__ == "__main__":
    run()  # pragma: no cover
