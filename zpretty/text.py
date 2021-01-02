def startswith_whitespace(text):
    """Check if text starts with a whitespace

    If text is not a string return False
    """
    if not isinstance(text, str):
        return False
    return text[:1].isspace()


def endswith_whitespace(text):
    """Check if text ends with a whitespace

    If text is not a string return False
    """
    if not isinstance(text, str):
        return False
    return text[-1:].isspace()


def lstrip_first_line(text):
    """lstrip only the first line of text"""
    if not text:
        return text
    if endswith_whitespace(text):
        text += " "
    lines = text.splitlines()
    lines[0] = lines[0].lstrip()
    return "\n".join(lines)


def rstrip_last_line(text):
    """rstrip only the last line of text"""
    if not text:
        return text
    if endswith_whitespace(text):
        text += " "
    lines = text.splitlines()
    lines[-1] = lines[-1].rstrip()
    return "\n".join(lines)
