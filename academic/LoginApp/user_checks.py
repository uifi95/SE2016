# Could be prettified, maybe?
def student_check(user):
    if not user.client_set.count():
        return False
    return user.client_set.first().type == "student"

def admin_check(user):
    return user.is_staff()

def teacher_check(user):
    if not user.client_set.count():
        return False
    return user.client_set.first().type == "teacher"