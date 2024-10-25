import requests

# Function to fetch SKU data
def fetch_sku_data(sku):
    try:
        # URL of your Flask server with SKU query
        url = f'http://<your-pi-host-ip>:5003/convert_sku?sku={sku}'
        print(f"Fetching SKU data for {sku}...")

        # Make GET request
        response = requests.get(url)

        # Check if request was successful
        if response.status_code == 200:
            print("Data fetched successfully!")
            data = response.json()

            # If data is not empty
            if data:
                # Assuming the first result is desired
                result = data[0]
                print(f"Old SKU: {result.get('Old SKU')}")
                print(f"New SKU: {result.get('New SKU')}")
                print(f"Description: {result.get('Description')}")
            else:
                print("No SKU found.")
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")

# Example usage
sku = 'ED-ADEL-RG-25g-3'  # Replace this with your SKU input
fetch_sku_data(sku)
