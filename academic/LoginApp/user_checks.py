# Could be prettified, maybe?
def student_check(user):
    if not user.client_set.count():
        return False
    return user.client_set.first().type == "student"


def admin_check(user):
    if not user.client_set.count():
        return False
    return user.groups.filter(name="staff").exists()


def teacher_check(user):
    if not user.client_set.count():
        return False
    return user.groups.filter(name="teacher").exists()


def dchief_check(user):
    if not user.client_set.count():
        return False
    return user.groups.filter(name="dchief").exists()
