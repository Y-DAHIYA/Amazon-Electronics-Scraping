# Amazon Electronics Dashboard - Power BI Project

## 📝 Project Overview
This project involves web scraping electronic product data from Amazon using Python libraries like Selenium and BeautifulSoup. The data is cleaned, stored in a SQL database, and finally visualized using Power BI. The dashboard provides insights into customer ratings, sales, discount patterns, and product quality.

---

## 🔍 Project Stages

### 1. **Web Scraping (Amazon Electronics)**
- **Tools Used:** `Selenium`, `BeautifulSoup`, `Pandas`, `Proxy API`
- **Steps:**
  - Automated browser navigation using Selenium.
  - Extracted product details: Name, Price, Original Price, Rating, Reviews, Sales info, and URL.
  - Implemented rotating proxy APIs to bypass IP blocking.
  - Cleaned data on-the-fly (removing special characters, missing values handled).
  - Stored data in a structured `DataFrame`.

### 2. **SQL Integration**
- **Database:** MySQL
- **Steps:**
  - Created table schema in MySQL.
  - Inserted cleaned data into SQL.
  - Sample Queries Used:
    ```sql
    SELECT * FROM electronics WHERE rating < 2;
    SELECT COUNT(*) FROM electronics WHERE discount > 50;
    SELECT name, price FROM electronics ORDER BY sold_last_month DESC LIMIT 10;
    ```

### 3. **Power BI Dashboard**
- **Data Source:** MySQL database
- **Data Cleaning:**
  - Converted text to numeric fields
  - Created calculated columns like `Revenue = Price * Sold Last Month`
  - Derived columns like `Rating Bucket`, `Discount Range`, `Price Range`

### 4. **Visualizations & Insights**

#### 📊 Charts
1. **Gauge Chart:** Average Customer Rating (Target = 4.5, Min = 0, Max = 5)
2. **Line Chart:** Monthly Units Sold by Customer Rating
3. **Clustered Column Chart:** Top 10 Best-Selling Electronics
4. **Donut Chart:** Product Share by Discount Range
5. **Stacked Bar Chart:** Scrap Items by Rating Bucket

#### 🧩 Slicers
- Rating Bucket
- Discount Range
- Price Range
- Reset Button for Filters

#### 🔢 Cards
- Total Scraped Items
- Total Revenue
- Average Rating
- Total Products Sold

---

## 📁 Folder Structure
```
├── dashboard.png
├── scraper.py
├── cleaned_data.csv
├── electronics.sql
├── powerbi_dashboard.pbix
├── README.md
```

---

## 💡 Key Learnings
- Handling dynamic content with Selenium
- Using Proxy APIs for large-scale scraping
- Cleaning and transforming data during and post scraping
- Writing optimized SQL queries for reporting
- Building impactful visuals using Power BI

---

## 📌 Tools & Technologies
- **Languages:** Python, SQL, DAX
- **Libraries:** Selenium, BeautifulSoup, Pandas, Requests
- **Database:** MySQL
- **Visualization:** Power BI

---

## 📷 Dashboard Preview
![Image](https://github.com/user-attachments/assets/0ee74301-7b56-49db-bd0a-db134619f4c1)

---

## 🔗 Connect
For any queries, feedback, or collaborations:
**GitHub:** [Your GitHub Profile Link]  
**Email:** [Your Email Address]

---

> "Turning Raw Data into Real Insights."

---

