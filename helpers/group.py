from helpers import privileges


def get_group(p):
    if privileges.hasuser(p):
        group = "User"

    elif privileges.hasuserdonator(p):
        group = "Donator"

    elif privileges.hasadmin(p):
        group = "Admin"

    elif privileges.hasuserrestricted(p):
        group = "Restricted"

    return {"group": group}
