import customtkinter as ctk
import tkinter.messagebox as tkmb
import sqlite3 #Library for SQL relational database
import hashlib  #For encryption/Decryption

import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import re

#-------------------///////----------------------------

# This function is used to create DB and its Tables
def createDB():
    # Connect to database
	conn = sqlite3.connect('Hajj_Portal.db')
	c = conn.cursor()
	# create a table to store the pilgrim information
	c.execute('''
			CREATE TABLE IF NOT EXISTS pilgrims (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				iqama_number TEXT NOT NULL UNIQUE,
				first_name TEXT NOT NULL,
				last_name TEXT NOT NULL,
				date_of_birth TEXT NOT NULL,
				contact_number TEXT NOT NULL UNIQUE,
				companions INTEGER NOT NULL,
				package_company TEXT NOT NULL,
				status TEXT DEFAULT 'Pending',
				comment TEXT DEFAULT ''
			)
		''')
        
    # create a table to store the user data
	c.execute('''CREATE TABLE IF NOT EXISTS users
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
					iqama_number TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL)''')
	conn.commit()
    # close the database connection
	conn.close()

#-----------------------------------------------
#------------Sign Up Portion Started------------

def signUp(user_entry,user_pass,app):
    # If the DB is not created then it create DB and the 2 tables. 
    createDB()
    # connect to database
    conn = sqlite3.connect('Hajj_Portal.db')
    c = conn.cursor()

    c.execute('SELECT * FROM users WHERE iqama_number = ?', (user_entry,))
    result = c.fetchone()
    if result is not None:
        # Already have a record
        tkmb.showinfo(title="Failed",message="Already Registered!!!")
    else:
        # insert new record into the database
        c.execute("INSERT INTO users (iqama_number, password, role) VALUES (?, ?, ?)", (user_entry, hash_encrypt(user_pass), "pilgrim"))
        tkmb.showinfo(title="Succes",message="Registered Successfully!!!")
        app.destroy()
        # commit changes to the database
        conn.commit()
        conn.close()
        login_Page()
    
    # commit changes to the database
    conn.commit()
    conn.close()

#---------------///////---------------

# This function used to display UI and get input from user.
def signUp_Page():
    # Selecting GUI theme - dark, light , system (for system default)
	ctk.set_appearance_mode("dark")

	# Selecting color theme - blue, green, dark-blue
	ctk.set_default_color_theme("blue")

	apps = ctk.CTk()
	apps.geometry("300x360")
	apps.title("Al-Hajj")

	label = ctk.CTkLabel(apps,text="Sign Up")
	label.pack(pady=15)

	frame = ctk.CTkFrame(master=apps)
	frame.pack(pady=20,padx=20,fill='both',expand=True)
    
	vcmd = (apps.register(validate_input), '%P')
	user_iqamaNumLabel = ctk.CTkLabel(master=frame, text="Iqama Number")
	user_iqamaNumLabel.pack()
    
	user_iqamaNum = ctk.CTkEntry(master=frame, validate="key", validatecommand=vcmd)
	user_iqamaNum.pack(pady=15,padx=20)

	user_PassLabel = ctk.CTkLabel(master=frame, text="Password")
	user_PassLabel.pack()
	user_pass= ctk.CTkEntry(master=frame,show="*")
	user_pass.pack(pady=12,padx=10)

	button = ctk.CTkButton(master=frame,text='Register', cursor="hand2", command=lambda: signUp(user_iqamaNum.get(),user_pass.get(),apps))
	button.pack(pady=12,padx=10)
    
	signup_label = ctk.CTkLabel(master=frame,text="Already have account? Sign In!", cursor="hand2")
	signup_label.bind("<Button-1>", lambda event:(apps.destroy(), login_Page()))
	signup_label.pack(pady=12,padx=10)

	apps.mainloop()


#------------Sign Up Portion Ended------------
#-------------------///////-------------------
#------------Login Portion Started------------

# This funtion is used to Encrypts the given text using a hashing algorithm
def hash_encrypt(text):
    """
    Encrypts the given text using a hashing algorithm
    """
    # Convert the text to bytes
    text_bytes = text.encode('utf-8')

    # Hash the bytes using SHA-256 algorithm
    hash_object = hashlib.sha256(text_bytes)

    # Convert the hashed bytes to hexadecimal representation
    hash_hex = hash_object.hexdigest()

    # Return the hashed text
    return hash_hex

#---------------///////---------------

