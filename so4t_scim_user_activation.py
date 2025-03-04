'''
This Python script is a working proof of concept example of using Stack Overflow APIs for SCIM User Activation. 
If you run into difficulties, please leave feedback in the Github Issues.
'''


# Standard Python libraries
import argparse
import json

# Local libraries
from so4t_scim_client import ScimClient


def main():

    args = get_args()

    if not args.csv:
        print("Please provide a CSV file with a list of users to activate. Exiting.")
        raise SystemExit
    
    scim_client = ScimClient(args.token, args.url)

    # Get all users via API
    all_users = scim_client.get_all_users()
    export_to_json(all_users, "scim_users.json")

    # Create and format list of users to deactivate
    csv_users_to_activate = get_users_from_csv(args.csv)
    for user_id in csv_users_to_activate:
        account_id = scim_user_lookup(all_users, user_id)
        if account_id: # if user_lookup returns None, skip this user
            print(f"Activating user with ID {account_id}...")
            scim_client.update_user(account_id, active=False)


def get_args():

    parser = argparse.ArgumentParser(
        description="Activate existing users for Stack Overflow for Teams."
    )

    parser.add_argument(
        "--token",
        type=str,
        required=True,
        help="The SCIM token for your Stack Overflow for Teams site."
    )

    parser.add_argument(
        "--url",
        type=str,
        required=True,
        help="The base URL for your Stack Overflow for Teams site."
    )

    parser.add_argument(
        "--csv",
        type=str,
        help="Path to CSV file with a list of users to deactivate."
    )

    # parser.add_argument(
    #     "--json",
    #     type=str,
    #     help="A JSON file with a list of users to deactivate."
    # )

    #parser.add_argument('--proxy',
    #   type=str,
    #    help='Used in situations where a proxy is required for API calls. The '
    #    'argument should be the proxy server address (e.g. proxy.example.com:8080).')

    args = parser.parse_args()

    return args


def get_users_from_csv(csv_file):

    users_to_deactivate = []

    with open(csv_file, 'r') as f:
        for line in f:
            users_to_deactivate.append(line.strip())

    return users_to_deactivate


# def get_users_from_json(json_file):
    
#         with open(json_file, 'r') as f:
#             users_to_deactivate = json.load(f)
    
#         return users_to_deactivate


def scim_user_lookup(users, user_id):

    print("**********")
    if '@' in user_id: # if user_id is an email address
        print(f"Searching for user with email {user_id}...")
        for user in users:
            try:
                if user["emails"][0]["value"] == user_id:
                    print(f"Found user with email {user_id}")
                    account_id = user["id"]
                    break
            except KeyError:
                # print(f"Found SCIM user with no email address:")
                # print(user)
                continue
    else: # if user_id is an external ID
        print(f"Searching for user with external ID {user_id}...")
        for user in users:
            try:
                if user["externalId"] == user_id:
                    print(f"Found user with external ID {user_id}")
                    account_id = user["id"]
                    break
            except KeyError:
                # print(f"Found SCIM user with no external ID:")
                # print(user)
                continue
    
    try:
        print(f"Account ID for user: {account_id}")
        return account_id
    except UnboundLocalError:
        print(f"User not found. Skipping this user.")
        return None
    
def export_to_json(users, filename):

    with open(filename, 'w') as f:
        json.dump(users, f, indent=4)


if __name__ == "__main__":
    main()