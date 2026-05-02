def split_string(input):
    profile_name, rest = input.split(" ", 1)

    return (profile_name.strip() or "", rest.strip() or "")