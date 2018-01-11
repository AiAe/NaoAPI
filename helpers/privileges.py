'''

    Privileges:
        0 - User Restricted
        1 - User
        2 - User Donator
        3 - Admin

'''

userrestricted = 1 << 0
user = 1 << 1
userdonator = 1 << 2
admin = 1 << 3


def hasuserrestricted(user_privileges):
    return (userrestricted & user_privileges) != 0


def hasuser(user_privileges):
    return (user & user_privileges) != 0


def hasuserdonator(user_privileges):
    return (userdonator & user_privileges) != 0


def hasadmin(user_privileges):
    return (admin & user_privileges) != 0
