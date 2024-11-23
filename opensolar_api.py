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


def fetch_token_and_ids(credentials, output_file):
    """Fetch token, user ID, and org ID, then save to an output file."""
    url = "https://api.opensolar.com/api-token-auth/"  # Adjust API URL if different
    response = requests.post(url, json=credentials)

    if response.status_code == 200:
        # Parse the response
        data = response.json()
        token = data.get("token")
        user_id = data.get("user", {}).get("id")
        org_id = data.get("org_id")

        if not all([token, user_id, org_id]):
            raise ValueError("Response is missing 'token', 'user.id', or 'org_id'.")

        # Save to output file
        output_data = {
            "token": token,
            "user_id": user_id,
            "org_id": org_id,
        }
        with open(output_file, "w") as file:
            json.dump(output_data, file, indent=4)

        print(f"Data successfully saved to {output_file}.")
    else:
        raise Exception(
            f"Failed to fetch token and IDs. HTTP {response.status_code}: {response.text}"
        )


if __name__ == "__main__":
    # Define file paths
    credentials_file = "credentials.txt"
    output_file = "output.json"

    # Fetch and save data
    try:
        credentials = read_credentials(credentials_file)
        fetch_token_and_ids(credentials, output_file)
    except Exception as e:
        print(f"Error: {e}")
