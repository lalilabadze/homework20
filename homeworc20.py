import requests
from bs4 import BeautifulSoup
import sqlite3

# SQLite database creation and connection
def create_database():
    conn = sqlite3.connect('countries.db')
    c = conn.cursor()
    
    # Create a table if not exists
    c.execute("""
    CREATE TABLE IF NOT EXISTS countries (
        id INTEGER PRIMARY KEY,
        country TEXT NOT NULL,
        capital TEXT NOT NULL
    )
    """)
    conn.commit()
    return conn, c


def parse_web_page():
    url = "https://geographyfieldwork.com/WorldCapitalCities.htm"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract country and capital pairs from the webpage , გარკვეული პერიოდის შემდეგ შესაზლოა ჩასასწორებელი იყოს. გვახსოვდეს
    country_capitals = []
    table = soup.find('table', {'class': 'sortable'})  # Locate the table
    
    if table:
        rows = table.find_all('tr')[1:]  # Skip the header row
        for row in rows:
            cols = row.find_all('td')
            if len(cols) > 1:
                country = cols[0].get_text(strip=True)
                capital = cols[1].get_text(strip=True)
                country_capitals.append((country, capital))
    
    return country_capitals

# Insert country-capital data into the SQLite database, მონაცემები
def insert_data_to_db(c, country_capitals):
    for country, capital in country_capitals:
        c.execute("""
        INSERT INTO countries (country, capital) 
        VALUES (?, ?)
        """, (country, capital))
    c.connection.commit()

def main():
    # Create database and table, 
    conn, c = create_database()
    
    # Parse the web page and get country-capital pairs
    country_capitals = parse_web_page()

    # Insert data into the database
    insert_data_to_db(c, country_capitals)
    
    # Verify that data was inserted
    c.execute("SELECT * FROM countries LIMIT 5")  # Show first 5 entries as an example
    rows = c.fetchall()
    for row in rows:
        print(row)
    
    # Close the database connection
    conn.close()

if __name__ == "__main__":
    main()
