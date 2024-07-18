import os
import threading
import time
import tkinter as tk
from tkinter import filedialog, messagebox
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import datetime

SCOPES = ['https://mail.google.com/']

class GmailCleanerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gmail Cleaner")
        self.service = None
        self.setup_ui()

    def setup_ui(self):
        tk.Button(self.root, text="Authenticate Credentials", command=self.authenticate).pack(pady=10)
        tk.Button(self.root, text="Or Load Token Directly", command=self.load_token_directly).pack(pady=10)
        tk.Label(self.root, text="Search Subject (optional):").pack()
        self.subject_entry = tk.Entry(self.root, width=50)
        self.subject_entry.pack(pady=5)
        tk.Label(self.root, text="From Email ID:").pack()
        self.from_email_entry = tk.Entry(self.root, width=50)
        self.from_email_entry.pack(pady=5)
        tk.Label(self.root, text="From Email Filter:").pack()
        self.from_email_filter_entry = tk.Entry(self.root, width=50)
        self.from_email_filter_entry.pack(pady=5)
        tk.Label(self.root, text="Delete Emails Before Date (YYYY/MM/DD):").pack()
        self.before_date_entry = tk.Entry(self.root, width=50)
        self.before_date_entry.pack(pady=5)
        tk.Button(self.root, text="Delete Emails", command=self.delete_emails).pack(pady=10)
        tk.Button(self.root, text="Clear Promotions", command=lambda: self.clear_category('promotions')).pack(pady=5)
        tk.Button(self.root, text="Clear Social", command=lambda: self.clear_category('social')).pack(pady=5)
        self.output_text = tk.Text(self.root, height=10, width=70)
        self.output_text.pack(pady=10)

    def authenticate(self):
        creds = None
        token_path = 'token.json'

        credentials_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if not credentials_path:
            messagebox.showerror("Error", "Please select a valid JSON file for credentials.")
            return

        flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
        creds = flow.run_local_server(port=0)

        with open(token_path, 'w') as token:
            token.write(creds.to_json())

        self.service = build('gmail', 'v1', credentials=creds)
        messagebox.showinfo("Authentication", "Successfully authenticated with Gmail API.")

    def load_token_directly(self):
        token_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if not token_path:
            messagebox.showerror("Error", "Please select a valid token JSON file.")
            return

        try:
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)
            if creds and creds.valid:
                self.service = build('gmail', 'v1', credentials=creds)
                messagebox.showinfo("Token Load", "Successfully loaded token and authenticated with Gmail API.")
            else:
                messagebox.showerror("Error", "The token is invalid or expired.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while loading the token: {e}")

    def set_of_messages_matching_query(self, query):
        try:
            response = self.service.users().messages().list(userId='me', q=query).execute()
            messages = response.get('messages', [])
            while 'nextPageToken' in response:
                page_token = response['nextPageToken']
                response = self.service.users().messages().list(userId='me', q=query, pageToken=page_token).execute()
                messages.extend(response.get('messages', []))
            return {msg['id'] for msg in messages}
        except HttpError as error:
            messagebox.showerror("Error", f"An error occurred: {error}")
            return set()

    def delete_emails(self):
        self.output_text.delete(1.0, tk.END)
        if not self.service:
            messagebox.showerror("Error", "Please authenticate first.")
            return

        subject = self.subject_entry.get().strip()
        from_email = self.from_email_entry.get().strip()
        from_email_filter = self.from_email_filter_entry.get().strip()
        before_date = self.before_date_entry.get().strip()

        if not subject and not from_email and not from_email_filter and not before_date:
            messagebox.showerror("Error", "Please enter either a subject, a from email ID, a from email filter, or a before date.")
            return

        query = ""
        if subject:
            query += f"subject:{subject}"
        if from_email:
            if query:
                query += " "
            query += f"from:{from_email}"
        if from_email_filter:
            if query:
                query += " "
            query += f"from:*{from_email_filter}*"
        if before_date:
            try:
                # Validate date format
                date_obj = datetime.datetime.strptime(before_date, '%Y/%m/%d')
                formatted_date = date_obj.strftime('%Y/%m/%d')
                if query:
                    query += " "
                query += f"before:{formatted_date}"
            except ValueError:
                messagebox.showerror("Error", "Date format should be YYYY/MM/DD.")
                return


        def fetch_and_delete():
            message_ids = self.set_of_messages_matching_query(query)
            if messagebox.askyesno("Confirmation", f"You are about to delete {len(message_ids)} messages. Do you want to continue?"):
                batch_size = 50
                message_ids = list(message_ids)
                for i in range(0, len(message_ids), batch_size):
                    batch_ids = message_ids[i:i + batch_size]
                    try:
                        self.service.users().messages().batchDelete(
                            userId='me',
                            body={'ids': batch_ids}
                        ).execute()
                        self.output_text.insert(tk.END, f"Deleted messages {i+1} to {i+batch_size}\n")
                    except HttpError as error:
                        if error.resp.status == 403:
                            self.output_text.insert(tk.END, f"Rate limit exceeded, retrying after a pause...\n")
                            time.sleep(1)  # Pause for 1 second before retrying
                            self.service.users().messages().batchDelete(
                                userId='me',
                                body={'ids': batch_ids}
                            ).execute()
                        else:
                            self.output_text.insert(tk.END, f"An error occurred: {error}\n")

                messagebox.showinfo("Success", "Deletion completed.")

        threading.Thread(target=fetch_and_delete).start()

    def clear_category(self, category):
        self.output_text.delete(1.0, tk.END)
        if not self.service:
            messagebox.showerror("Error", "Please authenticate first.")
            return

        def fetch_and_delete():
            message_ids = self.set_of_messages_matching_query(f"category:{category}")
            if messagebox.askyesno("Confirmation", f"You are about to delete {len(message_ids)} messages from {category.capitalize()}. Do you want to continue?"):
                batch_size = 50
                message_ids = list(message_ids)
                for i in range(0, len(message_ids), batch_size):
                    batch_ids = message_ids[i:i + batch_size]
                    try:
                        self.service.users().messages().batchDelete(
                            userId='me',
                            body={'ids': batch_ids}
                        ).execute()
                        self.output_text.insert(tk.END, f"Deleted messages {i+1} to {i+batch_size} from {category.capitalize()}\n")
                    except HttpError as error:
                        if error.resp.status == 403:
                            self.output_text.insert(tk.END, f"Rate limit exceeded, retrying after a pause...\n")
                            time.sleep(1)  # Pause for 1 second before retrying
                            self.service.users().messages().batchDelete(
                                userId='me',
                                body={'ids': batch_ids}
                            ).execute()
                        else:
                            self.output_text.insert(tk.END, f"An error occurred: {error}\n")

                messagebox.showinfo("Success", f"Deletion from {category.capitalize()} completed.")

        threading.Thread(target=fetch_and_delete).start()

    def batch_callback(self, request_id, response, exception):
        if exception:
            self.output_text.insert(tk.END, f"An error occurred: {exception}\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = GmailCleanerApp(root)
    root.mainloop()
