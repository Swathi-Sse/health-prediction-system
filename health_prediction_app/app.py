from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime
from ai_prediction import predict_health

app = Flask(__name__)
DB_NAME = "patients.db"


def get_db_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname TEXT NOT NULL,
        dob TEXT NOT NULL,
        email TEXT NOT NULL,
        glucose REAL NOT NULL,
        haemoglobin REAL NOT NULL,
        cholesterol REAL NOT NULL,
        remarks TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()


def validate_patient(fullname, dob, email, glucose, haemoglobin, cholesterol):
    if not fullname or len(fullname.strip()) < 3:
        return "Name must contain at least 3 characters."

    if "@" not in email or "." not in email:
        return "Please enter a valid email address."

    try:
        dob_date = datetime.strptime(dob, "%Y-%m-%d")
        if dob_date > datetime.now():
            return "Date of birth cannot be in the future."
    except ValueError:
        return "Please enter a valid date of birth."

    try:
        glucose = float(glucose)
        haemoglobin = float(haemoglobin)
        cholesterol = float(cholesterol)
    except ValueError:
        return "Blood test values must be numeric."

    if glucose < 50 or glucose > 500:
        return "Glucose value must be between 50 and 500."

    if haemoglobin < 5 or haemoglobin > 25:
        return "Haemoglobin value must be between 5 and 25."

    if cholesterol < 50 or cholesterol > 500:
        return "Cholesterol value must be between 50 and 500."

    return None


@app.route("/")
def dashboard():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM patients ORDER BY id DESC")
    patients = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM patients")
    total_patients = cursor.fetchone()[0]

    conn.close()

    return render_template(
        "dashboard.html",
        patients=patients,
        total_patients=total_patients
    )


@app.route("/add", methods=["POST"])
def add_patient():
    fullname = request.form.get("fullname")
    dob = request.form.get("dob")
    email = request.form.get("email")
    glucose = request.form.get("glucose")
    haemoglobin = request.form.get("haemoglobin")
    cholesterol = request.form.get("cholesterol")

    error = validate_patient(fullname, dob, email, glucose, haemoglobin, cholesterol)
    if error:
        return render_template("message.html", title="Validation Error", message=error, back_url="/")

    remarks = predict_health(glucose, haemoglobin, cholesterol)

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO patients
    (fullname, dob, email, glucose, haemoglobin, cholesterol, remarks)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        fullname.strip(),
        dob,
        email.strip(),
        float(glucose),
        float(haemoglobin),
        float(cholesterol),
        remarks
    ))

    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_patient(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        fullname = request.form.get("fullname")
        dob = request.form.get("dob")
        email = request.form.get("email")
        glucose = request.form.get("glucose")
        haemoglobin = request.form.get("haemoglobin")
        cholesterol = request.form.get("cholesterol")

        error = validate_patient(fullname, dob, email, glucose, haemoglobin, cholesterol)
        if error:
            conn.close()
            return render_template("message.html", title="Validation Error", message=error, back_url=f"/edit/{id}")

        remarks = predict_health(glucose, haemoglobin, cholesterol)

        cursor.execute("""
        UPDATE patients
        SET fullname = ?,
            dob = ?,
            email = ?,
            glucose = ?,
            haemoglobin = ?,
            cholesterol = ?,
            remarks = ?
        WHERE id = ?
        """, (
            fullname.strip(),
            dob,
            email.strip(),
            float(glucose),
            float(haemoglobin),
            float(cholesterol),
            remarks,
            id
        ))

        conn.commit()
        conn.close()
        return redirect("/")

    cursor.execute("SELECT * FROM patients WHERE id = ?", (id,))
    patient = cursor.fetchone()
    conn.close()

    if patient is None:
        return render_template("message.html", title="Not Found", message="Patient record not found.", back_url="/")

    return render_template("edit_patient.html", patient=patient)


@app.route("/delete/<int:id>")
def delete_patient(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM patients WHERE id = ?", (id,))

    conn.commit()
    conn.close()

    return redirect("/")


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
