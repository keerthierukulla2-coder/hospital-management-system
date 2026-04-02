import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "hospital-secret-key"

DATABASE = "hospital.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            gender TEXT,
            disease TEXT,
            phone TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            specialty TEXT,
            phone TEXT,
            email TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pharmacy (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            medicine_name TEXT,
            quantity INTEGER,
            price REAL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            role TEXT,
            email TEXT
        )
    """)

    # ✅ Insert sample data ONLY if tables are empty

    # Patients
    cursor.execute("SELECT COUNT(*) FROM patients")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("""
            INSERT INTO patients (name, age, gender, disease, phone)
            VALUES (?, ?, ?, ?, ?)
        """, [
            ("John Doe", 30, "Male", "Fever", "1234567890"),
            ("Emma Watson", 25, "Female", "Cold", "9876543210"),
        ])

    # Doctors
    cursor.execute("SELECT COUNT(*) FROM doctors")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("""
            INSERT INTO doctors (name, specialty, phone, email)
            VALUES (?, ?, ?, ?)
        """, [
            ("Dr. Smith", "Cardiology", "1112223333", "smith@hospital.com"),
            ("Dr. Brown", "Neurology", "4445556666", "brown@hospital.com"),
        ])

    # Pharmacy
    cursor.execute("SELECT COUNT(*) FROM pharmacy")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("""
            INSERT INTO pharmacy (medicine_name, quantity, price)
            VALUES (?, ?, ?)
        """, [
            ("Paracetamol", 100, 5.50),
            ("Ibuprofen", 50, 8.00),
        ])

    # Admins
    cursor.execute("SELECT COUNT(*) FROM admins")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("""
            INSERT INTO admins (name, role, email)
            VALUES (?, ?, ?)
        """, [
            ("Alice", "Manager", "alice@hospital.com"),
            ("Bob", "HR", "bob@hospital.com"),
        ])

    conn.commit()
    conn.close()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/patients")
def patients():
    conn = get_db_connection()
    patients = conn.execute("SELECT * FROM patients ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("patients.html", patients=patients)


@app.route("/patients/add", methods=["POST"])
def add_patient():
    name = request.form["name"]
    age = request.form["age"]
    gender = request.form["gender"]
    disease = request.form["disease"]
    phone = request.form["phone"]

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO patients (name, age, gender, disease, phone) VALUES (?, ?, ?, ?, ?)",
        (name, age, gender, disease, phone)
    )
    conn.commit()
    conn.close()
    flash("Patient added successfully.")
    return redirect(url_for("patients"))


@app.route("/patients/delete/<int:patient_id>")
def delete_patient(patient_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM patients WHERE id = ?", (patient_id,))
    conn.commit()
    conn.close()
    flash("Patient deleted successfully.")
    return redirect(url_for("patients"))


@app.route("/doctors")
def doctors():
    conn = get_db_connection()
    doctors = conn.execute("SELECT * FROM doctors ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("doctors.html", doctors=doctors)


@app.route("/doctors/add", methods=["POST"])
def add_doctor():
    name = request.form["name"]
    specialty = request.form["specialty"]
    phone = request.form["phone"]
    email = request.form["email"]

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO doctors (name, specialty, phone, email) VALUES (?, ?, ?, ?)",
        (name, specialty, phone, email)
    )
    conn.commit()
    conn.close()
    flash("Doctor added successfully.")
    return redirect(url_for("doctors"))


@app.route("/doctors/delete/<int:doctor_id>")
def delete_doctor(doctor_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM doctors WHERE id = ?", (doctor_id,))
    conn.commit()
    conn.close()
    flash("Doctor deleted successfully.")
    return redirect(url_for("doctors"))


@app.route("/pharmacy")
def pharmacy():
    conn = get_db_connection()
    medicines = conn.execute("SELECT * FROM pharmacy ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("pharmacy.html", medicines=medicines)


@app.route("/pharmacy/add", methods=["POST"])
def add_medicine():
    medicine_name = request.form["medicine_name"]
    quantity = request.form["quantity"]
    price = request.form["price"]

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO pharmacy (medicine_name, quantity, price) VALUES (?, ?, ?)",
        (medicine_name, quantity, price)
    )
    conn.commit()
    conn.close()
    flash("Medicine added successfully.")
    return redirect(url_for("pharmacy"))


@app.route("/pharmacy/delete/<int:medicine_id>")
def delete_medicine(medicine_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM pharmacy WHERE id = ?", (medicine_id,))
    conn.commit()
    conn.close()
    flash("Medicine deleted successfully.")
    return redirect(url_for("pharmacy"))


@app.route("/admins")
def admins():
    conn = get_db_connection()
    admins = conn.execute("SELECT * FROM admins ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("admins.html", admins=admins)


@app.route("/admins/add", methods=["POST"])
def add_admin():
    name = request.form["name"]
    role = request.form["role"]
    email = request.form["email"]

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO admins (name, role, email) VALUES (?, ?, ?)",
        (name, role, email)
    )
    conn.commit()
    conn.close()
    flash("Admin added successfully.")
    return redirect(url_for("admins"))


@app.route("/admins/delete/<int:admin_id>")
def delete_admin(admin_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM admins WHERE id = ?", (admin_id,))
    conn.commit()
    conn.close()
    flash("Admin deleted successfully.")
    return redirect(url_for("admins"))


iif __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)