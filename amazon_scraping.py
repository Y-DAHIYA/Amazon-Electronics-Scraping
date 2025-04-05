import re
import time
import pandas as pd
from bs4 import BeautifulSoup as bs
from selenium import webdriver

API_KEY = "4316fc6257316b8086e8295fe87d3ecf"
base_url = "https://www.amazon.in"
search_url = "https://www.amazon.in/s?k=electronics&i=electronics"

# Initialize Selenium driver
driver = webdriver.Chrome()

# Store all results
results = []
num_pages = 100

for page in range(1, num_pages + 1):
    print(f"Scraping page {page}...")

    # Build paginated URL
    if page == 1:
        url = f"https://api.scraperapi.com/?api_key={API_KEY}&url={search_url}"
    else:
        paginated_url = f"{search_url}&page={page}"
        url = f"https://api.scraperapi.com/?api_key={API_KEY}&url={paginated_url}"

    # Load page
    driver.get(url)
    time.sleep(5)
    soup = bs(driver.page_source, 'html.parser')

    main_container = soup.find("div", class_="s-main-slot s-result-list s-search-results sg-row")
    if not main_container:
        continue

    all_products = main_container.find_all("div", {"data-asin": True, "data-component-type": "s-search-result"})

    for product in all_products:
        try:
            asin = product.get("data-asin")
            if not asin.strip():
                continue

            a_tag = product.find("a", class_="a-link-normal s-line-clamp-4 s-link-style a-text-normal")
            name = a_tag.get_text(strip=True) if a_tag else None
            url = base_url + a_tag["href"] if a_tag and "href" in a_tag.attrs else None

            price_tag = product.find("span", class_="a-price")
            price = price_tag.find("span", class_="a-offscreen").get_text(strip=True) if price_tag else None

            original_price_tag = product.find("span", class_="a-price a-text-price")
            original_price = original_price_tag.find("span", class_="a-offscreen").get_text(strip=True) if original_price_tag else None

            offer_tag = product.find("span", string=lambda text: text and "%" in text)
            offer = offer_tag.get_text(strip=True) if offer_tag else None

            rating_tag = product.find("span", class_="a-icon-alt")
            rating = rating_tag.get_text(strip=True) if rating_tag else None

            review_tag = product.find("span", class_="a-size-base s-underline-text")
            reviews = review_tag.get_text(strip=True) if review_tag else None

            sold_tag = product.find("span", class_="a-size-base a-color-secondary")
            sold_last_month = sold_tag.get_text(strip=True) if sold_tag else None

            results.append({
                "Name": name,
                "Price": price,
                "Original Price": original_price,
                "Offer": offer,
                "Rating": rating,
                "Reviews": reviews,
                "Sold Last Month": sold_last_month,
                "url": url
            })

        except Exception as e:
            print("Error on a product:", e)

driver.quit()

# Convert to DataFrame
df = pd.DataFrame(results)

# ---------- Cleaning Functions ----------
def clean_price(price):
    if price:
        clean = price.replace("₹", "").replace(",", "").strip()
        try:
            return int(float(clean))
        except ValueError:
            return "NA"
    return "NA"

def clean_discount(discount):
    return int(re.search(r'(\d+)', discount).group(1)) if discount else "NA"

def clean_rating(rating):
    try:
        return float(rating.split()[0]) if rating else "NA"
    except:
        return "NA"

def clean_reviews(reviews):
    try:
        return int(reviews.replace(",", "")) if reviews else "NA"
    except:
        return "NA"

def clean_sold(sold):
    if sold:
        match = re.search(r'(\d+)', sold)
        return int(match.group(1)) if match else "NA"
    return "NA"

def clean_name(name):
    if isinstance(name, str):
        return re.sub(r'[^\w\s]', '', name).strip()
    return "NA"

def short_name(name, word_limit=6):
    if isinstance(name, str):
        clean = re.sub(r'[^\w\s]', '', name)
        words = clean.split()
        return ' '.join(words[:word_limit])
    return "NA"

def extract_keywords(name):
    if isinstance(name, str):
        keywords = ['earbuds', 'camera', 'organizer', 'case', 'warranty', 'charger', 'security', 'spy', 'stand', 'cable']
        clean = re.sub(r'[^\w\s]', '', name.lower())
        words = clean.split()
        brand = words[0].capitalize() if words else "Unknown"
        product_keywords = [word for word in words if word in keywords]
        return f"{brand} {' '.join(product_keywords).capitalize()}" if product_keywords else brand
    return "NA"

# ---------- Apply Cleaning Using Map Loop ----------
cleaning_map = {
    "Clean Name": ("Name", clean_name),
    "Short Name": ("Name", short_name),
    "Summary Name": ("Name", extract_keywords),
    "Price (₹)": ("Price", clean_price),
    "Original Price (₹)": ("Original Price", clean_price),
    "Discount (%)": ("Offer", clean_discount),
    "Rating": ("Rating", clean_rating),
    "Reviews": ("Reviews", clean_reviews),
    "Sold Last Month": ("Sold Last Month", clean_sold),
}

# Apply each cleaning function
for new_col, (original_col, func) in cleaning_map.items():
    df[new_col] = df[original_col].apply(func)

# Rearrange columns
df = df[[
    "Name", "Clean Name", "Short Name", "Summary Name", 
    "Price (₹)", "Original Price (₹)", "Discount (%)", 
    "Rating", "Reviews", "Sold Last Month", "url"
]]

# Save to CSV
df.to_csv("amazon_electronics_datas.csv", index=False)
print("✅ Saved as 'amazon_electronics_multi_page.csv'")
