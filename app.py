from flask import Flask, render_template, request
import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# MySQL Configuration using environment variables
db_config = {
    'host': os.getenv('MYSQL_HOST'),
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'database': os.getenv('MYSQL_DATABASE')
}

# Route: Home page (Form to submit data and show all users)


@app.route('/', methods=['GET', 'POST'])
def index():
    # Get data from the form (if POST method)
    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form['email']

            # Connect to MySQL and insert data
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
            conn.commit()
            cursor.close()
            conn.close()

        except Exception as e:
            return f"An error occurred: {e}"

    # Fetch all users from the database to display on the page
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Query to fetch all users
        cursor.execute("SELECT id, name, email FROM users")
        users = cursor.fetchall()  # Get all records

        # Close the connection
        cursor.close()
        conn.close()

        # Pass users data to the template
        return render_template('index.html', users=users)

    except Exception as e:
        return f"An error occurred: {e}"


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
