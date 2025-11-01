from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time, random, csv, os, sys

def human_delay(min_sec=2, max_sec=4):
    time.sleep(random.uniform(min_sec, max_sec))

def setup_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0",      
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15"
    ]
    options.add_argument(f"user-agent={random.choice(user_agents)}")
    
    try:
        # Use webdriver_manager to automatically handle ChromeDriver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        return driver
    except Exception as e:
        print(f"Error setting up ChromeDriver: {e}")
        print("Trying alternative method...")
        
        # Fallback: Try with system ChromeDriver
        try:
            service = Service()
            driver = webdriver.Chrome(service=service, options=options)
            return driver
        except Exception as e2:
            print(f"Alternative method also failed: {e2}")
            raise Exception("Could not initialize ChromeDriver. Please ensure Chrome is installed and up to date.")

def save_to_csv(team, season_type, stats_dict):
    with open('match_stats.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for stat_name, value in stats_dict.items():
            writer.writerow([team, season_type, stat_name, value])

def home_away_stats(driver):
    stats_dict = {}
    home_away = ["Home Form", "Away Form"]
    for form_type in home_away:
        try:
            row = driver.find_element(By.XPATH, f"//div[text()='{form_type}']/parent::div[@class='row club-data-table-row dFlex  ']")
            stats = row.find_elements(By.XPATH, ".//div[@class='m' or @class='green' or @class='red1' or @class='red' or @class='g' or @class='a']")
            
            if len(stats) >= 6:
                stats_dict[f"{form_type}_Played"] = stats[0].text
                stats_dict[f"{form_type}_Wins"] = stats[1].text
                stats_dict[f"{form_type}_Draws"] = stats[2].text
                stats_dict[f"{form_type}_Losses"] = stats[3].text
                stats_dict[f"{form_type}_GoalsFor"] = stats[4].text
                stats_dict[f"{form_type}_GoalsAgainst"] = stats[5].text
            else:
                print(f"Warning: Not enough stats found for {form_type}")
                stats_dict.update({
                    f"{form_type}_Played": "0",
                    f"{form_type}_Wins": "0",
                    f"{form_type}_Draws": "0",
                    f"{form_type}_Losses": "0",
                    f"{form_type}_GoalsFor": "0",
                    f"{form_type}_GoalsAgainst": "0"
                })
        except Exception as e:
            print(f"Error getting {form_type} stats: {e}")
            stats_dict.update({
                f"{form_type}_Played": "0",
                f"{form_type}_Wins": "0",
                f"{form_type}_Draws": "0",
                f"{form_type}_Losses": "0",
                f"{form_type}_GoalsFor": "0",
                f"{form_type}_GoalsAgainst": "0"
            })
    
    return stats_dict

def get_table_stats(driver):
    stats_dict = {}
    stats_to_get = ["xG For / Match", "xG Against / Match", "Scored / Match", "Conceded / Match", "AVG (Match Goals Average)", "Possession AVG", "Shots Taken / Match"]
    
    try:
        header = driver.find_element(By.XPATH, "//tr[@class='row header']")
        home_col = int(header.find_elements(By.XPATH, ".//th[contains(text(), 'At Home')]")[0].get_attribute("cellIndex"))
        away_col = int(header.find_elements(By.XPATH, ".//th[contains(text(), 'At Away')]")[0].get_attribute("cellIndex"))
        
        for stat_name in stats_to_get:
            try:
                row = driver.find_element(By.XPATH, f"//tr[@class='row']/td[text()='{stat_name}']/parent::tr")
                home_value = row.find_elements(By.TAG_NAME, "td")[home_col].text
                away_value = row.find_elements(By.TAG_NAME, "td")[away_col].text
                stats_dict[f"Home_{stat_name}"] = home_value
                stats_dict[f"Away_{stat_name}"] = away_value
            except:
                stats_dict[f"Home_{stat_name}"] = "0"
                stats_dict[f"Away_{stat_name}"] = "0"
    except Exception as e:
        print(f"Error getting table stats: {e}")
        for stat_name in stats_to_get:
            stats_dict[f"Home_{stat_name}"] = "0"
            stats_dict[f"Away_{stat_name}"] = "0"
    
    return stats_dict

def get_team_stats(team, season_type):
    print(f"Scraping data for {team} ({season_type} season)...")
    
    driver = None
    try:
        driver = setup_driver()
        url = "https://footystats.org/"
        
        driver.get(url)
        
        # Wait for and interact with search box
        team_search = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'Search Teams and Leagues')]"))
        )
        human_delay()
        team_search.clear()
        team_search.send_keys(team)
        human_delay()
        
        # Click on the team result
        result_click = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, f"//div[contains(text(), '{team.title()}') or contains(text(), '{team.upper()}')]"))
        )
        result_click.click()
        human_delay()
        
        # Wait for team page to load
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'pa1e bbox w100 cf pb05e')]"))
        )

        # Get current season stats
        current_stats = {**home_away_stats(driver), **get_table_stats(driver)}
        save_to_csv(team, season_type, current_stats)
        print(f"Successfully scraped current season data for {team}")

        # Try to get previous season data if this is the current season
        if season_type == "Current":
            try:
                print(f"Attempting to get previous season data for {team}...")
                season_dropdown = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'br4 dropdown-link club-hero-dropdown-tr')]"))
                )
                season_dropdown.click()
                human_delay()
                
                # Try to find and click previous season
                previous_season = driver.find_element(By.XPATH, "//button[contains(text(), '2024') or contains(text(), '2023') or contains(text(), 'Previous')]")
                previous_season.click()
                human_delay()
                
                # Wait for page to update
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'pa1e bbox w100 cf pb05e')]"))
                )
                
                previous_stats = {**home_away_stats(driver), **get_table_stats(driver)}
                save_to_csv(team, "Previous", previous_stats)
                print(f"Successfully scraped previous season data for {team}")
                
            except Exception as e:
                print(f"Could not get previous season data for {team}: {e}")

    except Exception as e:
        print(f"Error scraping {team}: {e}")
    finally:
        if driver:
            driver.quit()

def scrape_match(home_team, away_team):
    # Initialize CSV file with headers
    with open('match_stats.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Team', 'Season', 'Stat Type', 'Value'])

    print(f"Starting scrape for {home_team} vs {away_team}...")
    
    try:
        get_team_stats(home_team, "Current")
        get_team_stats(away_team, "Current")
        print("Scraping completed successfully! Data saved to match_stats.csv")
    except Exception as e:
        print(f"Scraping failed: {e}")

# Install required package first: pip install webdriver-manager
if __name__ == "__main__":
    print("=== Football Stats Scraper ===")
    print("Enter the teams to scrape data for:")
    
    # Get user input for teams
    home_team = input("Enter home team: ").strip()
    while not home_team:
        print("Home team cannot be empty!")
        home_team = input("Enter home team: ").strip()
    
    away_team = input("Enter away team: ").strip()
    while not away_team:
        print("Away team cannot be empty!")
        away_team = input("Enter away team: ").strip()
    
    print(f"\nScraping data for {home_team} (home) vs {away_team} (away)...")
    
    # Optional: Add a confirmation
    confirm = input("Start scraping? (y/n): ").strip().lower()
    if confirm in ['y', 'yes', '']:
        scrape_match(home_team, away_team)
    else:
        print("Scraping cancelled.")