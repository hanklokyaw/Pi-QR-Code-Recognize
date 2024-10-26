import requests
from RPLCD.i2c import CharLCD


lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=20, rows=4, dotsize=8)
lcd.clear()

# Initialize two LCDs with unique addresses
lcd1 = CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=20, rows=4, dotsize=8)
lcd2 = CharLCD(i2c_expander='PCF8574', address=0x3F, port=1, cols=20, rows=4, dotsize=8)

def display_on_lcds(text1, text2):
    # Clear both LCDs
    lcd1.clear()
    lcd2.clear()

    # Write to lcd1
    lcd1.cursor_pos = (0, 0)
    lcd1.write_string(text1[:20])  # Ensure text fits in 20 characters
    lcd1.cursor_pos = (1, 0)
    lcd1.write_string(text1[20:40])

    # Write to lcd2
    lcd2.cursor_pos = (0, 0)
    lcd2.write_string(text2[:20])
    lcd2.cursor_pos = (1, 0)
    lcd2.write_string(text2[20:40])

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
