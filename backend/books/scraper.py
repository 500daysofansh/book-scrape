from selenium import webdriver
from selenium.webdriver.common.by import By
from .models import Book
from .ai_insights import generate_book_insights
from .rag_pipeline import add_to_rag_storage

def run_deep_scraper():
    """
    Requirement: Document Processing Engine.
    Bonus: Multi-page scraping pipeline + Optimization Techniques.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--headless") 
    options.add_argument("--disable-gpu")
    
    # 🔥 OPTIMIZATION 1: Tell Chrome to NOT load images, CSS, or fonts.
    prefs = {
        "profile.managed_default_content_settings.images": 2,
        "profile.managed_default_content_settings.stylesheets": 2,
        "profile.managed_default_content_settings.fonts": 2
    }
    options.add_experimental_option("prefs", prefs)
    
    # 🔥 OPTIMIZATION 2: 'eager' means don't wait for the page to fully render, 
    # just grab the HTML and go.
    options.page_load_strategy = 'eager' 
    
    driver = webdriver.Chrome(options=options)
    
    try:
        # Loop through the first 2 pages
        for page_num in range(1, 3): 
            print(f"📄 Scraping Page {page_num}...")
            driver.get(f"https://books.toscrape.com/catalogue/page-{page_num}.html")
            
            links = driver.find_elements(By.CSS_SELECTOR, "h3 a")
            book_urls = [link.get_attribute("href") for link in links]

            # Processing 5 books per page for the demo
            for url in book_urls[:5]: 
                driver.get(url)
                # 🔥 OPTIMIZATION 3: Removed time.sleep(1). We don't need it anymore.

                title = driver.find_element(By.TAG_NAME, "h1").text
                
                # Check cache first
                if Book.objects.filter(title=title).exists():
                    print(f"⏭️ Skipping already processed: {title}")
                    continue

                try:
                    desc = driver.find_element(By.XPATH, "//div[@id='product_description']/following-sibling::p").text
                except:
                    desc = "No description available."
                    
                rating_class = driver.find_element(By.CSS_SELECTOR, ".star-rating").get_attribute("class")
                rating = rating_class.replace("star-rating ", "")

                # ⚠️ NOTE: The AI API call is now your only bottleneck. 
                # It takes 1-3 seconds per book to generate the summary/genre.
                insights = generate_book_insights(desc)

                book = Book.objects.create(
                    title=title,
                    author="Classic Literature",
                    description=desc,
                    rating=rating,
                    genre=insights.get('genre', 'General'),
                    summary=insights.get('summary', 'No summary available.'),
                    sentiment=insights.get('sentiment', 'Neutral'),
                    url=url
                )

                add_to_rag_storage(book)
                print(f"⚡ Turbo Processed: {title}")

    finally:
        driver.quit()