# Stack Overflow for Teams SCIM-based User Activation
A SCIM API script for Stack Overflow for Teams that can automate the Activation of a list of specific existing users.


## Requirements
* A Stack Overflow for Teams instance with SCIM enabled (Basic, Business, or Enterprise)
* Python 3.8 or higher ([download](https://www.python.org/downloads/))
* Operating system: Linux, MacOS, or Windows

## Setup

[Download](https://github.com/StackExchange/so4t_scim_user_activation/archive/refs/heads/main.zip) and unpack the contents of this repository

**Installing Dependencies**

* Open a terminal window (or, for Windows, a command prompt)
* Navigate to the directory where you unpacked the files
* Install the dependencies: `pip3 install -r requirements.txt`

**Enabling and Authenticating SCIM**

To use the SCIM API, you'll first need to enable SCIM in the admin settings. Second, you'll need to generate a SCIM token to authenticate the API calls.
- [SCIM Documentation for Basic and Business](https://stackoverflowteams.help/en/articles/4538506-automated-user-provisioning-scim-overview)
- [SCIM Documentation for Enterprise](https://support.stackenterprise.co/support/solutions/articles/22000236123-system-for-cross-domain-identity-management-scim-2-0-support)

> NOTE: The SCIM token differs from the API token used for Stack Overflow for Teams API. 

## Usage

Create a file named `users.csv` in the same directory as the script. 
You can find a CSV template [here](https://github.com/StackExchange/so4t_scim_user_activation/blob/main/Templates/users.csv).
- The CSV should have a single column with no header row
- Each row can be an email address or external ID

The script will read the CSV and Activate each user found in the list. If the user is not found, the script will skip to the next user and print a message to the console.

In a terminal window, navigate to the directory where you unpacked the script. Run the script with the `--csv` flag, replacing the URL, token, and path to CSV file with your own:
* For Basic and Business: `python3 so4t_scim_user_deactivation.py --url "https://stackoverflowteams.com/c/TEAM-NAME" --token "YOUR_SCIM_TOKEN" --csv users.csv`
* For Enterprise: `python3 so4t_scim_user_deactivation.py --url "https://SUBDOMAIN.stackenterprise.co" --token "YOUR_SCIM_TOKEN" --csv users.csv`

> If API requests to the Stack Overflow for Teams server must be made through a proxy, you can use the `--proxy` flag to specify the proxy URL. Example: `python3 so4t_tag_report.py --url "https://SUBDOMAIN.stackenterprise.co" --token "YOUR_SCIM_TOKEN" --proxy "PROXY.EXAMPLE.COM:PORTNUMBER"`

## Support, security, and legal

If you encounter problems using the script, please leave feedback in the Github Issues. You can also clone and change the script to suit your needs. It is provided as-is, with no warranty or guarantee of any kind.
