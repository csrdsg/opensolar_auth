import os
import requests
import json


def read_credentials(credentials_file):
    """Read email and password from the credentials file."""
    if not os.path.exists(credentials_file):
        raise FileNotFoundError(f"Credentials file '{credentials_file}' not found.")

    with open(credentials_file, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format in credentials.txt.")


def fetch_token_and_user_id(credentials):
    """Authenticate and fetch token and user ID."""
    url = "https://api.opensolar.com/api-token-auth/"  # Replace if endpoint differs
    response = requests.post(url, json=credentials)

    if response.status_code == 200:
        data = response.json()
        token = data.get("token")
        user_id = data.get("user", {}).get("id")
        if not token or not user_id:
            raise ValueError("Response is missing 'token' or 'user.id'.")
        return token, user_id
    else:
        raise Exception(
            f"Failed to fetch token and user ID. HTTP {response.status_code}: {response.text}"
        )


def update_machine_user_status(token, user_id):
    """Update the user's 'is_machine_user' status."""
    url = f"https://api.opensolar.com/auth/users/{user_id}/"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {"is_machine_user": True}
    response = requests.patch(url, headers=headers, json=payload)

    if response.status_code == 200:
        print("User status updated successfully.")
        print("Response:", response.json())
    else:
        raise Exception(
            f"Failed to update user status. HTTP {response.status_code}: {response.text}"
        )


if __name__ == "__main__":
    # Define file path
    credentials_file = "credentials.txt"

    # Execute the workflow
    try:
        credentials = read_credentials(credentials_file)
        token, user_id = fetch_token_and_user_id(credentials)
        update_machine_user_status(token, user_id)
    except Exception as e:
        print(f"Error: {e}")