# This function is used for login purpose.
def login(user_entry,user_pass,app):
    # connect to database
    conn = sqlite3.connect('Hajj_Portal.db')
    c = conn.cursor()
    
	#Creating a view
    c.execute("DROP VIEW IF EXISTS Login_Credentials;")
    c.execute("CREATE VIEW Login_Credentials AS SELECT iqama_number, password, role FROM users;")

    # query the database for the given credentials
    c.execute('SELECT password,role FROM Login_Credentials WHERE iqama_number = ?', (user_entry.get(),))
    result = c.fetchone()
    if result is not None:
        stored_hash = result[0]
		# hash the input password and compare it to the stored hash
        input_hash = hash_encrypt(user_pass.get())
        if input_hash == stored_hash:
			# login successful
            tkmb.showinfo(title="Login Successful",message="You have logged in Successfully.")
            if(result[1]== "pilgrim"):
                app.destroy()
                application_Form()
            elif(result[1]=="package_company"):
                app.destroy()
                admin_Dashboard()
        else:
			# login failed
            tkmb.showerror(title="Login Failed",message="Invalid password. Try Again!!!!!")
    else:
		# login failed
        tkmb.showerror(title="Login Failed",message="Invalid Username. Try Again!!!!!")
    # close the database connection
    conn.close()

#---------------///////---------------

# This function used to display UI and get input from user.
def login_Page():
    # Selecting GUI theme - dark, light , system (for system default)
	ctk.set_appearance_mode("dark")

	# Selecting color theme - blue, green, dark-blue
	ctk.set_default_color_theme("blue")

	app = ctk.CTk()
	app.geometry("300x350")
	app.title("Al-Hajj")

	label = ctk.CTkLabel(app,text="Sign In")
	label.pack(pady=10)

	frame = ctk.CTkFrame(master=app)
	frame.pack(pady=20,padx=20,fill='both',expand=True)
    
	vcmd = (app.register(validate_input), '%P')
	user_iqamaNumLabel = ctk.CTkLabel(master=frame, text="Iqama Number")
	user_iqamaNumLabel.pack()
    
	user_iqamaNum = ctk.CTkEntry(master=frame, validate="key", validatecommand=vcmd)
	user_iqamaNum.pack(pady=15,padx=20)

	user_PassLabel = ctk.CTkLabel(master=frame, text="Password")
	user_PassLabel.pack()
	user_pass= ctk.CTkEntry(master=frame,show="*")
	user_pass.pack(pady=12,padx=10)

	button = ctk.CTkButton(master=frame,text='Login', cursor="hand2",command=lambda: login(user_iqamaNum,user_pass,app))
	button.pack(pady=12,padx=10)
    
	signup_label = ctk.CTkLabel(master=frame,text="Don't have an account? Sign up!", cursor="hand2")
	signup_label.bind("<Button-1>", lambda event:(app.destroy(), signUp_Page()))
	signup_label.pack(pady=12,padx=10)

	app.mainloop()
        
#-------------------Login Portion Ended------------------------
#-----------------------------///////--------------------------
#-------------------Application Portion Started----------------

