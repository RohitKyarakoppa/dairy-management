import sqlite3

# Connect Database
conn = sqlite3.connect('dairy.db')

# Create Cursor
cursor = conn.cursor()

# Create Farmers Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS farmers(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    farmer_id TEXT,
    name TEXT,
    mobile TEXT,
    village TEXT
)
''')

# Create Milk Entries Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS milk_entries(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    farmer_id TEXT,
    shift TEXT,
    liters REAL,
    fat REAL,
    snf REAL,
    rate REAL,
    amount REAL,
    date TEXT
)
''')

# Save Changes
conn.commit()

# Close Database
conn.close()

print("Database Created Successfully")