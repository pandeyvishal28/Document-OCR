import tkinter as tk
import ttkbootstrap as ttk
from tkinter import messagebox
from tkinter import filedialog
import cv2
import OCR_Engine
import db_connection as db


window = ttk.Window(themename="darkly")
window.title("Aadhaar Card Reader")
window.geometry("1400x720")
window.resizable(False, False)



# add icon
icon = tk.PhotoImage(file='Images\AOCR.png')
window.iconphoto(False, icon)


front_image_path = ""
back_image_path = ""

def select_front_image():
    global front_image_path
    front_image_path = filedialog.askopenfilename( title="Select Front Image", filetypes=(("jpeg files", "*.jpg"), ("png files", "*.png")))
    # messagebox.showinfo("Front Image Selected", "Front Image Selected Successfully")

def select_back_image():
    global back_image_path
    back_image_path = filedialog.askopenfilename( title="Select Back Image", filetypes=(("jpeg files", "*.jpg"), ("png files", "*.png")))
    # messagebox.showinfo("Back Image Selected", "Back Image Selected Successfully")

def image_preprocessing(front, back):

    global front_image, back_image

    # reading images
    front_image = cv2.imread(front)
    back_image = cv2.imread(back)

    # process front image
    front_image = cv2.resize(front_image, (600, 400), interpolation=cv2.INTER_CUBIC)
    front_image = cv2.cvtColor(front_image, cv2.COLOR_BGR2GRAY)
    var_f = cv2.Laplacian(front_image, cv2.CV_64F).var()

    if var_f < 50:
        messagebox.showerror("Error", "Front Image is Too Blurry")
        #exit(1)

    # process back image
    back_image = cv2.resize(back_image, (600, 400), interpolation=cv2.INTER_CUBIC)
    back_image = cv2.cvtColor(back_image, cv2.COLOR_BGR2GRAY)
    var_b = cv2.Laplacian(back_image, cv2.CV_64F).var()

    if var_b < 50:
        messagebox.showerror("Error", "Back Image is Too Blurry")
        #exit(1)




def extract():
    global data
    global  front_image_path, back_image_path
    global front_image , back_image

    if front_image_path == "" or back_image_path == "":
        messagebox.showerror("Error", "Please Select Both Images")
    else:


        image_preprocessing(front_image_path, back_image_path)

        output = OCR_Engine.extract_aadhaar(front_image, back_image)
        
        data = list(output.values())

        
            

        # id_type_textarea.delete("1.0", tk.END)
        name_textarea.delete("1.0", tk.END)
        dob_textarea.delete("1.0", tk.END)
        gender_textarea.delete("1.0", tk.END)
        aadhaar_number_textarea.delete("1.0", tk.END)
        pin_code_textarea.delete("1.0", tk.END)
        address_textarea.delete("1.0", tk.END)


        # id_type_textarea.insert(tk.END, output['ID Type'])
        name_textarea.insert(tk.END, output['Name'])
        dob_textarea.insert(tk.END, output['Date of Birth'])
        gender_textarea.insert(tk.END, output['Sex'])
        aadhaar_number_textarea.insert(tk.END, output['Adhaar Number'])
        pin_code_textarea.insert(tk.END, output['Pin Code'])
        address_textarea.insert(tk.END, output['Address'])

data = []        

def save_to_database():
    global data
    # insert into database
    with db.DBConnection('aadhaar.sqlite3') as conn:
        insert_query = f"INSERT INTO aadhaar_data VALUES ('{data[0]}', '{data[1]}', '{data[2]}', '{data[3]}', '{data[4]}', '{data[5]}')"
        create_table_query = "CREATE TABLE IF NOT EXISTS aadhaar_data ( Name varchar(30), DOB varchar(10) ,Aadhaar_Number int primary key,Gender varchar(10) ,Address varchar(100) ,  Pin_Code int)"
        cursor = conn.cursor()
        # create table
        cursor.execute(create_table_query)
        try:
            cursor.execute(insert_query)
            conn.commit()
            messagebox.showinfo("Success", "Data Saved Successfully")
        except:
            messagebox.showerror("Error", "Data Already Exists")
        
        conn.commit()
        cursor.close()
        conn.close()



# Adhaar OCR Label
aadhaar_ocr_label = ttk.Label(window, text="Aadhaar OCR", font=("Lucida Calligraphy", 30, "bold", 'underline'))
aadhaar_ocr_label.pack(pady=20)



# input frame
input_frame = ttk.Frame(window)
input_frame.pack(side = tk.LEFT, padx=150)

# output frame
output_frame = ttk.Frame(window)
output_frame.pack(side=tk.LEFT, padx=50, ipadx=150)


# buttons
f_img = ttk.Button(input_frame, text="Select Front Image", command=select_front_image)
f_img.pack(pady=50, padx=60)

b_img = ttk.Button(input_frame, text="Select Back Image", command=select_back_image)
b_img.pack(pady=50, padx=60)

extract = ttk.Button(input_frame, text="Extract Image Data", command=extract)
extract.pack(pady=50, padx=60)

# save to database
save_to_db = ttk.Button(input_frame, text="Save to Database", command=save_to_database)
save_to_db.pack(pady=50, padx=60)


# name label
name_label = ttk.Label(output_frame, text="Name:", font = ("times new roman",20, 'bold'))
name_label.grid(row=2, column=2, pady=10, padx=10)

# name textarea
name_textarea = tk.Text(output_frame, height=1, width=30, font=(20))
name_textarea.grid(row=2, column=3, pady=10, padx=10)

# DOB label
dob_label = ttk.Label(output_frame, text="DOB:", font=("times new roman",20, 'bold'))
dob_label.grid(row=3, column=2, pady=10, padx=10)

# DOB textarea
dob_textarea = tk.Text(output_frame, height=1, width=30, font=(20))
dob_textarea.grid(row=3, column=3, pady=10, padx=10)

# Gender label
gender_label = ttk.Label(output_frame, text="Gender:", font=("times new roman",20, 'bold'))
gender_label.grid(row=4, column=2, pady=10, padx=10)

# gender textarea
gender_textarea = tk.Text(output_frame, height=1, width=30, font=(20))
gender_textarea.grid(row=4, column=3, pady=10, padx=10)

# Aadhaar Number label
aadhaar_number_label = ttk.Label(output_frame, text="Aadhaar Number:", font=("times new roman",20, 'bold'))
aadhaar_number_label.grid(row=5, column=2, pady=10, padx=10)

# Aadhaar Number textarea
aadhaar_number_textarea = tk.Text(output_frame, height=1, width=30, font=(20))
aadhaar_number_textarea.grid(row=5, column=3, pady=10, padx=10)

# Address label
address_label = ttk.Label(output_frame, text="Address:", font=("times new roman",20, 'bold'))
address_label.grid(row=7, column=2, pady=10, padx=10)

# Address textarea
address_textarea = tk.Text(output_frame, height=5, width=30, font=(20))
address_textarea.grid(row=7, column=3, pady=10, padx=10)

# Pin Code label
pin_code_label = ttk.Label(output_frame, text="Pin Code:", font=("times new roman",20, 'bold'))
pin_code_label.grid(row=6, column=2, pady=10, padx=10)

# Pin Code textarea
pin_code_textarea = tk.Text(output_frame, height=1, width=30, font=(20))
pin_code_textarea.grid(row=6, column=3, pady=10, padx=10)



window.mainloop()