# This function is used to handle application submission.
def submit_application(iqama_number, first_name, last_name, date_of_birth, contact_number, companions, package_company, status):
    # connect to database
    conn = sqlite3.connect('Hajj_Portal.db')
    c = conn.cursor()

    c.execute('SELECT * FROM pilgrims WHERE iqama_number = ?', (iqama_number,))
    result = c.fetchone()
    if result is not None:
        # Already have an application
        tkmb.showinfo(title="Failed",message=first_name+" "+last_name+"\nYour application already exists!!!")
    else:

        # insert new application record into database
        c.execute("INSERT INTO pilgrims (iqama_number, first_name, last_name, date_of_birth, contact_number, companions, package_company, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (iqama_number, first_name, last_name, date_of_birth, contact_number, companions, package_company, status))

        # commit changes and close the database connection
        conn.commit()
        conn.close()

        # show success message
        tkmb.showinfo(title="Success",message=first_name+" "+last_name+"\nYour application has been submitted!!!")

#---------------///////---------------

# This function provides the funtionality of Stored procedure.
def update_Procedures(iqama_number, first_name, last_name, date_of_birth, contact_number, companions, package_company):
     # connect to database
    conn = sqlite3.connect('Hajj_Portal.db')
    c = conn.cursor()

    c.execute('''UPDATE pilgrims SET
                        first_name = ?,
                        last_name = ?,
                        date_of_birth = ?,
                        contact_number = ?,
                        companions = ?,
                        package_company = ?
                    WHERE iqama_number = ?;
                ''', (first_name, last_name, date_of_birth, contact_number, companions, package_company, iqama_number))
    
    # commit changes to the database
    conn.commit()
    conn.close()

#---------------///////---------------

# This function is used to handle application update.
def update_application(iqama_number, first_name, last_name, date_of_birth, contact_number, companions, package_company):
    # call the stored procedure to update a record
    update_Procedures(iqama_number, first_name, last_name, date_of_birth, contact_number, companions, package_company)
    
    # show success message
    tkmb.showinfo(title="Success",message=first_name+" "+last_name+"\nYour record has been updated!!!")

# create an entry for the contact number that only allows numbers
def validate_input(new_value):
    if new_value.isdigit():
        return True
    elif new_value == "":
        return True
    else:
        return False

#---------------///////---------------

# regular expression for Saudi Arabia mobile number
sa_mobile_regex = r"^(?:\+?966|\+966|0)?5[0-9]{8}$"

#---------------///////---------------

def validate_contact_number(contact_number):
    """
    Validates the contact number using the Saudi Arabia mobile number regex.
    Returns True if the contact number is valid, False otherwise.
    """
    return bool(re.match(sa_mobile_regex, contact_number))

def on_contact_number_change(new_value):
    """
    Callback function to validate the contact number as the user types.
    """
    if validate_contact_number(new_value) or new_value == "":
        return True
    else:
        return False

#---------------///////---------------

# This function is used to display application form.
def application_Form():
    master = ctk.CTk()
    # create a new window for the application
    application_window = tk.Toplevel(master)
    application_window.geometry("400x450")
    application_window.title("Hajj Application")
    
    vcmd = (application_window.register(validate_input), '%P')

    # create a label for the application form
    application_label = tk.Label(application_window, text="Hajj Application Form", font=("Arial", 16,"bold"))
    application_label.grid(row=0, column=1, pady=10)

    # create a label for the iqama number
    iqama_label = tk.Label(application_window, text="Iqama Number:")
    iqama_label.grid(row=1, column=0, columnspan=1, pady=10)

    # create a text box for the iqama number
    iqama_text = tk.Entry(application_window, validate="key", validatecommand=vcmd)
    iqama_text.grid(row=1, column=1)

    # create a label for the first name
    first_name_label = tk.Label(application_window, text="First Name:")
    first_name_label.grid(row=2, column=0, pady=10)

    # create a text box for the first name
    first_name_text = tk.Entry(application_window)
    first_name_text.grid(row=2, column=1)

    # create a label for the last name
    last_name_label = tk.Label(application_window, text="Last Name:")
    last_name_label.grid(row=3, column=0, pady=10)

    # create a text box for the last name
    last_name_text = tk.Entry(application_window)
    last_name_text.grid(row=3, column=1)

    # create a label for the date of birth
    dob_label = tk.Label(application_window, text="DOB(dd/mm/yyyy):")
    dob_label.grid(row=4, column=0, pady=10)
    # create a datepicker widget
    datepicker = DateEntry(application_window, date_pattern='dd/mm/yyyy')
    datepicker.grid(row=4, column=1)

    # create a label for the contact number
    contact_label = tk.Label(application_window, text="Contact Number:")
    contact_label.grid(row=5, column=0, pady=10)

    # create a text box for the contact number
    vcmd_ContantNum = (application_window.register(on_contact_number_change), '%P')
    contact_text = tk.Entry(application_window, validate="key", validatecommand=vcmd_ContantNum)
    contact_text.grid(row=5, column=1)

    # create a label for the number of companions
    companions_label = tk.Label(application_window, text="No. of Companions:")
    companions_label.grid(row=6, column=0, pady=10)

    # create a spinbox for the number of companions
    companions_spinbox = tk.Spinbox(application_window, from_=0, to=10, validate="key", validatecommand=vcmd)
    companions_spinbox.grid(row=6, column=1)

    # create a label for the package company
    package_company_label = tk.Label(application_window, text="Package Company:")
    package_company_label.grid(row=7, column=0, pady=10)

    # create a drop-down menu for the package company
    package_company_menu = ttk.Combobox(application_window, values=["ABC Company", "XYZ Company", "123 Company"])
    package_company_menu.grid(row=7, column=1)
    
    # create a frame to hold the buttons
    button_frame = tk.Frame(application_window)
    button_frame.grid(row=9, column=0, columnspan=2)

    # create a button to submit the application
    submit_button = tk.Button(button_frame, text="Submit", cursor="hand2", command=lambda: submit_application(iqama_text.get()
                    , first_name_text.get(), last_name_text.get(), datepicker.get(), contact_text.get()
                    , companions_spinbox.get(), package_company_menu.get(), "Pending") if all([iqama_text.get()
                    , first_name_text.get(), last_name_text.get(), datepicker.get(), contact_text.get(), companions_spinbox.get()
                    , package_company_menu.get()]) else None)
    submit_button.pack(side=tk.LEFT, padx=10)

    # create a button to update the records
    update_button = tk.Button(button_frame, text="Update", cursor="hand2", command=lambda: update_application(iqama_text.get()
                    , first_name_text.get(), last_name_text.get(),datepicker.get(),contact_text.get()
                    ,companions_spinbox.get(),package_company_menu.get()) if all([iqama_text.get()
                    , first_name_text.get(), last_name_text.get(), datepicker.get(), contact_text.get()
                    , companions_spinbox.get(), package_company_menu.get()]) else None)
    update_button.pack(side=tk.LEFT, padx=10)

    # center the button frame
    button_frame.place(relx=0.5, rely=0.87, anchor=tk.CENTER)

    application_window.mainloop()

#-----------------------------///////--------------------------
#-------------------Application Portion Ended----------------

def retrieve_records(treeview):
    conn = sqlite3.connect('Hajj_Portal.db')
    c = conn.cursor()
    c.execute('SELECT * FROM pilgrims')
    records = c.fetchall()
    for i, record in enumerate(records):
        treeview.insert('', 'end', values=record)
    conn.close()

def update_status(treeview,iqama_num, status, comment):
    conn = sqlite3.connect('Hajj_Portal.db')
    c = conn.cursor()
    c.execute('UPDATE pilgrims SET status=?, comment=? WHERE iqama_number=?', (status, comment, iqama_num))
    conn.commit()
    # clear existing rows from grid
    for row in treeview.get_children():
        treeview.delete(row)
        
    # repopulate grid with latest records from database
    c.execute("SELECT * FROM pilgrims")
    rows = c.fetchall()
    for row in rows:
        treeview.insert("", "end", values=row)
    
    conn.commit()
    conn.close()


def admin_Dashboard():
    root = tk.Tk()
    root.geometry("1200x350")
    root.title("Admin Dashboard")

    # Create Treeview widget
    treeview = ttk.Treeview(root, columns=('No.', 'Iqama Number', 'First Name', 'Last Name', 'DOB', 'Contact Number', 'Companions', 'Package Company', 'Status', 'Comment'), show="headings")
    treeview.pack()
    treeview.heading('No.', text='No.',anchor="w")
    treeview.column("No.", width=30, anchor="center")

    treeview.heading('Iqama Number', text='IQAMA Number')
    treeview.column("Iqama Number", width=110, anchor="center")

    treeview.heading('First Name', text='First Name')
    treeview.column("First Name", width=100, anchor="center")

    treeview.heading('Last Name', text='Last Name')
    treeview.column("Last Name", width=100, anchor="center")

    treeview.heading('DOB', text='Date of Birth')
    treeview.column("DOB", width=100, anchor="center")

    treeview.heading('Contact Number', text='Contact Number')
    treeview.column("Contact Number", width=130, anchor="center")

    treeview.heading('Companions', text='Companions')
    treeview.column("Companions", width=100, anchor="center")
    
    treeview.heading('Package Company', text='Package Company')
    treeview.column("Package Company", width=150, anchor="center")

    treeview.heading('Status', text='Status')
    treeview.column("Status", width=100, anchor="center")

    treeview.heading('Comment', text='Comment')
    treeview.column("Comment", width=200, anchor="center")

    # Retrieve records from the database and populate the treeview
    retrieve_records(treeview)

    # Add labels, entry boxes, dropdown menu, and buttons
    label_iqama_num = ttk.Label(root, text='Iqama Number',padding=15)
    entry_iqama_num = ttk.Entry(root)
    label_status = ttk.Label(root, text='Status')
    status_var = tk.StringVar(root)
    dropdown_status = ttk.Combobox(root, textvariable=status_var, values=['Approved', 'Rejected'])
    label_comment = ttk.Label(root, text='Comment')
    entry_comment = ttk.Entry(root)
    button_update = ttk.Button(root, text='Update Status', command=lambda: update_status(treeview,entry_iqama_num.get(),dropdown_status.get(),entry_comment.get()))

    # Pack labels, entry boxes, dropdown menu, and buttons
    label_iqama_num.pack()
    entry_iqama_num.pack()
    label_status.pack()
    dropdown_status.pack()
    label_comment.pack()
    entry_comment.pack()
    button_update.pack()

    # set height and width
    treeview.config(height=6)
    root.mainloop()

#-------------------------------------------
#--------------Main Function----------------
#-------------------------------------------
if __name__ == "__main__":
	login_Page()