# Open source libraries
import requests


class ScimClient:

    def __init__(self, token, url, proxy=None):
        self.base_url = url
        self.token = token
        self.headers = {
            'Authorization': f"Bearer {self.token}"
        }
        if "stackoverflowteams.com" in self.base_url: # For Basic and Business tiers
            self.soe = False
            self.scim_url = f"{self.base_url}/auth/scim/v2/users"
        else: # For Enterprise tier
            self.soe = True
            self.scim_url = f"{self.base_url}/api/scim/v2/users"
        
        self.proxies = {'https': proxy} if proxy else {'https': None}


    def get_user(self, account_id):
        # Get a single user by account ID

        scim_url = f"{self.scim_url}/{account_id}"
        response = requests.get(scim_url, headers=self.headers, proxies=self.proxies)

        if response.status_code == 404:
            print(f"User with account ID {account_id} not found.")
            return None

        elif response.status_code != 200:
            print(f"API call failed with status code: {response.status_code}.")
            print(response.text)
            return None

        else:
            print(f"Retrieved user with account ID {account_id}")
            return response.json()
    

    def get_all_users(self):
        '''
        Get all users via SCIM API
        SCIM API returns a max of 100 items per call, so we need to paginate through the results
        
        Example response for 1 user:
        {
            'active': False,
            'name': {'givenName': 'Bruce', 'familyName': 'Banner'},
            'emails': [
                    {'primary': True, 'value': 'bbanner@company.com'}
                ],
            'schemas': ['urn:ietf:params:scim:schemas:core:2.0:User'],
            'meta': {
                'created': '2017-05-30T21:45:30.740Z',
                'location': 'https://demo.stackenterprise.co/api/scim/v2/users/8'},
            'id': '8',
            'externalId': '00ufmj2tmtWu2X',
            'userType': 'Admin',
            'profileUrl': 'https://demo.stackenterprise.co/accounts/8',
            'displayName': 'Bruce Banner',
            'userName': 'bbanner@company.com'
        }
        '''

        params = {
            "count": 100,
            "startIndex": 1,
        }

        items = []
        while True: # Keep performing API calls until all items are received
            print(f"Getting 100 results from {self.scim_url} with startIndex of {params['startIndex']}")
            response = requests.get(self.scim_url, headers=self.headers, params=params, 
                                    proxies=self.proxies)
            if response.status_code != 200:
                print(f"API call failed with status code: {response.status_code}.")
                print(response.text)
                break

            items_data = response.json().get('Resources')
            items += items_data

            params['startIndex'] += params['count']
            if params['startIndex'] > response.json().get('totalResults'):
                break

        return items


    def update_user(self, account_id, active=None, role=None):
        # Update a user's active status or role via SCIM API
        # Role changes require an admin setting to allow SCIM to modify user roles
        # `role` can be one of the following: Registered, Moderator, Admin
        # if another role is passed, it will be ignored (and still report HTTP 200)
        # `active` can be True or False

        valid_roles = ["Registered", "Moderator", "Admin"]

        scim_url = f"{self.scim_url}/{account_id}"
        payload = {}
        if active is not None:
            payload['active'] = active
        if role is not None:
            if role in valid_roles:
                payload['userType'] = role
            else:
                print(f"Invalid role: {role}. Valid roles are: {valid_roles}")
                return

        response = requests.put(scim_url, headers=self.headers, json=payload, proxies=self.proxies)

        if response.status_code == 404:
            print(f"User with account ID {account_id} not found.")
        elif response.status_code != 200:
            print(f"API call failed with status code: {response.status_code}.")
            print(response.text)
        else:
            print(f"Updated user with account ID {account_id}")


    def delete_user(self, account_id, retries=0):
        # By default, deleting users via SCIM is disabled. To enable it, open a support ticket.
        # Deleting a user via SCIM requires the user's account ID (not user ID)
        
        scim_url = f"{self.scim_url}/{account_id}"

        print(f"Sending DELETE request to {scim_url}")
        response = requests.delete(scim_url, headers=self.headers, proxies=self.proxies)

        if response.status_code == 400:
            # 400 Error responses:
                # {"ErrorMessage":"You cannot delete or destroy System Accounts."}
            print(f"Failed to delete user with account ID {account_id}")
            print(response.json().get('ErrorMessage'))

        elif response.status_code == 404:
            print(f"User with account ID {account_id} not found.")

        elif response.status_code == 403:
            ### NEED TO TEST THIS TO BE SURE
            print(f"Deleting users via SCIM is disabled. To enable it, open a support ticket.")

        elif response.status_code == 500:
            # 500 Error responses:
                # {"ErrorMessage":"Moderators cannot be deleted - tried to delete <UserName>. 
                    # Adjust role to User."}
                # "SCIM user modification failed - unknown user"
            if "Adjust role to User" in response.json().get('ErrorMessage'):
                print(f"User with account ID {account_id} cannot be deleted because they're "
                        "a moderator or admin.")
                print("Reducing their role to User...")
                self.update_user(account_id, role="Registered")
                if retries < 3:
                    print("Retrying delete...")
                    self.delete_user(account_id, retries+1)
                else:
                    print("Max retries reached. Aborting deletion.")
            else:
                print(f"Failed to delete user with account ID {account_id}")
                print(response.json().get('ErrorMessage'))

        elif response.status_code != 204:
            print(f"API call failed with status code: {response.status_code}.")
            print(response.text)

        else:
            print(f"Deleted user with account ID {account_id}")  
