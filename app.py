from flask import Flask, render_template, request, redirect, url_for, session
from supabase import create_client
import uuid
import bcrypt
from utils.encrypt import hash_password, check_password
import json
import os
import openai
import time
import g4f
import requests

app = Flask(__name__)

# Supabase configuration
SUPABASE_URL = ''
SUPABASE_KEY = ''
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Initialize OpenAI API key
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email_address = request.form['email']
        password = request.form['password']
        confirm_password = request.form['password_confirmation']

        if password == confirm_password:
            # Create a new user
            credentials = {
                'email': email_address,
                'password': password
            }
            user = supabase.auth.sign_up(credentials)

            # Hash the password
            # hashed_password = hash_password(password)


            # Insert data to the database Users table
            supabase.table('Users').insert({
                'user_id': str(uuid.uuid4()),
                'first_name': first_name,
                'last_name': last_name,
                'email': email_address,
                'password': password
            }).execute()

            return render_template('patientUpdate.html', message='User created successfully')


    return render_template('signup.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    # Fetch the appointments from the database
    # Fetch appointments from the database
    appointments_query = supabase.table('Appointments').select('*')
    response = appointments_query.execute()
    response = response.json()
    response = json.loads(response)
    appointments = []

    for appointment in response['data']:
        appointments.append(appointment)

    # Fetch reminders
    reminders_query = supabase.table('Reminders').select('*')
    response = reminders_query.execute()
    response = response.json()
    response = json.loads(response)
    reminders = []

    for reminder in response['data']:
        reminders.append(reminder)


    # Fetch the queries
    queries_query = supabase.table('Queries').select('*')
    response = queries_query.execute()
    response = response.json()
    response = json.loads(response)
    queries = []

    for query in response['data']:
        queries.append(query)

    if request.method == 'POST':
        email_address = request.form['email']
        password = request.form['password']

        # Hash the password


        # Login user
        credentials = {
            'email': email_address,
            'password': password
        }
        # user = supabase.auth.sign_in(credentials)

        # Check if the user exists
        # Fetch user data based on email address
        user_query = supabase.table('Users').select('*').eq('email', email_address)
        response = user_query.execute()
        # print(response)

        response = response.json()
        
        # Convert the response to a dictionary
        user = json.loads(response)
        print(user['data'][0]['password'])
        
    
        if password == user['data'][0]['password']:
            print("Entered Usage")

            # Get first name
            first_name = user['data'][0]['first_name']

            return render_template('patientDashboard.html', message='User logged in successfully', name=first_name, appointments=appointments, reminders = reminders, queries = queries)
        
        return render_template('login.html', message='Incorrect password', appointments=appointments, reminders = reminders, queries = queries)
        
    return render_template('login.html', appointments=appointments, reminders = reminders, queries = queries)

# Admin Login
@app.route('/adminLogin', methods=['POST', 'GET'])
def adminLogin():
    # Fetch the appointments from the database
    # Fetch appointments from the database
    appointments_query = supabase.table('Appointments').select('*')
    response = appointments_query.execute()
    response = response.json()
    response = json.loads(response)
    appointments = []

    for appointment in response['data']:
        appointments.append(appointment)

    # Fetch reminders
    reminders_query = supabase.table('Reminders').select('*')
    response = reminders_query.execute()
    response = response.json()
    response = json.loads(response)
    reminders = []

    for reminder in response['data']:
        reminders.append(reminder)


    # Fetch the queries
    queries_query = supabase.table('Queries').select('*')
    response = queries_query.execute()
    response = response.json()
    response = json.loads(response)
    queries = []

    for query in response['data']:
        queries.append(query)

    if request.method == 'POST':
        email_address = request.form['email']
        password = request.form['password']

        # Hash the password


        # Login user
        credentials = {
            'email': email_address,
            'password': password
        }
        # user = supabase.auth.sign_in(credentials)

        # Check if the user exists
        # Fetch user data based on email address
        if email_address == 'admin@second-life.com':
            if password == 'admin':
                print("Entered Usage")

                return render_template('adminDashboard.html', message='User logged in successfully', name='Admin', appointments=appointments, reminders = reminders, queries = queries)

        else:
            return render_template('adminLogin.html', message='Incorrect password')
        
        return render_template('adminLogin.html', message='Incorrect password')
    return render_template('adminLogin.html')

# Patient Dashboard Update Page
@app.route('/patientUpdate', methods=['POST', 'GET'])
def patientUpdate():
    # Fetch the appointments from the database
    # Fetch appointments from the database
    appointments_query = supabase.table('Appointments').select('*')
    response = appointments_query.execute()
    response = response.json()
    response = json.loads(response)
    appointments = []

    for appointment in response['data']:
        appointments.append(appointment)

    # Fetch reminders
    reminders_query = supabase.table('Reminders').select('*')
    response = reminders_query.execute()
    response = response.json()
    response = json.loads(response)
    reminders = []

    for reminder in response['data']:
        reminders.append(reminder)


    # Fetch the queries
    queries_query = supabase.table('Queries').select('*')
    response = queries_query.execute()
    response = response.json()
    response = json.loads(response)
    queries = []

    for query in response['data']:
        queries.append(query)

    if request.method == 'POST':
            # Retrieve form data
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            weight = request.form['weight']
            height = request.form['height']
            phone_no = request.form['phone_no']
            address = request.form['address']
            email = request.form['email']
            gender = request.form['gender']
            dob = request.form['dob']
            emergency_contact = request.form['emergency_contact']
            emergency_phone = request.form['emergency_phone']
            consulting_doctor = request.form['consulting_doctor']
            specialization = request.form['specialization']


            # Process the data as needed (e.g., update database)
            # For demonstration purposes, let's print the data
            print("Form Data:")
            print(f"First Name: {first_name}")
            print(f"Last Name: {last_name}")
            print(f"Weight: {weight}")
            print(f"Height: {height}")
            print(f"Phone Number: {phone_no}")
            print(f"Address: {address}")
            print(f"Date of Birth: {dob}")
            print(f"Emergency Contact: {emergency_contact}")
            print(f"Emergency Phone: {emergency_phone}")
            print(f"Consulting Doctor: {consulting_doctor}")
            print(f"Specialization: {specialization}")

            # You can add code here to update the database with the form data
                        # Assuming you have the form data in variables like first_name, last_name, etc.
            form_data = {
                'first_name': first_name,
                'last_name': last_name,
                'weight': weight,
                'height': height,
                'phone_no': phone_no,
                'address': address,
                'dob': dob,
                'emergency_contact': emergency_contact,
                'emergency_phone': emergency_phone,
                'consulting_doctor': consulting_doctor,
                'specialization': specialization,
                'email': email,
                'gender': gender
                
            }

            # Insert data into Supabase table
            response = supabase.table('Patients').insert([form_data]).execute()


            # Render the template with a success message or redirect to another page
            return render_template('patientUpdate.html', success_message="Data successfully updated!")
    
        

    return render_template('patientUpdate.html')



# Patient Dashboard
@app.route('/patientDashboard', methods=['POST', 'GET'])
def patientDashboard():
    # Fetch the appointments from the database
    # Fetch appointments from the database
    appointments_query = supabase.table('Appointments').select('*')
    response = appointments_query.execute()
    response = response.json()
    response = json.loads(response)
    appointments = []

    for appointment in response['data']:
        appointments.append(appointment)

    # Fetch reminders
    reminders_query = supabase.table('Reminders').select('*')
    response = reminders_query.execute()
    response = response.json()
    response = json.loads(response)
    reminders = []

    for reminder in response['data']:
        reminders.append(reminder)


    # Fetch the queries
    queries_query = supabase.table('Queries').select('*')
    response = queries_query.execute()
    response = response.json()
    response = json.loads(response)
    queries = []

    for query in response['data']:
        queries.append(query)

    
    if request.method == 'POST':
        return render_template('patientDashboard.html', appointments=appointments, reminders = reminders, queries = queries)
    return render_template('patientDashboard.html', appointments=appointments, reminders = reminders, queries = queries)


@app.route('/adminDashboard', methods=['POST', 'GET'])
def adminDashboard():
    # Fetch the appointments from the database
    # Fetch appointments from the database
    appointments_query = supabase.table('Appointments').select('*')
    response = appointments_query.execute()
    response = response.json()
    response = json.loads(response)
    appointments = []

    for appointment in response['data']:
        appointments.append(appointment)

    # Fetch reminders
    reminders_query = supabase.table('Reminders').select('*')
    response = reminders_query.execute()
    response = response.json()
    response = json.loads(response)
    reminders = []

    for reminder in response['data']:
        reminders.append(reminder)


    # Fetch the queries
    queries_query = supabase.table('Queries').select('*')
    response = queries_query.execute()
    response = response.json()
    response = json.loads(response)
    queries = []

    for query in response['data']:
        queries.append(query)

    
    if request.method == 'POST':
        return render_template('adminDashboard.html', appointments=appointments, reminders = reminders, queries = queries)
    return render_template('adminDashboard.html', appointments=appointments, reminders = reminders, queries = queries)

# Upload Reports
@app.route('/uploadReport', methods=['POST', 'GET'])
def uploadReport():
    if request.method == 'POST':
        # Retrieve form data file
        report = request.files['report']
        report_name = request.form['report_name']

        # Save the file to the uploads folder
        report.save(f'static/uploads/{report_name}.pdf')

        # Render the template with a success message or redirect to another page
        return render_template('uploadReport.html', success_message="Report successfully uploaded!")

    return render_template('uploadReport.html')

# viewReport
@app.route('/viewReport', methods=['POST', 'GET'])
def viewReport():
    # List all PDFs in static/uploads/
    
    files = os.listdir('static/uploads/')
    print(files)

    return render_template('viewReport.html', file_names=files)

# Add Queries and view queries route
@app.route('/queries', methods=['POST', 'GET'])
def queries():

    # Fetch doctors from the database
    doctors_query = supabase.table('Doctors').select('*')
    response = doctors_query.execute()
    response = response.json()
    response = json.loads(response)
    doctors = []

    for doctor in response['data']:
        doctors.append(doctor['doctor_name'])

    # Fetch Queries from the database
    queries_query = supabase.table('Queries').select('*')
    response = queries_query.execute()
    response = response.json()
    response = json.loads(response)

    queries = []

    for query in response['data']:
        queries.append(query)
    print(queries)
    if request.method == 'POST':
        # Retrieve form data
        query = request.form['query']
        query_name = request.form['query_name']
        doctor = request.form['doctor']

        # Process the data as needed (e.g., update database)
        # For demonstration purposes, let's print the data
        print("Form Data:")
        print(f"Query: {query}")
        print(f"Query Name: {query_name}")
        print(f"Doctor: {doctor}")


        # You can add code here to update the database with the form data
                    # Assuming you have the form data in variables like first_name, last_name, etc.
        form_data = {
            'query': query,
            'query_name': query_name,
            'doctor': doctor
        }

        # Insert data into Supabase table
        response = supabase.table('Queries').insert([form_data]).execute()


        # Render the template with a success message or redirect to another page
        return render_template('queries.html', success_message="Query successfully uploaded!", doctors=doctors, queries=queries)
    return render_template('queries.html', doctors=doctors, queries=queries)

# Book Appointment Route
@app.route('/bookAppointments', methods=['POST', 'GET'])
def bookAppointments():

    # Fetch doctors from the database
    doctors_query = supabase.table('Doctors').select('*')
    response = doctors_query.execute()
    response = response.json()
    response = json.loads(response)
    doctors = []

    for doctor in response['data']:
        doctors.append(doctor['doctor_name'])

    if request.method == 'POST':
        # Retrieve form data
        appointment_date = request.form['appointment_date']
        appointment_time = request.form['appointment_time']
        appointment_reason = request.form['appointment_reason']
        appointment_doctor = request.form['appointment_doctor']

        # Process the data as needed (e.g., update database)
        # For demonstration purposes, let's print the data
        print("Form Data:")
        print(f"Appointment Date: {appointment_date}")
        print(f"Appointment Time: {appointment_time}")
        print(f"Appointment Reason: {appointment_reason}")
        print(f"Appointment Doctor: {appointment_doctor}")

        # You can add code here to update the database with the form data
                    # Assuming you have the form data in variables like first_name, last_name, etc.
        form_data = {
            'appointment_date': appointment_date,
            'appointment_time': appointment_time,
            'appointment_reason': appointment_reason,
            'appointment_doctor': appointment_doctor
        }

        # Insert data into Supabase table
        response = supabase.table('Appointments').insert([form_data]).execute()

        bot_message = "Appointment booked with " + appointment_doctor + " on " + appointment_date + " at " + appointment_time + " for " + appointment_reason
        bot_token = ''
        bot_chatID = ''
        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

        response = requests.get(send_text)

        # Render the template with a success message or redirect to another page
        return render_template('bookAppointments.html', success_message="Appointment successfully booked!")
    return render_template('bookAppointments.html', doctors=doctors)

# View Appointments
@app.route('/viewAppointments', methods=['POST', 'GET'])
def viewAppointments():

    # Fetch appointments from the database
    appointments_query = supabase.table('Appointments').select('*')
    response = appointments_query.execute()
    response = response.json()
    response = json.loads(response)
    appointments = []

    for appointment in response['data']:
        appointments.append(appointment)

    print(appointments)


    return render_template('viewAppointments.html', appointments=appointments)


# Add Doctor
@app.route('/addDoctor', methods=['POST', 'GET'])
def addDoctor():
    if request.method == 'POST':
        doctor_name = request.form['doctor_name']
        specialty = request.form['specialty']
        hospital = request.form['hospital']

        new_doctor = {
            'doctor_name': doctor_name,
            'specialty': specialty,
            'hospital': hospital
            # Add any other fields as needed
        }

        # Insert data into Supabase table
        response = supabase.table('Doctors').insert([new_doctor]).execute()


        # Render the template with a success message or redirect to another page
        return render_template('addDoctor.html', success_message="Doctor successfully added!")
     
    return render_template('addDoctor.html')

# Ask GPT
@app.route('/askGPT', methods=['POST', 'GET'])
def askGPT():



    # Fetch Queries from the database
    queries_query = supabase.table('GPT_Queries').select('*')
    response = queries_query.execute()
    response = response.json()
    response = json.loads(response)

    queries = []

    for query in response['data']:
        queries.append(query)
    print(queries)

    if request.method == 'POST':
        try:
            # Retrieve form data
            query = request.form['query']

            # Process the data as needed (e.g., update database)
            # For demonstration purposes, let's print the data
            print("Form Data:")
            print(f"Query: {query}")

            # # Use ChatGPT to generate a response
            # response = openai.Completion.create(
            #     engine="ada",  # You may need to adjust the engine based on availability and use case
            #     prompt=query,
            #     max_tokens=100  # Adjust as needed
            # )
            # generated_response = response.choices[0].text.strip()

                    
            # Using automatic a provider for the given model
            ## Normal response
            response = g4f.ChatCompletion.create(
                model=g4f.models.gpt_4,
                messages=[{"role": "doctor", "content": query}],
            )  

            print(response)

        
            # Form data
            form_data = {
                'query': query,
                'reply': response
            }


            # Insert data into Supabase table
            supabase.table('GPT_Queries').insert([form_data]).execute()

            # Render the template with the generated response
            return render_template('askGPT.html', success_message="Query successfully uploaded!", queries = queries)
        except:
            return render_template('error.html')

    return render_template('askGPT.html', queries = queries)

# Error Route
@app.route('/error', methods=['POST', 'GET'])
def error():
    return render_template('error.html')

@app.route('/addReminders', methods=['POST', 'GET'])


def addReminder():
    # Fetch reminders from the database
    reminders_query = supabase.table('Reminders').select('*')
    response = reminders_query.execute()
    response = response.json()
    response = json.loads(response)
    reminders = []


    for reminder in response['data']:
        reminders.append(reminder)
    print(reminders)
    if request.method == 'POST':
        reminder_name = request.form['reminder_name']
        reminder_date = request.form['reminder_date']
        reminder_time = request.form['reminder_time']
        reminder_description = request.form['reminder_description']

        new_reminder = {
            'reminder_name': reminder_name,
            'reminder_date': reminder_date,
            'reminder_time': reminder_time,
            'reminder_description': reminder_description
            # Add any other fields as needed
        }

        # Insert data into Supabase table
        response = supabase.table('Reminders').insert([new_reminder]).execute()

        bot_message = "Reminder: " + reminder_name + " on " + reminder_date + " at " + reminder_time + " Description: " + reminder_description
        bot_token = ''
        bot_chatID = ''
        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

        response = requests.get(send_text)


        # Render the template with a success message or redirect to another page
        return render_template('addReminders.html', success_message="Reminder successfully added!", reminders = reminders)
     
    return render_template('addReminders.html', reminders = reminders)

@app.route('/insurance', methods=['POST', 'GET'])
def insurance():
    # Fetch insurance from the database
    insurance_query = supabase.table('Insurance').select('*')
    response = insurance_query.execute()

    response = response.json()
    response = json.loads(response)
    insurances = []

    for insurance in response['data']:
        insurances.append(insurance)

    if request.method == 'POST':
        insured_name = request.form['insured_name']
        date_of_birth = request.form['date_of_birth']
        contact_number = request.form['contact_number']
        insurance_type = request.form['insurance_type']
        policy_number = request.form['policy_number']

        insurance_data = {
            'insured_name': insured_name,
            'date_of_birth': date_of_birth,
            'contact_number': contact_number,
            'insurance_type': insurance_type,
            'policy_number': policy_number
            # Add any other fields as needed
        }

        # Insert data into Supabase table
        response = supabase.table('Insurance').insert([insurance_data]).execute()

        bot_message = "Insurance: " + insurance_type + " Policy Number: " + policy_number + " Insured Name: " + insured_name + " Date of Birth: " + date_of_birth + " Contact Number: " + contact_number
        bot_token = ''
        bot_chatID = ''
        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

        response = requests.get(send_text)

        # Render the template with a success message or redirect to another page
        return render_template('insurance.html', success_message="Insurance information submitted successfully!", insurances = insurances)

    return render_template('insurance.html', insurances = insurances)

# View all patients
@app.route('/viewPatients', methods=['POST', 'GET'])
def viewPatients():
    # Fetch patients from the database
    patients_query = supabase.table('Patients').select('*')
    response = patients_query.execute()
    response = response.json()
    response = json.loads(response)
    patients = []

    for patient in response['data']:
        patients.append(patient)

    print(patients)


    return render_template('viewPatients.html', patients=patients)

if __name__ == '__main__':  
    # Run on port 4000
    app.run(port=4000, debug=True)

