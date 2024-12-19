import mysql.connector as pymysql
from datetime import datetime

passwrd = None
db = None  
C = None

def base_check():
    check = 0
    db = pymysql.connect(host="localhost", user="root", password=passwrd)
    cursor = db.cursor()
    cursor.execute('SHOW DATABASES')
    result = cursor.fetchall()
    for r in result:
        for i in r:
            if i == 'clinic_management':
                cursor.execute('USE clinic_management')
                check = 1
    if check != 1:
        create_database()

def table_check():
    db = pymysql.connect(host="localhost", user="root", password=passwrd)
    cursor = db.cursor()
    cursor.execute('SHOW DATABASES')
    result = cursor.fetchall()
    for r in result:
        for i in r:
            if i == 'clinic_management':
                cursor.execute('USE clinic_management')
                cursor.execute('SHOW TABLES')
                result = cursor.fetchall()
                if len(result) < 3:
                    create_tables()
                else:
                    print('      Booting systems...')

def create_database():
    try:
        db = pymysql.connect(host="localhost", user="root", password=passwrd)
        cursor = db.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS clinic_management")
        db.commit()
        db.close()
        print("Database 'clinic_management' created successfully.")
    except pymysql.Error as e:
        print(f"Error creating database: {str(e)}")

def create_tables():
    try:
        db = pymysql.connect(host="localhost", user="root", password=passwrd, database="clinic_management")
        cursor = db.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                PATIENT_ID INT PRIMARY KEY AUTO_INCREMENT,
                NAME VARCHAR(255),
                AGE INT,
                GENDER VARCHAR(10),
                PHONE_NO VARCHAR(15)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS doctors (
                DOCTOR_ID INT PRIMARY KEY AUTO_INCREMENT,
                NAME VARCHAR(255),
                SPECIALIZATION VARCHAR(255),
                PHONE_NO VARCHAR(15)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS appointments (
                APPOINTMENT_ID INT PRIMARY KEY AUTO_INCREMENT,
                PATIENT_ID INT,
                DOCTOR_ID INT,
                APPOINTMENT_DATE DATE,
                TIME_SLOT VARCHAR(10),
                STATUS VARCHAR(20) DEFAULT 'Scheduled',
                FOREIGN KEY (PATIENT_ID) REFERENCES patients(PATIENT_ID),
                FOREIGN KEY (DOCTOR_ID) REFERENCES doctors(DOCTOR_ID)
            )
        """)
        
        db.commit()
        db.close()
        print("Tables 'patients', 'doctors', and 'appointments' created successfully.")
    except pymysql.Error as e:
        print(f"Error creating tables: {str(e)}")

def add_patient():
    name = input("Enter Patient Name: ")
    age = int(input("Enter Patient Age: "))
    gender = input("Enter Gender (Male/Female): ")
    phone_no = input("Enter Phone Number: ")
    data = (name, age, gender, phone_no)
    sql = "INSERT INTO patients (NAME, AGE, GENDER, PHONE_NO) VALUES (%s, %s, %s, %s)"
    try:
        C.execute(sql, data)
        db.commit()
        print('Patient added successfully...')
    except pymysql.Error as e:
        print(f"Error adding patient: {str(e)}")

def view_patients():
    C.execute("SELECT * FROM patients")
    result = C.fetchall()
    for r in result:
        print(r)

def add_doctor():
    name = input("Enter Doctor Name: ")
    specialization = input("Enter Specialization: ")
    phone_no = input("Enter Phone Number: ")
    data = (name, specialization, phone_no)
    sql = "INSERT INTO doctors (NAME, SPECIALIZATION, PHONE_NO) VALUES (%s, %s, %s)"
    try:
        C.execute(sql, data)
        db.commit()
        print('Doctor added successfully...')
    except pymysql.Error as e:
        print(f"Error adding doctor: {str(e)}")

def view_doctors():
    C.execute("SELECT * FROM doctors")
    result = C.fetchall()
    for r in result:
        print(r)

def book_appointment():
    patient_id = int(input("Enter Patient ID: "))
    doctor_id = int(input("Enter Doctor ID: "))
    appointment_date = input("Enter Appointment Date (YYYY-MM-DD): ")
    time_slot = input("Enter Time Slot (e.g., 10:00 AM): ")
    data = (patient_id, doctor_id, appointment_date, time_slot)
    sql = "INSERT INTO appointments (PATIENT_ID, DOCTOR_ID, APPOINTMENT_DATE, TIME_SLOT) VALUES (%s, %s, %s, %s)"
    try:
        C.execute(sql, data)
        db.commit()
        print('Appointment booked successfully...')
    except pymysql.Error as e:
        print(f"Error booking appointment: {str(e)}")

def view_appointments():
    C.execute("""
        SELECT 
            a.APPOINTMENT_ID, 
            p.NAME AS PATIENT_NAME, 
            d.NAME AS DOCTOR_NAME, 
            a.APPOINTMENT_DATE, 
            a.TIME_SLOT, 
            a.STATUS 
        FROM appointments a 
        JOIN patients p ON a.PATIENT_ID = p.PATIENT_ID 
        JOIN doctors d ON a.DOCTOR_ID = d.DOCTOR_ID
    """)
    result = C.fetchall()
    for r in result:
        print(r)
def main():
    global passwrd
    passwrd = input("Enter password for MySQL: ")
    base_check()
    table_check()
    global db, C
    db = pymysql.connect(host="localhost", user="root", password=passwrd, database="clinic_management")
    C = db.cursor()
    while True:
        log = input("For Admin: A, Exit: X ::: ")
        if log.upper() == "A":
            while True:
                menu = input('''Add Patient: AP, View Patients: VP, Add Doctor: AD, View Doctors: VD, Book Appointment: BA, View Appointments: VA, Exit: X ::: ''')
                if menu.upper() == 'AP':
                    add_patient()
                elif menu.upper() == 'VP':
                    view_patients()
                elif menu.upper() == 'AD':
                    add_doctor()
                elif menu.upper() == 'VD':
                    view_doctors()
                elif menu.upper() == 'BA':
                    book_appointment()
                elif menu.upper() == 'VA':
                    view_appointments()
                elif menu.upper() == 'X':
                    break
                else:
                    print("Wrong Input")         
        elif log.upper() == "X":
            print("THANK YOU FOR USING CLINIC MANAGEMENT SYSTEM")
            break
        else:
            print("Wrong Input")
if __name__ == "__main__":
    main()