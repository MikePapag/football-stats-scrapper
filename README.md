Football Stats Scraper ⚽

A powerful Selenium-based web scraper that extracts comprehensive football statistics from FootyStats.org for data analysis and match predictions.

🚀 Features
Automated Data Collection: Scrapes home and away team statistics including form, goals, xG, possession, and shots

Multi-Season Support: Collects both current and previous season data

User-Friendly Interface: Simple command-line input for team names

Anti-Detection Measures: Randomized user agents and human-like delays

CSV Export: Clean data output in CSV format for easy analysis

Automatic ChromeDriver Management: No manual driver updates required

📊 Data Collected
Home/Away Form Statistics
Matches Played, Wins, Draws, Losses

Goals For and Goals Against

Home and Away performance metrics

Advanced Metrics
Expected Goals (xG) For/Against per Match

Goals Scored/Conceded per Match

Match Goals Average

Possession Average

Shots Taken per Match

🛠️ Installation
Prerequisites
Python 3.7+

Google Chrome browser

Stable internet connection

Setup
Clone the repository:

bash
git clone https://github.com/yourusername/football-stats-scraper.git
cd football-stats-scraper
Install required packages:

bash
pip install -r requirements.txt
Run the scraper:

bash
python src/football_scraper.py
📋 Requirements
Create a requirements.txt file with:

txt
selenium==4.15.0
webdriver-manager==4.0.1
🎯 Usage
Run the script:

bash
python src/football_scraper.py
Enter the home and away team names when prompted:

text
=== Football Stats Scraper ===
Enter the teams to scrape data for:
Enter home team: Manchester United
Enter away team: Liverpool
Confirm to start scraping:

text
Scraping data for Manchester United (home) vs Liverpool (away)...
Start scraping? (y/n): y
Check the generated match_stats.csv file for your data.

🔧 Technical Details
Selenium Implementation
Headless Chrome: Runs in background without GUI

Explicit Waits: Ensures reliable element loading

XPath Selectors: Robust element targeting

Error Handling: Graceful failure recovery

Anti-Bot Measures
Randomized user agents

Human-like delays between actions

Chrome automation flags disabled

Realistic browsing patterns

Data Output
The scraper generates a CSV file with the following columns:

Team: Team name

Season: Current or Previous season

Stat Type: Specific statistic name

Value: Statistic value

🧪 Example Output
csv
Team,Season,Stat Type,Value
Manchester United,Current,Home Form_Played,8
Manchester United,Current,Home Form_Wins,6
Manchester United,Current,Home Form_Draws,1
Manchester United,Current,Home Form_Losses,1
Manchester United,Current,Home_Scored / Match,2.25
...
⚠️ Important Notes
Respect website terms of service

Use appropriate delays to avoid overloading servers

Data is for educational and analytical purposes

Website structure changes may require code updates

🐛 Troubleshooting
Common Issues
ChromeDriver errors:

Ensure Chrome is updated to latest version

The script automatically manages ChromeDriver via webdriver-manager

Element not found:

Website structure may have changed

Check console for specific error messages

Scraping blocked:

Increase delay times in human_delay() function

Try different user agents

⚖️ Disclaimer
This tool is designed for educational purposes to demonstrate web scraping with Selenium. Users are responsible for complying with website terms of service and applicable laws.

Built with Python + Selenium • Perfect for data science and football analytics projects
