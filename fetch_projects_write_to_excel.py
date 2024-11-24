import sys
import pandas as pd
from datetime import datetime
from fetch_projects import read_token_and_org_id, fetch_org_projects


def save_projects_to_excel(projects, output_file):
    """Save projects to an Excel file."""
    if not projects:
        print("No projects to save.")
        return

    # Convert projects data into a pandas DataFrame
    df = pd.DataFrame(projects)

    # Save the DataFrame to an Excel file
    df.to_excel(output_file, index=False)
    print(f"Projects saved to {output_file}.")


if __name__ == "__main__":
    # Define file paths
    data_file = "output.json"

    # Check if an output file argument is provided
    if len(sys.argv) > 1:
        excel_file = sys.argv[1]
    else:
        # Use current date in ISO format if no argument is provided
        current_date = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
        excel_file = f"projects_{current_date}.xlsx"

    # Execute the workflow
    try:
        # Import token and org_id using the shared function
        token, org_id = read_token_and_org_id(data_file)

        # Fetch projects using the shared function
        projects = fetch_org_projects(token, org_id)

        # Save projects to Excel
        save_projects_to_excel(projects, excel_file)
    except Exception as e:
        print(f"Error: {e}")
