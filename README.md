![tests](https://github.com/collective/zpretty/workflows/tests/badge.svg)

[![image](https://coveralls.io/repos/github/collective/zpretty/badge.svg?branch=master)](https://coveralls.io/github/collective/zpretty?branch=master)

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/collective/zpretty/master.svg)](https://results.pre-commit.ci/latest/github/collective/zpretty/master)

A tool to format in a **very opinionated** way HTML, XML and text
containing XML snippets.

It satisfies a primary need: decrease the pain of diffing HTML/XML.

For this reason `zpretty` formats the markup following these rules of
thumb:

- maximize the vertical space/decrease the line length
- attributes should be sorted consistently
- attribute sorting is first semantic and then alphabetic

This tool understands the [TAL
language](https://en.wikipedia.org/wiki/Template_Attribute_Language) and
has some features dedicated to it.

This tool is not a linter! If you are looking for linters safe bets are
[Tidy](https://www.html-tidy.org/) and
[xmllint](http://xmlsoft.org/xmllint.html).

You may have parsing problems! `zpretty` will close for you some known
self closing tags, like `input` and `img`, that are allowed to be open
in HTML.

`zpretty` is not clever enough to understand correctly valueless
attributes! Some work is ongoing, but it works best with \"normal\"
attributes.

Lack of feature/slowness are a known issue. For the moment the
development focused in having a working tool. So it works fast enough:
less than a second to format a \~100k file. New features are planned and
also huge perfomance boost can be easily obtained. Anyway `zpretty` is
not your option for formatting large files (\> 1 MB).

See [TODO section](#todo_section) to know what is forecast for the
future.

The source code and the issue tracker are hosted on
[GitHub](https://github.com/collective/zpretty).

# INSTALL

The suggested installation method is using
[pip](https://pypi.python.org/pypi/pip/):

```bash
python3 -m pip install --user zpretty
```

The latest release of `zpretty` requires Python3. If you need to use
Python2.7 use `zpretty` 0.9.x.

# USAGE

Basic usage:

```console
$ zpretty -h
usage: zpretty [-h] [--encoding ENCODING] [-i] [-v] [-x] [-z] [--check]
               [paths ...]

positional arguments:
    paths                The list of paths to prettify (defaults to stdin)

options:
    -h, --help           show this help message and exit
    --encoding ENCODING  The file encoding (defaults to utf8)
    -i, --inplace        Format files in place (overwrite existing file)
    -v, --version        Show zpretty version number
    -x, --xml            Treat the input file(s) as XML
    -z, --zcml           Treat the input file(s) as XML. Follow the ZCML
                        styleguide
    --check              Return code 0 if nothing would be changed, 1 if some
                        files would be reformatted
```

Without parameters constraining the file type (e.g. `-x`, `-z`, \...)
`zpretty` will try to guess the right options for you.

Example:

```console
zpretty hello_world.html
```

# pre-commit support

`zpretty` can be used as a [pre-commit](https://pre-commit.com/) hook.
To do so, add the following to your `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/collective/zpretty
  rev: FIXME
  hooks:
    - id: zpretty
```

# VSCode extension

There is a VSCode extension that uses `zpretty`:

- [https://marketplace.visualstudio.com/items?itemName=erral.erral-zcmlLanguageConfiguration](https://marketplace.visualstudio.com/items?itemName=erral.erral-zcmlLanguageConfiguration)

Thanks to @erral for the work!

# DEVELOP

```bash
git clone ...
cd zpretty
make
```

# RUNNING TESTS

```bash
make test
```

# TODO

- [ ] Valueless attributes are not allowed in XML
- [ ] Attributes are aligned in a strange way if previous sibling has no spaces
- [ ] TBD: Style attributes should be multiline
