# gmail_cleaner
Gmail Cleaner is a Python app with a Tkinter GUI for managing Gmail. Users can authenticate, load tokens, and delete emails based on subject, sender, date, or category. The app supports batch deletion and provides status updates, offering a user-friendly way to clean up your inbox.

![image](https://github.com/user-attachments/assets/17419a4a-4a23-4734-89fe-2f5ab531e6c4)

## Features

- Authenticate using Gmail API
- Load existing token directly
- Delete emails based on:
  - Subject
  - Sender email ID
  - Sender email filter
  - Date before which emails should be deleted
- Clear emails from Promotions and Social categories
- Batch deletion to handle large numbers of emails
- Display status updates during the deletion process

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/gmail-cleaner.git
   cd gmail-cleaner
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python gmail_cleaner.py
   ```


## Usage

1. **Launch the application:**
   ```bash
   python gmail_cleaner.py
   ```

2. **Authenticate with your Gmail account:**
   - Click on the "Authenticate Credentials" button.
   - A file dialog will open. Select your credentials JSON file (usually named `credentials.json`).
   - Follow the prompts to authenticate with your Google account.
   - Once authenticated, the app will save a `token.json` file for future use.

3. **Optionally, load an existing token directly:**
   - If you have previously authenticated and have a `token.json` file, you can use it directly.
   - Click on the "Or Load Token Directly" button.
   - A file dialog will open. Select your `token.json` file.

4. **Enter the desired criteria for deleting emails:**
   - **Search Subject (optional):** Enter a subject to search for specific emails.
   - **From Email ID:** Enter the full email address of the sender whose emails you want to delete.
   - **From Email Filter:** Enter a partial email address or domain to filter emails from certain senders.
   - **Delete Emails Before Date (YYYY/MM/DD):** Enter a date to delete emails before this date. Ensure the format is YYYY/MM/DD.

5. **Delete emails based on the criteria provided:**
   - Click on the "Delete Emails" button.
   - The application will search for emails matching the criteria and prompt you for confirmation before deletion.
   - Once confirmed, it will start deleting the emails in batches, displaying the progress in the text area.

6. **Alternatively, clear emails from specific categories:**
   - **Clear Promotions:**
     - Click on the "Clear Promotions" button.
     - The application will search for emails in the Promotions category and prompt you for confirmation before deletion.
   - **Clear Social:**
     - Click on the "Clear Social" button.
     - The application will search for emails in the Social category and prompt you for confirmation before deletion.

7. **Monitor the deletion process:**
   - The text area at the bottom of the application will display status updates during the deletion process.
   - If the rate limit is exceeded, the application will automatically pause and retry.
```

## Requirements

- Python 3.x
- Tkinter
- Google API Client Library for Python
- Google Auth Library for Python
- OAuthlib

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
```
