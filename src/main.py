from DirectorClient import DirectorClient
from MentorClient import MentorClient
from MenteeClient import MenteeClient

def user_login():
    '''
    Allow the user to login to the program. Validates the user and 
    returns the role given by the user
    Accepts 'Director', 'Mentor', or 'Mentee'
    '''
    while True:
        role = input("Enter your username (director, mentor, mentee): ")
        valid_roles = {'Director', 'Mentor', 'Mentee'}

        if role.title() in valid_roles:
            return role.title()
        else:
            print("Invalid username \"" + role + "\"")

def init_client(role):
    '''
    Initialize the client for the given role
    :return: the client object for the given role
    '''
    if role == "Director":
        return DirectorClient()
    elif role == "Mentor":
        return MentorClient()
    elif role == "Mentee":
        return MenteeClient()
    else:
        raise ValueError("Internal error. Disallowed role given to 'init_client()' function")

if __name__ == "__main__":
    role = user_login()
    client = init_client(role)

    while True:
        opt = client.menu()
        client.execute(opt)

