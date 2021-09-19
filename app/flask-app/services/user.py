""" User Service """

def create(details):
    """ Create User """
    """
    {
        "email": "abcd@gmail.com",
        "age": 18,
        "python_programming_experience": "none"
    }
    """
    return True

def exists(email):
    """ Does the User exist? """
    if email == "abcd@gmail.com":
        return True
    return False
