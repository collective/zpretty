class _AnyIn:
    """Silly object that is used to always return True
    when checking if an item is in it.
    Used to tell BeautifulSoup to preserve whitespace in all tags
    """

    def __contains__(self, item):
        return True


ANY_IN = _AnyIn()
