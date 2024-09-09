import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import requests
from bs4 import BeautifulSoup
import phonenumbers
import re

class WebScraper:
    def __init__(self, root):
        self.root = root
        self.root.title("Web Scraper")
        self.root.geometry("800x600")  # Set window size

        # Load the background image
        self.bg_image = Image.open("C:/Users/Lenovo/Desktop/yash final/background image.jpg")
        self.bg_image = self.bg_image.resize((800, 600))
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Create a canvas and set the background image
        self.canvas = tk.Canvas(self.root, width=800, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor=tk.NW)

        self.create_widgets()
        self.style_widgets()

    def create_widgets(self):
        # Create the main frame on the canvas
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.canvas.create_window(400, 300, window=self.main_frame)  # Center the frame

        # Create the header frame
        self.header_frame = ttk.Frame(self.main_frame)
        self.header_frame.pack(pady=10)

        # Header Label
        self.header_label = ttk.Label(self.header_frame, text="Creative Web Scraper", font=('Helvetica', 20, 'bold'))
        self.header_label.pack()

        # Create and pack the URL entry widgets
        self.input_frame = ttk.Frame(self.main_frame)
        self.input_frame.pack(pady=20)

        self.url_label = ttk.Label(self.input_frame, text="Enter URL:", font=('Helvetica', 12))
        self.url_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.url_entry = ttk.Entry(self.input_frame, width=50, font=('Helvetica', 12))
        self.url_entry.grid(row=0, column=1, pady=5, padx=10)
        
        self.scrape_button = tk.Button(self.input_frame, text="Scrape", command=self.scrape, bg='#007acc', fg='white', font=('Helvetica', 12, 'bold'), relief='flat', bd=0, padx=10, pady=5)
        self.scrape_button.grid(row=0, column=2, pady=5, padx=5)
        
        self.scrape_button.bind("<Enter>", self.on_enter)
        self.scrape_button.bind("<Leave>", self.on_leave)

        # Create and pack the treeview for displaying results
        self.tree_frame = ttk.Frame(self.main_frame)
        self.tree_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(self.tree_frame, columns=('Name', 'Phone', 'Email'), show='headings', height=15)
        self.tree.heading('Name', text='Name')
        self.tree.heading('Phone', text='Phone')
        self.tree.heading('Email', text='Email')
        self.tree.column('Name', width=200)
        self.tree.column('Phone', width=150)
        self.tree.column('Email', width=250)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Add a scrollbar to the treeview
        self.scrollbar = ttk.Scrollbar(self.tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def style_widgets(self):
        # Configure styles for ttk widgets
        style = ttk.Style()
        style.configure('TLabel', font=('Helvetica', 12))
        style.configure('TButton', font=('Helvetica', 12))
        style.configure('TEntry', font=('Helvetica', 12))
        style.configure('Treeview', font=('Helvetica', 10), background="#f0f0f0", fieldbackground="#f0f0f0")
        style.configure('Treeview.Heading', font=('Helvetica', 12, 'bold'))

    def on_enter(self, e):
        self.scrape_button['background'] = '#005a9c'

    def on_leave(self, e):
        self.scrape_button['background'] = '#007acc'

    def scrape(self):
        url = self.url_entry.get()
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            self.tree.delete(*self.tree.get_children())
            names = set()
            phone_numbers = set()
            email_addresses = set()
            
            # More targeted approach to extract relevant data
            for tag in soup.find_all(['p', 'li', 'td']):
                text = tag.get_text(separator=' ', strip=True)
                if re.match(r'\b[A-Z][a-z]+ [A-Z][a-z]+\b', text):
                    names.add(text)
                # Using phonenumbers library to find and parse phone numbers
                for match in phonenumbers.PhoneNumberMatcher(text, "IN"):  # Adjust "IN" to your country code
                    phone_numbers.add(phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.E164))
                if re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text):
                    email_addresses.add(re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text).group())
            
            max_len = max(len(names), len(phone_numbers), len(email_addresses))
            names = list(names)
            phone_numbers = list(phone_numbers)
            email_addresses = list(email_addresses)

            for i in range(max_len):
                name = names[i] if i < len(names) else ''
                phone = phone_numbers[i] if i < len(phone_numbers) else ''
                email = email_addresses[i] if i < len(email_addresses) else ''
                self.tree.insert('', 'end', values=(name, phone, email))
        
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Error fetching URL: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

def main():
    root = tk.Tk()
    app = WebScraper(root)
    root.mainloop()

if __name__ == "__main__":
    main()
