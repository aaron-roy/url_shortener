import requests
from tabulate import tabulate



api_base_url = 'http://127.0.0.1:8000'


def pretty_print_url_map(url_map):
    # Define the headers for the table
    headers = ['long_url', 'short_url', 'clicks']
    
    # Convert list of dicts into list of tuples
    table_data = [(entry['long_url'], entry['short_url'], entry['clicks']) for entry in url_map]
    
    # Use tabulate to format and print the data
    print(tabulate(table_data, headers=headers, tablefmt='pretty'))

def main():

    user_input = input("Please enter a URL (Enter nothing to quit or C to see Clicks): ")

    while user_input:
        
        if user_input == "C":
            response = requests.get(f'{api_base_url}/url_map/')
            pretty_print_url_map(response.json())
        else:
            response = requests.post(
                f'{api_base_url}/shorten/',  # POST to the correct endpoint
                json={"url": user_input}  # Pass the URL in the JSON body
            )
            print(f"Shortened URL: {response.json()['shortened_url']}")
        user_input = input("Please enter a URL (Enter nothing to quit or C to see Clicks): ")
        

    print("Test ended!")


if __name__ == '__main__':
    main()