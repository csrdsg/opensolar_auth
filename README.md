# Fetch Token and IDs Script

This script fetches the `token`, `user_id`, and `org_id` from the OpenSolar API and saves them to `output.json`.

## Prerequisites
- Python 3.x
- `requests` library (`pip install requests`)

## Usage
1. Create a `credentials.txt` file in the project directory with the following content:
   ```json
   {
       "username": "your_email",
       "password": "your_password"
   }
