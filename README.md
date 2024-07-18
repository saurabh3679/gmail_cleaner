# gmail_cleaner
Gmail Cleaner is a Python app with a Tkinter GUI for managing Gmail. Users can authenticate, load tokens, and delete emails based on subject, sender, date, or category. The app supports batch deletion and provides status updates, offering a user-friendly way to clean up your inbox.


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

1. Launch the application:
   ```bash
   python gmail_cleaner.py
   ```

2. Authenticate with your Gmail account by selecting the credentials JSON file.

3. Optionally, load an existing token JSON file directly.

4. Enter the desired criteria for deleting emails (subject, sender email ID, sender email filter, date before which emails should be deleted).

5. Click on "Delete Emails" to delete emails based on the criteria provided.

6. Alternatively, click on "Clear Promotions" or "Clear Social" to delete emails from the Promotions or Social categories, respectively.

## Requirements

- Python 3.x
- Tkinter
- Google API Client Library for Python
- Google Auth Library for Python
- OAuthlib

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
```
