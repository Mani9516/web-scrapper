# web-scrapper
AI-Powered Email Scraper and Sender

This project is an AI-based application that scrapes websites for contact information (such as email addresses and phone numbers) and sends personalized emails automatically using Cohere's AI-based text generation model.

Features

Web Scraping: Uses BeautifulSoup and Requests to extract contact details from websites.

Email and Phone Number Detection: Automatically identifies emails and phone numbers from scraped data. AI-Powered Email Generation: Utilizes the Cohere AI model to generate personalized email content. Email Automation: Sends emails via an integrated Gmail connection. GUI Interface: Provides an intuitive interface built using Tkinter for ease of use.

How It Works

Scraping Website Data: The app scrapes a given URL for relevant contact information. Information Detection: Regular expressions and the phonenumbers library are used to detect email addresses and phone numbers. Personalized Email Generation: Cohere AI is used to generate a personalized email. Email Sending: The script automates email sending through a browser and Gmail API.
