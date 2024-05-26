import sqlite3

class DBConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()


def save_to_database(data):
    
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