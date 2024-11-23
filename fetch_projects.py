import os
import requests
import json


def read_token_and_org_id(data_file):
    """Read the token and org_id from the data file."""
    if not os.path.exists(data_file):
        raise FileNotFoundError(f"Data file '{data_file}' not found.")

    with open(data_file, "r") as file:
        try:
            data = json.load(file)
            token = data.get("token")
            org_id = data.get("org_id")
            if not token or not org_id:
                raise ValueError("Data file is missing 'token' or 'org_id'.")
            return token, org_id
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format in data file.")


def fetch_org_projects(token, org_id):
    """Fetch projects for the given organization."""
    url = f"https://api.opensolar.com/api/orgs/{org_id}/projects/"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        projects = response.json()
        print("Projects fetched successfully.")
        print(json.dumps(projects, indent=4))
        return projects
    else:
        raise Exception(
            f"Failed to fetch projects. HTTP {response.status_code}: {response.text}"
        )


if __name__ == "__main__":
    # Define file path
    data_file = "output.json"

    # Execute the workflow
    try:
        token, org_id = read_token_and_org_id(data_file)
        fetch_org_projects(token, org_id)
    except Exception as e:
        print(f"Error: {e}")
