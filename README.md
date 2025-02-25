# Dune Dashboard Chart Refresher Bot

This project automates refreshing charts on a [Dune.com](https://dune.com/) dashboard using SeleniumBase with Undetected Chrome. The bot navigates to the Dune login page, waits for user authentication, and then continuously monitors and refreshes dashboard elements.

## Features

- **Automated Login & Navigation:** Opens the Dune login page and waits for you to log in.
- **Dynamic Element Interaction:** Searches for dashboard elements with specific text patterns and clicks associated buttons to trigger a refresh.
- **Cookie Handling:** Detects and accepts cookie notifications automatically.
- **Robust Logging & Error Handling:** Uses Python’s logging module to output detailed runtime information and handles errors gracefully.

## Prerequisites

- Python 3.7 or later
- Google Chrome installed on your system

## Installation

1. Clone the repository or download the source code.

2. Create and activate a virtual environment (recommended):

   python -m venv venv  
   source venv/bin/activate  # On Windows use: venv\Scripts\activate

3. Install the required packages:

   python -m pip install -r requirements.txt

## Usage

1. Run the Script:

   python app.py

2. Login Phase:

   - The bot will launch the Dune login page.
   - Manually log in to your Dune account.
   - Once logged in, return to your terminal and press Enter to continue.

3. Dashboard Refresh:

   - After login, the script navigates to the dashboard URL.
   - The bot continuously searches for elements with specific characteristics, clicks associated buttons, and triggers a refresh.
   - The bot also handles any cookie notifications by automatically accepting them.

4. Stopping the Bot:

   - Press Ctrl+C in the terminal to gracefully stop the bot.

## Customization

- **Headless Mode:** To run the bot without a visible browser window, change the headless parameter to True in the init() function call.
- **Timing & Wait Intervals:** Adjust the sleep durations and WebDriverWait times in the code as needed based on your network speed and dashboard load times.
- **Logging:** The logging level is set to INFO by default. You can modify it in the logging.basicConfig setup.

## Troubleshooting

- **Element Not Found:** Ensure that the class names and XPath expressions in the script match the current structure of the Dune dashboard.
- **Driver Issues:** Verify that Google Chrome is up-to-date. SeleniumBase and Undetected Chrome should automatically handle the correct version of ChromeDriver.
- **Login Problems:** Make sure to complete the login process in the opened browser before pressing Enter in the terminal.

## License

This project is licensed under the MIT License.

---

Happy automating!"# dune-analytics-refresh-bot" 
