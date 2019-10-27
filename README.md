[![image](https://travis-ci.org/collective/zpretty.svg?branch=master)](https://travis-ci.org/collective/zpretty/)

[![image](https://coveralls.io/repos/github/collective/zpretty/badge.svg?branch=master)](https://coveralls.io/github/collective/zpretty?branch=master)

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
[Tidy](http://www.html-tidy.org/) and
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

The suggested instal method is using
[pip](https://pypi.python.org/pypi/pip/):

    $ pip install zpretty

The latest release of `zpretty` requires Python3. If you need to use
Python2.7 use `zpretty` 0.9.x.

# USAGE

Basic usage:

    zpretty [-h] [--encoding ENCODING] [-i] [-x] [-z] [file [file ...]]

    positional arguments:
      file                 The list of files to prettify (defaults to stdin)

    optional arguments:
      -h, --help           show this help message and exit
      --encoding ENCODING  The file encoding (defaults to utf8)
      -i, --inplace        Format files in place (overwrite existing file)
      -x, --xml            Threat the input file(s) as XML
      -z, --zcml           Threat the input file(s) as XML. Follow the ZCML
                           styleguide

Without parameters constraining the file type (e.g. [-x]{.title-ref},
[-z]{.title-ref}, \...) `zpretty` will try to guess the right options
for you.

Example:

    zpretty hello_world.html

# DEVELOP

    $ git clone ...
    $ cd zpretty
    $ make

# RUNNING TESTS

    $ make test

# TODO

- [ ] Valueless attributes are not allowed in XML
- [ ] Attributes are aligned in a strange way if previous sibling has no spaces
- [ ] TBD: Style attributes should be multiline
