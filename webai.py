import streamlit as st
import requests
from bs4 import BeautifulSoup
import phonenumbers
import re

# Streamlit Web Scraper class
class WebScraper:
    def __init__(self):
        self.create_widgets()

    def create_widgets(self):
        st.title("Creative Web Scraper")

        # URL input
        url = st.text_input("Enter URL:", "")
        if st.button("Scrape"):
            if url:
                self.scrape(url)

    def scrape(self, url):
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Sets to avoid duplicate entries
            names = set()
            phone_numbers = set()
            email_addresses = set()

            # Extract relevant data from <p>, <li>, <td> tags
            for tag in soup.find_all(['p', 'li', 'td']):
                text = tag.get_text(separator=' ', strip=True)
                
                # Match names (e.g., "John Doe")
                if re.match(r'\b[A-Z][a-z]+ [A-Z][a-z]+\b', text):
                    names.add(text)
                
                # Match phone numbers using phonenumbers library
                for match in phonenumbers.PhoneNumberMatcher(text, "IN"):  # Adjust country code if needed
                    phone_numbers.add(phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.E164))
                
                # Match emails using regex
                if re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text):
                    email_addresses.add(re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text).group())

            # Convert sets to lists for easy display
            names = list(names)
            phone_numbers = list(phone_numbers)
            email_addresses = list(email_addresses)

            # Display scraped data in Streamlit
            if names or phone_numbers or email_addresses:
                st.subheader("Scraped Results")

                results = []
                max_len = max(len(names), len(phone_numbers), len(email_addresses))
                for i in range(max_len):
                    name = names[i] if i < len(names) else ''
                    phone = phone_numbers[i] if i < len(phone_numbers) else ''
                    email = email_addresses[i] if i < len(email_addresses) else ''
                    results.append((name, phone, email))

                # Display results in a dataframe
                df = {
                    'Name': [row[0] for row in results],
                    'Phone': [row[1] for row in results],
                    'Email': [row[2] for row in results]
                }

                st.write(df)
            else:
                st.warning("No data found.")

        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching URL: {e}")
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Main function
def main():
    scraper = WebScraper()

if __name__ == "__main__":
    main()
