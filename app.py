from flask import Flask, render_template, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

# ---------------- HOME PAGE ----------------
@app.route('/')
def home():
    return render_template('index.html')


# ---------------- ADD FARMER ----------------
# ---------------- ADD FARMER ----------------
@app.route('/add_farmer', methods=['GET', 'POST'])
def add_farmer():

    message = ""

    if request.method == 'POST':

        farmer_id = request.form['farmer_id']
        name = request.form['name']
        mobile = request.form['mobile']
        village = request.form['village']

        conn = sqlite3.connect('dairy.db')
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO farmers(farmer_id, name, mobile, village) VALUES(?,?,?,?)",
            (farmer_id, name, mobile, village)
        )

        conn.commit()
        conn.close()

        message = "Farmer Added Successfully"

    return render_template('add_farmer.html', message=message)


# ---------------- SEARCH FARMER ----------------
@app.route('/search_farmer', methods=['GET', 'POST'])
def search_farmer():

    farmer = None

    if request.method == 'POST':

        farmer_id = request.form['farmer_id']

        conn = sqlite3.connect('dairy.db')
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM farmers WHERE farmer_id=?",
            (farmer_id,)
        )

        farmer = cursor.fetchone()

        conn.close()

    return render_template('search_farmer.html', farmer=farmer)
# ---------------- DELETE FARMER ----------------
@app.route('/delete_farmer', methods=['GET', 'POST'])
def delete_farmer():

    message = ""

    if request.method == 'POST':

        farmer_id = request.form['farmer_id']

        conn = sqlite3.connect('dairy.db')
        cursor = conn.cursor()

        # Delete farmer
        cursor.execute(
            "DELETE FROM farmers WHERE farmer_id=?",
            (farmer_id,)
        )

        # Delete related milk entries
        cursor.execute(
            "DELETE FROM milk_entries WHERE farmer_id=?",
            (farmer_id,)
        )

        conn.commit()
        conn.close()

        message = "Farmer Deleted Successfully"

    return render_template('delete_farmer.html', message=message)


# ---------------- MILK ENTRY ----------------
# ---------------- MILK ENTRY ----------------
@app.route('/milk_entry', methods=['GET', 'POST'])
def milk_entry():

    message = ""

    if request.method == 'POST':

        farmer_id = request.form['farmer_id']

        shift = request.form['shift']

        liters = float(request.form['liters'])

        fat = float(request.form['fat'])

        snf = float(request.form['snf'])

        # Rate Calculation
        rate = (fat * 8) + (snf * 4)

        amount = rate * liters

        # Automatic Date
        date = datetime.now().strftime("%Y-%m-%d")

        conn = sqlite3.connect('dairy.db')

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO milk_entries
            (farmer_id, shift, liters, fat,
             snf, rate, amount, date)

            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,

            (
                farmer_id,
                shift,
                liters,
                fat,
                snf,
                rate,
                amount,
                date
            )
        )

        conn.commit()

        conn.close()

        message = f"{shift} Milk Entry Saved Successfully"

    return render_template(
        'milk_entry.html',
        message=message
    )


# ---------------- REPORT PAGE ----------------
@app.route('/report', methods=['GET', 'POST'])
def report():

    data = []

    farmer_name = ""

    if request.method == 'POST':

        farmer_id = request.form['farmer_id']

        conn = sqlite3.connect('dairy.db')

        cursor = conn.cursor()

        cursor.execute(
            '''
            SELECT farmers.name,
                   milk_entries.date,
                   milk_entries.shift,
                   milk_entries.liters,
                   milk_entries.fat,
                   milk_entries.snf,
                   milk_entries.amount

            FROM milk_entries

            JOIN farmers
            ON milk_entries.farmer_id = farmers.farmer_id

            WHERE farmers.farmer_id = ?

            ORDER BY milk_entries.date DESC
            ''',

            (farmer_id,)
        )

        data = cursor.fetchall()

        if data:
            farmer_name = data[0][0]

        conn.close()

    return render_template(
        'report.html',
        data=data,
        farmer_name=farmer_name
    )
# ---------------- RUN APP ----------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)