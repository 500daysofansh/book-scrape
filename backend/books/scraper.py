from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape_books(limit=10):
    # Setup Chrome options (Headless means no window pops up)
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    url = "http://books.toscrape.com/catalogue/category/books_1/index.html"
    driver.get(url)
    time.sleep(2) # Give it a second to breathe
    
    books_list = []
    
    # Find all book containers
    items = driver.find_elements(By.CLASS_NAME, "product_pod")[:limit]
    
    for item in items:
        try:
            # Extract basic info
            title = item.find_element(By.TAG_NAME, "h3").find_element(By.TAG_NAME, "a").get_attribute("title")
            rating = item.find_element(By.CSS_SELECTOR, ".star-rating").get_attribute("class").split()[-1]
            price = item.find_element(By.CLASS_NAME, "price_color").text
            book_url = item.find_element(By.TAG_NAME, "h3").find_element(By.TAG_NAME, "a").get_attribute("href")
            
            # Note: In a real scenario, you'd click the link to get the full description. 
            # For this test, we'll create a placeholder description.
            books_list.append({
                "title": title,
                "rating": rating,
                "description": f"A great book priced at {price}. This was collected via automation.",
                "url": book_url,
                "author": "Unknown Author" # The demo site doesn't list authors on the front page
            })
        except Exception as e:
            print(f"Skipping a book due to error: {e}")
            
    driver.quit()
    return books_list