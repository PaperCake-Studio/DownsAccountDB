import requests
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

def update_account(username):
    """Function to update a single account."""
    try:
        payload = {"username": username}
        headers = {'Content-Type': 'application/json'}
        response = requests.post('https://downsicient-users-api.plfront.us.kg/updateRecord', 
                               data=json.dumps(payload), 
                               headers=headers)
        tableTxt = "\t\t"
        if (len(str(payload)) > 25): tableTxt = "\t"
        return str(response.status_code) + " | " + str(payload) + tableTxt + "|\t" + response.text
    except requests.RequestException as e:
        return f"Error updating {username}: {str(e)}"

# Get all records
try:
    response = requests.get('https://downsicient-users-api.plfront.us.kg/getAllRecords')
    response.raise_for_status()
    accounts = response.json()
except requests.RequestException as e:
    print(f"Error fetching records: {str(e)}")
    exit(1)

# Update accounts in parallel using ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=75) as executor:
    # Map usernames to update tasks
    future_to_username = {executor.submit(update_account, account['username']): account['username'] for account in accounts}
    # Collect and print results as they complete
    for future in as_completed(future_to_username):
        username = future_to_username[future]
        try:
            result = future.result()
            print(result)
        except Exception as e:
            print(f"Error processing {username}: {str(e)}")

# Reminder when all updates are complete
print("\n=== All account updates completed! ===")
