from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape_books(limit=10):
    """
    Uses Selenium to scrape real book data. 
    Clicks into individual book pages to retrieve full descriptions.
    """
    # Setup headless Chrome options for performance
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    # Target URL (Sandbox bookstore)
    url = "http://books.toscrape.com/catalogue/category/books_1/index.html"
    driver.get(url)
    time.sleep(2)
    
    books_data = []
    
    # Find initial book links on the home page
    book_elements = driver.find_elements(By.CSS_SELECTOR, "h3 a")
    book_links = [el.get_attribute("href") for el in book_elements][:limit]
    
    for link in book_links:
        try:
            # Navigate to the specific book detail page
            driver.get(link)
            time.sleep(1) # Polite scraping
            
            title = driver.find_element(By.TAG_NAME, "h1").text
            
            # Extract Rating from class name (e.g., 'star-rating Three')
            rating_element = driver.find_element(By.CSS_SELECTOR, ".star-rating")
            rating = rating_element.get_attribute("class").replace("star-rating ", "")
            
            # Extract Real Description (found in the sibling of the product_description header)
            try:
                description = driver.find_element(By.XPATH, "//div[@id='product_description']/following-sibling::p").text
            except:
                description = "No description available."
                
            books_data.append({
                "title": title,
                "rating": rating,
                "description": description,
                "url": link,
                "author": "Classic Literature" # Site doesn't list authors; providing a default
            })
            print(f"✅ Scraped: {title}")
            
        except Exception as e:
            print(f"❌ Error scraping {link}: {e}")
            
    driver.quit()
    return books_data