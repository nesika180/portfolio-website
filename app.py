from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# DB INIT
def init_db():
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            message TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# HOME
@app.route('/')
def home():
    return render_template('home.html')

# ABOUT
@app.route('/about')
def about():
    return render_template('about.html')

# PROJECTS
@app.route('/projects')
def projects():
    return render_template('projects.html')

# CONTACT


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        conn = sqlite3.connect('messages.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)",
            (name, email, message)
        )
        conn.commit()
        conn.close()

        return redirect(url_for('contact', success='1'))

    success = request.args.get('success')
    return render_template('contact.html', success=success)

@app.route('/messages')
def view_messages():
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM contacts ORDER BY id DESC")
    data = cursor.fetchall()

    conn.close()

    return render_template('messages.html', messages=data)


if __name__ == "__main__":
    app.run(debug=True)

