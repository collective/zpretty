

.. image:: https://travis-ci.org/collective/zpretty.svg?branch=master
    :target: http://travis-ci.org/collective/zpretty.svg


A tool to format in a **very opinionated** way
HTML, XML and text containing XML snippets.

It satisfies a primary need: decrease the pain of diffing HTML/XML.

For this reason ``zpretty`` formats the markup
following these rules of thumb:

- maximize the vertical space/decrease the line length
- attributes should be sorted consistently
- attribute sorting is first semantic and then alphabetic

This tool understands the
`TAL language <https://en.wikipedia.org/wiki/Template_Attribute_Language>`_
and has some features dedicated to it.

.. note:: This tool is not a linter!
    If you are looking for linters safe bets are
    `Tidy <http://www.html-tidy.org/>`_ and
    `xmllint <http://xmlsoft.org/xmllint.html>`_.

.. note:: You may have parsing problems!
    ``zpretty`` will require you to close some tags like ``input`` and ``img``.

.. note:: ``zpretty`` is not clever enough to understand correctly valueless attributes!
    Some work is ongoing, but it works best with "normal" attributes.

.. note:: Lack of feature/slowness are a known issue.
    For the moment the development focused in having a working tool.
    So it works fast enough: less than a second to format a ~100k file.
    New features are planned and also huge perfomance boost can be easily
    obtained.
    Anyway ``zpretty`` is not your option for formatting large files (> 1 MB).

See `TODO section <todo_section_>`_ to know what is forecast for the future.

The source code and the issue tracker are hosted on
`GitHub <https://github.com/collective/zpretty>`_.


INSTALL
=======

The suggested instal method is using
`pip <https://pypi.python.org/pypi/pip/>`_:

::

    $ pip install zpretty


USAGE
=====

Basic usage:

::

    zpretty [-h] [-i] [file [file ...]]

    positional arguments:
      file           The list of files to prettify

    optional arguments:
      -h, --help     show this help message and exit
      -i, --inplace  format files in place (overwrite)


Example:

::

    zpretty hello_world.html


DEVELOP
=======

::

    $ git clone ...
    $ cd zpretty
    $ make

RUNNING TESTS
=============

::

    $ make test




TODO
====

.. _todo_section:

- [ ] Python 3 support ... ;)
- [ ] Command line options
- [ ] Improve performances
- [ ] Valueless attributes are not allowed in XML
- [ ] Attributes are aligned in a strange way if previous sibling has no spaces
- [ ] TBD: Style attributes should be multiline
- [ ] Fix Not Close exception
