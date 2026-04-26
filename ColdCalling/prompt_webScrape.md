You are an autonomous coding agent tasked with building a Python tool that collects restaurant and food-related business data for a SINGLE selected area at a time and exports it to an Excel file.

### GOAL
Build a script that:
1. Accepts a user input for ONE area (e.g., "Guelph", "Cambridge", "Waterloo", "Kitchener", "Burlington", "Hamilton", "Orangeville").
2. Searches for SMALL / INDEPENDENT food businesses only:
   - Restaurants (non-franchise)
   - Sweet shops / मिठाई stores
   - Sweets manufacturers
   - Cloud kitchens
   - Takeout-only kitchens
3. Collects structured data and exports to an Excel file.

---

### DATA FIELDS (COLUMNS IN EXCEL)
- Business Name
- Address
- City
- Phone Number (business only, no personal numbers)
- Website (if available)
- Category / Cuisine (Indian, Chinese, Italian, etc.)
- Source (Google, Yelp, YellowPages, etc.)

DO NOT collect or infer personal/private data like owner names unless explicitly public and business-listed.

---

### DATA SOURCES (PRIORITY ORDER)
Use compliant and scalable methods:

1. Google Places API (preferred over scraping Google Maps)
2. Yelp Fusion API
3. Public business directories (HTML scraping allowed only if robots.txt permits)
4. Official business websites

Avoid scraping pages that block bots or violate terms.

---

### FILTERING LOGIC
- Exclude large chains and franchises (e.g., McDonald's, Tim Hortons)
- Keep only independent/local businesses
- Heuristics:
  - Remove businesses with multiple locations or franchise indicators
  - Prefer unique names and single-location businesses

---

### TECH STACK
- Python 3
- Libraries:
  - requests / httpx
  - pandas
  - openpyxl or xlsxwriter
  - beautifulsoup4 (only where scraping is allowed)
- Optional: use dotenv for API keys

---

### FUNCTIONAL REQUIREMENTS

1. Input Module:
   - Prompt user: "Enter city name:"
   - Validate input (must be one city only)

2. Data Collection:
   - Query APIs with keywords:
     "restaurant", "sweet shop", "mithai", "bakery", "cloud kitchen"
   - Handle pagination
   - Normalize data across sources

3. Deduplication:
   - Remove duplicates based on name + address

4. Data Cleaning:
   - Standardize phone numbers
   - Normalize cuisine/category
   - Clean addresses

5. Export:
   - Save as: `<city>_restaurants.xlsx`
   - Use pandas DataFrame

---

### OUTPUT FORMAT
Excel file with clean columns and no duplicates.

---

### ERROR HANDLING
- Handle API rate limits
- Retry failed requests
- Skip incomplete records gracefully

---

### BONUS FEATURES (IF POSSIBLE)
- Add a column: "Confidence Score (Independent Business)"
- Add logging
- CLI arguments instead of input prompt

---

### DELIVERABLE
A complete Python script that:
- Runs from command line
- Takes a city as input
- Outputs a structured Excel file

Write clean, modular, production-ready code.