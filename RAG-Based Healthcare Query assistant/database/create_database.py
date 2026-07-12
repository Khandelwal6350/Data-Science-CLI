from pathlib import Path
import sqlite3
import pandas as pd

# =====================================================
# PROJECT PATHS
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_PATH = BASE_DIR / "data" / "healthcare_dataset.csv"
DATABASE_PATH = BASE_DIR / "database" / "hospital.db"

# =====================================================
# LOAD DATASET
# =====================================================

print("=" * 60)
print("Loading Dataset...")
print("=" * 60)

df = pd.read_csv(DATASET_PATH)

print(f"Rows    : {df.shape[0]}")
print(f"Columns : {df.shape[1]}")

# =====================================================
# DATA VALIDATION
# =====================================================

print("\nChecking Missing Values...\n")
print(df.isnull().sum())

print("\nChecking Duplicate Rows...")

duplicates = df.duplicated().sum()
print(f"Duplicate Rows : {duplicates}")

if duplicates > 0:
    df = df.drop_duplicates()
    print("Duplicate rows removed.")

# =====================================================
# DATE CONVERSION
# =====================================================

df["Date of Admission"] = pd.to_datetime(
    df["Date of Admission"],
    errors="coerce"
)

df["Discharge Date"] = pd.to_datetime(
    df["Discharge Date"],
    errors="coerce"
)

# =====================================================
# SQLITE CONNECTION
# =====================================================

conn = sqlite3.connect(DATABASE_PATH)

conn.execute("PRAGMA foreign_keys = ON")

cursor = conn.cursor()

# =====================================================
# DROP OLD TABLES
# =====================================================

cursor.execute("DROP TABLE IF EXISTS billing")
cursor.execute("DROP TABLE IF EXISTS medical_records")
cursor.execute("DROP TABLE IF EXISTS admissions")
cursor.execute("DROP TABLE IF EXISTS patients")

# =====================================================
# CREATE TABLES
# =====================================================

cursor.execute("""
CREATE TABLE patients(

    patient_id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT,

    age INTEGER,

    gender TEXT,

    blood_type TEXT

)
""")

cursor.execute("""
CREATE TABLE admissions(

    admission_id INTEGER PRIMARY KEY AUTOINCREMENT,

    patient_id INTEGER,

    hospital TEXT,

    doctor TEXT,

    room_number INTEGER,

    admission_type TEXT,

    admission_date DATE,

    discharge_date DATE,

    FOREIGN KEY(patient_id)
    REFERENCES patients(patient_id)

)
""")

cursor.execute("""
CREATE TABLE medical_records(

    record_id INTEGER PRIMARY KEY AUTOINCREMENT,

    patient_id INTEGER,

    medical_condition TEXT,

    medication TEXT,

    test_results TEXT,

    FOREIGN KEY(patient_id)
    REFERENCES patients(patient_id)

)
""")

cursor.execute("""
CREATE TABLE billing(

    bill_id INTEGER PRIMARY KEY AUTOINCREMENT,

    patient_id INTEGER,

    insurance_provider TEXT,

    billing_amount REAL,

    FOREIGN KEY(patient_id)
    REFERENCES patients(patient_id)

)
""")

conn.commit()

print("\nTables Created Successfully")

# =====================================================
# INSERT DATA
# =====================================================

print("Inserting Data...")

for _, row in df.iterrows():

    cursor.execute("""

    INSERT INTO patients(

        name,

        age,

        gender,

        blood_type

    )

    VALUES(?,?,?,?)

    """, (

        row["Name"],

        row["Age"],

        row["Gender"],

        row["Blood Type"]

    ))

    patient_id = cursor.lastrowid

    cursor.execute("""

    INSERT INTO admissions(

        patient_id,

        hospital,

        doctor,

        room_number,

        admission_type,

        admission_date,

        discharge_date

    )

    VALUES(?,?,?,?,?,?,?)

    """, (

        patient_id,

        row["Hospital"],

        row["Doctor"],

        row["Room Number"],

        row["Admission Type"],

        row["Date of Admission"].strftime("%Y-%m-%d"),

        row["Discharge Date"].strftime("%Y-%m-%d")

    ))

    cursor.execute("""

    INSERT INTO medical_records(

        patient_id,

        medical_condition,

        medication,

        test_results

    )

    VALUES(?,?,?,?)

    """, (

        patient_id,

        row["Medical Condition"],

        row["Medication"],

        row["Test Results"]

    ))

    cursor.execute("""

    INSERT INTO billing(

        patient_id,

        insurance_provider,

        billing_amount

    )

    VALUES(?,?,?)

    """, (

        patient_id,

        row["Insurance Provider"],

        row["Billing Amount"]

    ))

conn.commit()

print("Data Inserted Successfully")

# =====================================================
# CREATE INDEXES
# =====================================================

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_condition
ON medical_records(medical_condition)
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_doctor
ON admissions(doctor)
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_hospital
ON admissions(hospital)
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_admission_date
ON admissions(admission_date)
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_insurance
ON billing(insurance_provider)
""")

conn.commit()

print("Indexes Created Successfully")

# =====================================================
# VERIFY DATABASE
# =====================================================

print("\nDatabase Summary")

patients = cursor.execute(
    "SELECT COUNT(*) FROM patients"
).fetchone()[0]

admissions = cursor.execute(
    "SELECT COUNT(*) FROM admissions"
).fetchone()[0]

records = cursor.execute(
    "SELECT COUNT(*) FROM medical_records"
).fetchone()[0]

billing = cursor.execute(
    "SELECT COUNT(*) FROM billing"
).fetchone()[0]

print(f"Patients        : {patients}")
print(f"Admissions      : {admissions}")
print(f"Medical Records : {records}")
print(f"Billing Records : {billing}")

conn.close()

print("\nDatabase Ready Successfully.")