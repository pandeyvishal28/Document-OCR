import tkinter as tk
import ttkbootstrap as ttk
from tkinter import messagebox
from tkinter import filedialog
import cv2
import OCR_Engine
import db_connection as db





pan_window = ttk.Window()
pan_window.title("PAN Card Reader")
pan_window.geometry("1400x720")
pan_window.resizable(False, False)

pan_ocr_label = ttk.Label(pan_window, text="PAN OCR", font=("Lucida Calligraphy", 30, "bold", 'underline'))
pan_ocr_label.pack(pady=20)

def select_image():
    global image_path
    image_path = filedialog.askopenfilename( title="Select Image", filetypes=(("jpeg files", "*.jpg"), ("png files", "*.png")))
    # messagebox.showinfo("Image Selected", "Image Selected Successfully")

def image_preprocessing(image):
    global img
    # reading images
    img = cv2.imread(image)

    # process front image
    img = cv2.resize(img, (600, 400), interpolation=cv2.INTER_CUBIC)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    var = cv2.Laplacian(img, cv2.CV_64F).var()

    if var < 50:
        messagebox.showerror("Error", "Image is Too Blurry")
        #exit(1)

def extract():
    global data
    global image_path
    global img

    if image_path == "":
        messagebox.showerror("Error", "Please Select Image")
    else:
        image_preprocessing(image_path)

        output = OCR_Engine.extract_pan(img)
        data = list(output.values())

        # id_type_textarea.delete("1.0", tk.END)
        
        pan_textarea.delete("1.0", tk.END)

        # id_type_textarea.insert(tk.END, output['ID Type'])
    
        pan_textarea.insert(tk.END, output['PAN'])

data = []

def save_to_database():
    global data
    # insert into database
    with db.DBConnection('pan.sqlite3') as conn:
        insert_query = f"INSERT INTO pan_data VALUES ('{data[3]}')"
        create_table_query = "CREATE TABLE IF NOT EXISTS pan_data (PAN_Number int primary key)"
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

# input frame
input_frame = ttk.Frame(pan_window)
input_frame.pack(side=tk.LEFT, padx=150)

# output frame
output_frame = ttk.Frame(pan_window)
output_frame.pack(side=tk.LEFT, padx=50, ipadx=150)

# buttons
img = ttk.Button(input_frame, text="Select Image", command=select_image)
img.pack(pady=50, padx=60)

extract = ttk.Button(input_frame, text="Extract Image Data", command=extract)
extract.pack(pady=50, padx=60)

# save to database
save_to_db = ttk.Button(input_frame, text="Save to Database", command=save_to_database)
save_to_db.pack(pady=50, padx=60)

# # name label
# name_label = ttk.Label(output_frame, text="Name:", font=("times new roman", 20, 'bold'))
# name_label.grid(row=2, column=2, pady=10, padx=10)

# # name textarea
# name_textarea = tk.Text(output_frame, height=1, width=30, font=(20))
# name_textarea.grid(row=2, column=3, pady=10, padx=10)

# # DOB label
# dob_label = ttk.Label(output_frame, text="DOB:", font=("times new roman", 20, 'bold'))
# dob_label.grid(row=3, column=2, pady=10, padx=10)

# # DOB textarea
# dob_textarea = tk.Text(output_frame, height=1, width=30, font=(20))
# dob_textarea.grid(row=3, column=3, pady=10, padx=10)

# PAN label
pan_label = ttk.Label(output_frame, text="PAN:", font=("times new roman", 20, 'bold'))
pan_label.grid(row=4, column=2, pady=10, padx=10)

# PAN textarea
pan_textarea = tk.Text(output_frame, height=1, width=30, font=(20))
pan_textarea.grid(row=4, column=3, pady=10, padx=10)



pan_window.mainloop()