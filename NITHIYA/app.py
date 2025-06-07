# app.py (Flask backend using direct MySQL connector, no SQLAlchemy)
from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "supersecretkey"

# MySQL Configuration
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Digidara1000",
    database="paperdb"
)
cursor = mydb.cursor(dictionary=True)

@app.route('/')
def home():
    return render_template('home_page.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit_paper():
    if request.method == 'POST':
        try:
            sql = """
                INSERT INTO submission
                (student_name, student_id, email, college, stream, course, title, abstract, doc_link, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                request.form['student_name'],
                request.form['student_id'],
                request.form['email'],
                request.form['college'],
                request.form['stream'],
                request.form['course'],
                request.form['title'],
                request.form['abstract'],
                request.form.get('doc_link', ''),
                'Pending'
            )
            cursor.execute(sql, values)
            mydb.commit()
            return redirect(url_for('submission_success'))
        except mysql.connector.Error as err:
            flash("❌ Error submitting paper: " + str(err), "danger")
            return redirect(url_for('submit_paper'))
    return render_template('submit_paper.html')

@app.route('/submission-success')
def submission_success():
    return render_template('submission_success.html')

@app.route('/view', methods=['GET', 'POST'])
def view_submission():
    submissions = None
    if request.method == 'POST':
        email = request.form['email']
        cursor.execute("SELECT * FROM submission WHERE email = %s", (email,))
        submissions = cursor.fetchall()
    return render_template('view_submission.html', submissions=submissions)

import mysql.connector
from flask import request, session, redirect, url_for, render_template, flash

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Connect to MySQL database
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Digidara1000',
            database='paperdb'
        )
        cursor = conn.cursor()
        query = "SELECT * FROM admins WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        admin = cursor.fetchone()
        conn.close()

        if admin:
            session['admin'] = True
            return redirect(url_for('admin_view'))
        else:
            flash("Invalid login", "danger")

    return render_template('admin.html')


@app.route('/admin-view')
def admin_view():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))

    name_filter = request.args.get('name')
    status_filter = request.args.get('status')

    query = "SELECT * FROM submission WHERE 1=1"
    params = []

    if name_filter:
        query += " AND student_name LIKE %s"
        params.append(f"%{name_filter}%")
    if status_filter:
        query += " AND status = %s"
        params.append(status_filter)

    cursor.execute(query, tuple(params))
    results = cursor.fetchall()
    return render_template('admin_dashboard.html', submissions=results)

@app.route('/update-status/<int:id>/<status>')
def update_status(id, status):
    if not session.get('admin'):
        return redirect(url_for('admin_login'))

    cursor.execute("UPDATE submission SET status = %s WHERE id = %s", (status, id))
    mydb.commit()
    return redirect(url_for('admin_view'))
@app.route('/about')
def about_us():
    return render_template('about_us.html')

@app.route('/instructions')
def instructions():
    return render_template('instructions.html')

@app.route('/admin-page')
def admin_page():
    return render_template('admin_page.html')


@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)