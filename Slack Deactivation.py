import argparse
import requests
import os

# These need to be moved into Jenkins secrets somehow


def get_usr_id_by_email(token, email):
    ''' This gets the user ID from slack, formats the url when called in main. uses the requests model to make the call and pass in token/email. Then takes the information from the json object and grabs the ID

    '''
    url = "https://slack.com/api/users.lookupByEmail?token={}&email={}"
    response = requests.get(url.format(token, email))
    json_response = response.json()
    user = json_response['user']
    usr_id = user['id']
    return usr_id

def set_usr_to_inactive_legacy(token, usr_id):
    ''' Takes the user ID and sets the user to inactive.

    '''
    url = "https://slack.com/api/users.admin.setInactive"
    auth_header = {"Authorization": "Bearer {}".format(token)}
    response = requests.post(url, data={"user": usr_id}, headers = auth_header)
    return response

def set_usr_to_inactive(token, usr_id): #This only works wih plus accounts. Had to rework with legacy tokens for our paid version. Can be deleted or commented out. 
    url = 'https://api.slack.com/scim/v1/Users/{}'
    auth_header = {"Authorization": "Bearer {}".format(token)}
    response = requests.delete(url.format(usr_id), headers = auth_header)
    return response

def main():
    '''Calls all functions requried to run and accepts command line arguments for the email for use in jenkins'''
    parser = argparse.ArgumentParser()
    parser.add_argument("user_email")
    args = parser.parse_args()
    email = args.user_email
    usr_id = get_usr_id_by_email(NEW_TOKEN, email)
    deactivate_usr = set_usr_to_inactive_legacy(LEGACY_TOKEN, usr_id)
    print(deactivate_usr.text)

if __name__ == '__main__':
    main()