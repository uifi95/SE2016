# Could be prettified, maybe?
def student_check(user):
    return user.groups.filter(name="student").count() > 0

def admin_check(user):
    return user.is_staff()