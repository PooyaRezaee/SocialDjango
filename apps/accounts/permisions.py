def IsFollowerOrSelfPermissions(user_requested,user_target):
    if user_requested in user_target.followers_real or user_requested == user_target:
        return True
    else:
        return False
