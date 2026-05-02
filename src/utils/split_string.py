def split_string(string, separator, reverse=False):
    if reverse:
        parts = string.rsplit(separator, 1)
    else:
        parts = string.split(separator, 1)
    if len(parts) == 1:
        return parts[0].strip(), ""
    return parts[0].strip(), parts[1].strip()
