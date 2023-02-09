# Changelog

3.0.0 (2023-02-09)
------------------

- The pre-commit hook now modifies fixes the files instead of just checking
  if they should be fixed
  [ale-rt]
- Fix the check behavior when multiple files are passed
  [ale-rt]
- Improve the check that sniffs html files
  (Fixes #89)
  [ale-rt]


2.4.1 (2022-10-25)
------------------

- XML files with newlines between attributes are properly formatted
  (Fixes #84)
  [ale-rt]
- Do not tamper attributes in XML as if they were a page template attribute
  (Fixes #85)
  [ale-rt]


2.4.0 (2022-10-22)
------------------

- Prevent fiddling around with custom entity declaration (Fixes #80)
  [ale-rt]
- Add support for Python 3.11.
  [ale-rt]
- Drop support for Python 3.6.
  [ale-rt]


2.3.1 (2022-09-30)
------------------

- Do not try to do anything on CDATAs (Fixes #76)
  [ale-rt]


2.3.0 (2022-09-26)
------------------

- Added a -v/--version option [ale-rt]


2.3.0a4 (2022-09-24)
--------------------

- Remove custom tree builder which is not used anymore [ale-rt]
- Fix entity sustitution in XML (Fixes #48, Refs #71) [ale-rt]


2.3.0a3 (2022-07-08)
--------------------

- Do not escape entities inside the script and style tags (Fixes #57) [ale-rt]


2.3.0a2 (2022-07-08)
--------------------

- Fix release


2.3.0a1 (2022-07-08)
--------------------

- Preserve whitespace in XML documents and `pre` elements (Fixes #64) [ale-rt]
- Improve doctype handling [ale-rt]
- Do not kill XML documents with a doctype (Fixes #47) [ale-rt]
- Support Python 3.10 [ale-rt]


2.2.0 (2021-12-06)
------------------

- Add a `--check` command line parameter (Fixes #49) [ale-rt]
- Now the package is `pre-commit` compatibile (Fixes #50) [ale-rt]


2.1.0 (2021-02-12)
------------------

- Remove unused `autofix` method [ale-rt]
- Do not render a spurious `=""` when new lines appear inside a tag (Refs. #35) [ale-rt]
- The attributes renderer knows about the element indentation
  and for indents the attributes consequently [ale-rt]
- The ZCML element has now its custom tag templates, this simplifies the code [ale-rt]
- Attributes content spanning multiple lines is not indented anymore (Refs. #17) [ale-rt]
- Improved sorting for zcml attributes (Refs. #11) [ale-rt]
- Code is compliant with black 20.8b1 [ale-rt]
- Switch to pytest for running tests [ale-rt]
- Upgrade dev requirements [ale-rt]
- Support Python 3.9 [ale-rt]


## 2.0.0 (2020-05-28)

- Updated the list of self closing elements and boolean attributes [ale-rt]


## 1.0.3 (2020-05-22)

- Fix unwanted newlines (#20)


## 1.0.2 (2019-11-03)

- In Python3.8 quotes in attributes were escaped
- Fix output again on file and stdout [ale-rt]

## 1.0.1 (2019-10-28)

- Fix output on file [ale-rt]

## 1.0.0 (2019-10-27)

- Support Python3 only [ale-rt]

## 0.9.3 (2017-05-06)

- Last release that supports Python2.7
- Fix text method
- Preserve entities in text
- Added an `--encoding` parameter
- Added an `--xml` parameter to force xml parsing
- Choose the better parser according to the given filename if no parser is forced
- Process stdin if `-` is in the arguments or no arguments are passed [ale-rt]

## 0.9.2 (2017-02-27)

- Small modification for the order of the zcml attributes
- Auto add a new line to the end of the prettified files
- Self heal open self closing tag. [ale-rt]

## 0.9.1.1 (2017-02-18)

- Fixed bad release. [ale-rt]

## 0.9.1 (2017-02-18)

- Initial support for zcml style guide (\#3). [ale-rt]

## 0.9.0 (2017-02-11)

- Initial release. [ale-rt]
