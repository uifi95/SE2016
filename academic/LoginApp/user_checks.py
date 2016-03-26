# Could be prettified, maybe?
def student_check(user):
    return user.client_set.first().type == "student"

def admin_check(user):
    return user.is_staff()