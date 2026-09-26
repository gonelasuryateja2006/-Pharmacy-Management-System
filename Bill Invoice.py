import os
import sys
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from PIL import Image, ImageTk
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
import subprocess
import webbrowser
from datetime import datetime

class PharmacyManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Bill Invoice")
        self.root.geometry("1920x1080")

        self.cmpName_var=StringVar()
        self.Address_var=StringVar()
        self.City_var=StringVar()
        self.State_var=StringVar()
        self.Country_var=StringVar()
        self.PinCode_var=StringVar()
        self.Contact_var=StringVar()
        self.email_var=StringVar()


        self.bg = ImageTk.PhotoImage(file=r"Images\bg2.jpg")
        lbl_bg = Label(self.root, image=self.bg)
        lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)

        self.txt = "Blaze Pharmacy Management System!.....\nStock Statement Generator.........."
        self.count = 0
        self.text = ' '
        self.label = Label(self.root, text=self.txt, font=("times new roman", 30, "bold"), fg="red", bg="black")
        self.label.pack(pady=50)
        self.slider()

        self.conn = mysql.connector.connect(host="localhost", username="root", password=os.environ["PHARMACY_DB_PASSWORD"], database="pharmacy_demo")
        self.my_cursor = self.conn.cursor()

        FrameDetails = Frame(self.root, bd=15, relief=RIDGE, bg="lightgreen")
        FrameDetails.place(x=0, y=150, width=1535, height=245)

        Table_frame = Frame(self.root, bd=15, relief=RIDGE)
        Table_frame.place(x=0, y=150, width=1535, height=245)
        

        scroll_x = ttk.Scrollbar(Table_frame, orient=HORIZONTAL)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y = ttk.Scrollbar(Table_frame, orient=VERTICAL)
        scroll_y.pack(side=RIGHT, fill=Y)

        self.medicine_table = ttk.Treeview(Table_frame, column=("Reference No", "Company Name", "Type of Medicine", "Issue Date", "Expiry Date", "Side Effect", "Precautions and Warnings", "Dosage", "Price", "Product Quantity", "Uses", "Name", "Lot.No"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.config(command=self.medicine_table.xview)
        scroll_y.config(command=self.medicine_table.yview)

        self.medicine_table.heading("Reference No", text="Reference Number")
        self.medicine_table.heading("Company Name", text="Company Name")
        self.medicine_table.heading("Type of Medicine", text="Type of Medicine")
        self.medicine_table.heading("Issue Date", text="Issue Date")
        self.medicine_table.heading("Expiry Date", text="Expiry Date")
        self.medicine_table.heading("Side Effect", text="Side Effect")
        self.medicine_table.heading("Precautions and Warnings", text="Precautions and Warnings")
        self.medicine_table.heading("Dosage", text="Dosage")
        self.medicine_table.heading("Price", text="Price")
        self.medicine_table.heading("Product Quantity", text="Product Quantity")
        self.medicine_table.heading("Uses", text="Uses")
        self.medicine_table.heading("Name", text="Medicine Name")
        self.medicine_table.heading("Lot.No", text="Lot.No")
        self.medicine_table.pack(fill=BOTH, expand=1)

        self.medicine_table.column("Reference No", width=100)
        self.medicine_table.column("Company Name", width=100)
        self.medicine_table.column("Type of Medicine", width=100)
        self.medicine_table.column("Issue Date", width=100)
        self.medicine_table.column("Expiry Date", width=100)
        self.medicine_table.column("Side Effect", width=100)
        self.medicine_table.column("Precautions and Warnings", width=100)
        self.medicine_table.column("Dosage", width=100)
        self.medicine_table.column("Price", width=100)
        self.medicine_table.column("Product Quantity", width=100)
        self.medicine_table.column("Uses", width=100)
        self.medicine_table.column("Name", width=100)
        self.medicine_table.column("Lot.No", width=100)
        self.fetch_data()

        self.medicine_table["show"] = "headings"
        self.medicine_table.pack(fill=BOTH, expand=1)

        address_frame = Frame(self.root, bd=15, relief=RIDGE,bg="orangered")
        address_frame.place(x=1300, y=395, width=235, height=297)
        

        scroll_x = ttk.Scrollbar(address_frame, orient=HORIZONTAL)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y = ttk.Scrollbar(address_frame, orient=VERTICAL)
        scroll_y.pack(side=RIGHT, fill=Y)


        self.address_table = ttk.Treeview(address_frame, column=("CmpName","Address","City","State","Country","Pincode","Contact","E-Mail"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.config(command=self.address_table.xview)
        scroll_y.config(command=self.address_table.yview)

        self.address_table.column("CmpName",width=100)
        self.address_table.column("Address",width=100)
        self.address_table.column("City",width=100)
        self.address_table.column("State",width=100)
        self.address_table.column("Country",width=100)
        self.address_table.column("Pincode",width=100)
        self.address_table.column("Contact",width=100)
        self.address_table.column("E-Mail",width=100)
        self.fetch_address()
        self.address_table.bind("<ButtonRelease-1>",self.get_cursor)

        self.address_table["show"]="headings"
        self.address_table.pack(fill=BOTH,expand=1)

        self.address_table.heading("CmpName", text="Company Name")
        self.address_table.heading("Address", text="Address")
        self.address_table.heading("City", text="City")
        self.address_table.heading("State", text="State")
        self.address_table.heading("Country", text="Country")
        self.address_table.heading("Pincode", text="Pincode")
        self.address_table.heading("Contact", text="Contact")
        self.address_table.heading("E-Mail", text="E-Mail")

        ButtonFrame = Frame(self.root, bd=10, relief=RIDGE, bg="orangered", padx=20)
        ButtonFrame.place(x=50, y=700, width=1450, height=75)

        self.search_var = StringVar()
        search_combo = ttk.Combobox(ButtonFrame, textvariable=self.search_var, width=10, font=("arial", 29, "bold"), state="readonly")
        search_combo["values"] = ["Ref_No", "MedName", "LotNo"]
        search_combo.grid(row=0, column=6)
        search_combo.current(0)
        search_combo.place(x=-10, y=0)

        lblSearch = Label(ButtonFrame, font=("arial", 17, "bold"), text="Search By", padx=7, pady=10, bg="black", fg="gold")
        lblSearch.grid(row=0, column=5, sticky=W)
        lblSearch.place(x=250, y=0)

        self.searchTxt_var = StringVar()
        txtSearch = Entry(ButtonFrame, textvariable=self.searchTxt_var, bd=3, relief=RIDGE, width=15, font=("times new roman", 29, "bold"))
        txtSearch.grid(column=9, row=0)
        txtSearch.place(x=400, y=0)

        searchBtn = Button(ButtonFrame, text="Search", command=self.search_data, font=("arial", 15, "bold"), padx=7, pady=6, width=12, bg="blue", fg="white")
        searchBtn.grid(row=0, column=8)
        searchBtn.place(x=725, y=0)

        btnPDFMed = Button(ButtonFrame, text="PDF", font=("arial", 15, "bold"), bg="green", fg="white", padx=7, pady=6, command=lambda:[self.generate_pdf(), self.fun2()])
        btnPDFMed.grid(row=0, column=4)
        btnPDFMed.place(x=900, y=0)

        btnRefreshMed = Button(ButtonFrame, text="Refresh", font=("arial", 15, "bold"), command=self.refresh_page, bg="yellow", fg="white", padx=7, pady=6)
        btnRefreshMed.grid(row=0, column=4)
        btnRefreshMed.place(x=975, y=0)

        btnMainPage = Button(ButtonFrame, text="Main Page", font=("arial", 15, "bold"), command=self.fun1, bg="red", fg="white", padx=25, pady=6)
        btnMainPage.grid(row=0, column=4)
        btnMainPage.place(x=1085, y=0)

        btnShowall = Button(ButtonFrame, text="Show All", font=("arial", 15, "bold"), command=self.fetch_data, bg="Brown", fg="white", padx=25, pady=6)
        btnShowall.grid(row=0, column=4)
        btnShowall.place(x=1255, y=0)

        DataFrame=Frame(self.root,bd=15,relief=RIDGE,padx=20,bg="orangered")
        DataFrame.place(x=0,y=395,width=1300,height=300)

        DataFrameLeft=LabelFrame(DataFrame,bd=10,relief=RIDGE,bg="orangered",padx=20,text="Shipping Address",fg="yellow",font=("times new roman",25,"bold"))
        DataFrameLeft.place(x=-10,y=5,width=1250,height=260)


        lblCmpName=Label(DataFrameLeft,font=("times new roman",18,"bold"),text="Company Name:",bg="orangered",fg="yellow",padx=2,pady=6)
        lblCmpName.grid(row=1,column=1,sticky=W)
        lblCmpName.place(x=-10,y=0)
        txtCmpName=Entry(DataFrameLeft,textvariable=self.cmpName_var,font=("arial",13,"bold"),bg="white",bd=2,relief=RIDGE,width=29)
        txtCmpName.grid(row=1,column=1)
        txtCmpName.place(x=185,y=10)

        lblAddress=Label(DataFrameLeft,font=("times new roman",18,"bold"),text="Address:",bg="orangered",fg="yellow",padx=2,pady=6)
        lblAddress.grid(row=2,column=2,sticky=W)
        lblAddress.place(x=-10,y=40)
        txtAddress=Entry(DataFrameLeft,textvariable=self.Address_var,font=("arial",18,"bold"),bg="white",bd=2,relief=RIDGE,width=20)
        txtAddress.grid(row=2,column=0,sticky=W)
        txtAddress.place(x=185,y=50)

        lblCity=Label(DataFrameLeft,font=("times new roman",18,"bold"),text="City:",bg="orangered",fg="yellow",padx=2,pady=6)
        lblCity.grid(row=2,column=2,sticky=W)
        lblCity.place(x=-10,y=85)
        txtCity=Entry(DataFrameLeft,textvariable=self.City_var,font=("arial",13,"bold"),bg="white",bd=2,relief=RIDGE,width=29)
        txtCity.grid(row=2,column=0,sticky=W)
        txtCity.place(x=185,y=100)

        lblState=Label(DataFrameLeft,font=("times new roman",18,"bold"),text="State:",bg="orangered",fg="yellow",padx=2,pady=6)
        lblState.grid(row=2,column=2,sticky=W)
        lblState.place(x=-10,y=130)
        txtState=Entry(DataFrameLeft,textvariable=self.State_var,font=("arial",13,"bold"),bg="white",bd=2,relief=RIDGE,width=29)
        txtState.grid(row=2,column=0,sticky=W)
        txtState.place(x=185,y=140)

        lblCountry=Label(DataFrameLeft,font=("times new roman",18,"bold"),text="Country:",bg="orangered",fg="yellow",padx=2,pady=6)
        lblCountry.grid(row=2,column=2,sticky=W)
        lblCountry.place(x=475,y=0)
        txtCountry=Entry(DataFrameLeft,textvariable=self.Country_var,font=("arial",13,"bold"),bg="white",bd=2,relief=RIDGE,width=29)
        txtCountry.grid(row=2,column=0,sticky=W)
        txtCountry.place(x=600,y=10)

        lblPinCode=Label(DataFrameLeft,font=("times new roman",18,"bold"),text="Pincode:",bg="orangered",fg="yellow",padx=2,pady=6)
        lblPinCode.grid(row=2,column=2,sticky=W)
        lblPinCode.place(x=475,y=40)
        txtPinCode=Entry(DataFrameLeft,textvariable=self.PinCode_var,font=("arial",13,"bold"),bg="white",bd=2,relief=RIDGE,width=29)
        txtPinCode.grid(row=2,column=0,sticky=W)
        txtPinCode.place(x=600,y=50)

        lblContact=Label(DataFrameLeft,font=("times new roman",18,"bold"),text="Contact:",bg="orangered",fg="yellow",padx=2,pady=6)
        lblContact.grid(row=2,column=2,sticky=W)
        lblContact.place(x=475,y=85)
        txtContact=Entry(DataFrameLeft,textvariable=self.Contact_var,font=("arial",13,"bold"),bg="white",bd=2,relief=RIDGE,width=29)
        txtContact.grid(row=2,column=0,sticky=W)
        txtContact.place(x=600,y=95)

        lblEmail=Label(DataFrameLeft,font=("times new roman",18,"bold"),text="E-Mail:",bg="orangered",fg="yellow",padx=2,pady=6)
        lblEmail.grid(row=2,column=2,sticky=W)
        lblEmail.place(x=475,y=130)
        txtEmail=Entry(DataFrameLeft,textvariable=self.email_var,font=("arial",13,"bold"),bg="white",bd=2,relief=RIDGE,width=29)
        txtEmail.grid(row=2,column=0,sticky=W)
        txtEmail.place(x=600,y=140)

        down_frame=Frame(DataFrameLeft,bd=4,relief=RIDGE,bg="darkgreen")
        down_frame.place(x=1000,y=50,width=135,height=145)

        btnAdd=Button(down_frame,text="ADD",command=self.AddMed,font=("arial",13,"bold"),width=12,bg="blue",fg="white")
        btnAdd.grid(row=0,column=0)
        btnAdd.place(x=0,y=0)

        btnUpdate=Button(down_frame,text="UPDATE",command=self.UpdateMed,font=("arial",13,"bold"),width=12,bg="green",fg="white")
        btnUpdate.grid(row=1,column=0)
        btnUpdate.place(x=0,y=35)

        btnClear=Button(down_frame,text="CLEAR",command=self.ClearFields,font=("arial",13,"bold"),width=12,bg="orange",fg="white")
        btnClear.grid(row=1,column=0)
        btnClear.place(x=0,y=70)

        btnDelete=Button(down_frame,text="DELETE",command=self.delete,font=("arial",13,"bold"),width=12,bg="red",fg="white")
        btnDelete.grid(row=1,column=0)
        btnDelete.place(x=0,y=105)

        self.date_time_label = Label(DataFrameLeft, font=("times new roman", 20, "bold"), bg="black", fg="yellow")
        self.date_time_label.pack(side=TOP, anchor=E, padx=0, pady=0)
        self.update_time()

    def update_time(self):
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        self.date_time_label.config(text=current_time)
        self.root.after(1000, self.update_time)
    

    def slider(self):
        if self.count >= len(self.txt):
            self.count = -1
            self.text = ''
            self.label.configure(text=self.text)
        else:
            self.text = self.text + self.txt[self.count]
            self.label.configure(text=self.text)
        self.count += 1
        self.label.after(100, self.slider)

    def refresh_page(self):
        self.root.destroy()
        new_root = Tk()
        new_obj = PharmacyManagementSystem(new_root)
        new_root.mainloop()

    def fetch_data(self):
        self.my_cursor.execute("SELECT * FROM pharmacy")
        rows = self.my_cursor.fetchall()
        if len(rows) != 0:
            self.medicine_table.delete(*self.medicine_table.get_children())
            for row in rows:
                self.medicine_table.insert("", END, values=row)
            self.conn.commit()

    def fetch_address(self):
        self.my_cursor.execute("SELECT * FROM toaddress")
        rows = self.my_cursor.fetchall()
        if len(rows) != 0:
            self.address_table.delete(*self.address_table.get_children())
            for row in rows:
                self.address_table.insert("", END, values=row)
            self.conn.commit()

    def search_data(self):
        conn = mysql.connector.connect(host="localhost", username="root", password=os.environ["PHARMACY_DB_PASSWORD"], database="pharmacy_demo")
        my_cursor = conn.cursor()
        my_cursor.execute("SELECT * FROM pharmacy WHERE " + str(self.search_var.get()) + " LIKE '%" + str(self.searchTxt_var.get()) + "%'")
        rows = my_cursor.fetchall()
        if len(rows) != 0:
            self.medicine_table.delete(*self.medicine_table.get_children())
            for i in rows:
                self.medicine_table.insert("", END, values=i)
            conn.commit()
        conn.close()

    def fun1(self):
        subprocess.Popen([sys.executable, r"Pharmacy Management System Project.py"])

    def fun2(self):
        webbrowser.open_new( r"pharmacy_invoice.pdf")
        

    def generate_pdf(self):
        selected_item = self.medicine_table.selection()
        if not selected_item:
            messagebox.showerror("Selection Error", "Please select a row to generate PDF.")
            return

        item_values = self.medicine_table.item(selected_item[0], 'values')
        if not item_values:
            messagebox.showerror("Data Error", "No data found for the selected row.")
            return

        pdf_buffer = BytesIO()
        c = canvas.Canvas(pdf_buffer, pagesize=letter)
        width, height = letter

        image_path = r"Images\stamp.jpg"
        image_x = 375 
        image_y = height - 620  
        image_width = 200  
        image_height = 150  

        c.drawImage(image_path, image_x, image_y, width=image_width, height=image_height)

        company_name = self.cmpName_var.get()
        address_details = {
        "Company Name": company_name,
        "Address": self.Address_var.get(),
        "City": self.City_var.get(),
        "State": self.State_var.get(),
        "Country": self.Country_var.get(),
        "Pincode": self.PinCode_var.get(),
        "Contact": self.Contact_var.get(),
        "Email": self.email_var.get()
    }
        c.setFont("Helvetica-Bold", 13)
        y_position = height - 650
        for key, value in address_details.items():
            c.drawString(50, y_position, f"{key}: {value}")
            y_position -= 15

        title = "Blaze Pharmacy Stock Statement"
        title_font_size = 30
        c.setFont("Helvetica-Bold", title_font_size)
        title_width = c.stringWidth(title, "Helvetica-Bold", title_font_size)
        c.drawString((width - title_width) / 2, height - 44, title)

        From = "Shipping From,"
        From_font_size = 14
        c.setFont("Helvetica-Bold", From_font_size)
        From_width = c.stringWidth(From, "Helvetica-Bold", From_font_size)
        c.drawString((width - From_width) / 12, height - 520, From)

        From1="Blaze Pharmacy Pvt.Ltd,"
        From1_font_size = 13
        c.setFont("Helvetica-Bold", From1_font_size)
        From1_width = c.stringWidth(From1, "Helvetica-Bold", From1_font_size)
        c.drawString((width - From1_width) / 8, height - 540, From1)

        Address="No:9/5,Govindan Road,West Mamabalam,"
        Address_font_size = 13
        c.setFont("Helvetica-Bold", Address_font_size)
        Address_width = c.stringWidth(Address, "Helvetica-Bold", Address_font_size)
        c.drawString((width - Address_width) / 6.3, height - 555, Address)

        City="Chennai,Tamilnadu,INDIA - 600033"
        City_font_size = 13
        c.setFont("Helvetica-Bold", City_font_size)
        City_width = c.stringWidth(City, "Helvetica-Bold", City_font_size)
        c.drawString((width - City_width) / 7, height - 570, City)


        contact="Contact: 9876543210 / 044 9876 5432"
        contact_font_size = 13
        c.setFont("Helvetica-Bold", contact_font_size)
        contact_width = c.stringWidth(contact, "Helvetica-Bold", contact_font_size)
        c.drawString((width - contact_width) / 7, height - 585, contact)

        email="e-mail: blazepharmacy@gmail.com"
        email_font_size = 13
        c.setFont("Helvetica-Bold", email_font_size)
        email_width = c.stringWidth(email, "Helvetica-Bold", email_font_size)
        c.drawString((width - email_width) / 7, height - 600, email)

        sign="BLAZE MANAGEMENT"
        sign_font_size = 13
        c.setFont("Helvetica-Bold", sign_font_size)
        sign_width = c.stringWidth(sign, "Helvetica-Bold", sign_font_size)
        c.drawString((width - sign_width) / 1.2, height - 630, sign)

        
        From2 = "Shipping To,"
        From2_font_size = 14
        c.setFont("Helvetica-Bold", From2_font_size)
        From2_width = c.stringWidth(From2, "Helvetica-Bold", From2_font_size)
        c.drawString((width - From2_width) / 12, height - 630, From2)

        com = "*THIS IS A COMPUTER GENERATED PDF (OR) STATEMENT"
        com_font_size = 14
        c.setFont("Helvetica-Bold", com_font_size)
        com_width = c.stringWidth(com, "Helvetica-Bold", com_font_size)
        c.drawString((width - com_width) / 12, height - 775, com)

        now = datetime.now()
        current_datetime = now.strftime("%Y-%m-%d     %H:%M:%S")
        c.setFont("Helvetica", 13)
        c.drawString(70, height - 75, f"Date & Time: {current_datetime}")


        line1 = "------------------------------------------------------------"
        line1_font_size = 25
        c.setFont("Helvetica-Bold", line1_font_size)
        line1_width = c.stringWidth(line1, "Helvetica-Bold", line1_font_size)
        c.drawString((width - line1_width) / 2, height - 20, line1)

        
        line2 = "------------------------------------------------------------"
        line2_font_size = 25
        c.setFont("Helvetica-Bold", line2_font_size)
        line2_width = c.stringWidth(line2, "Helvetica-Bold", line2_font_size)
        c.drawString((width - line2_width) / 2, height - 60, line2)

        line3 = "-----------------------------------------------------------------"
        line3_font_size = 25
        c.setFont("Helvetica-Bold", line3_font_size)
        line3_width = c.stringWidth(line3, "Helvetica-Bold", line3_font_size)
        c.drawString((width - line3_width) / 2, height - 485, line3)


        heading_font_size = 15
        data_font_size = 15
        line_height = 30
        margin = 100

   
        headers = [
            "Reference No                 ", "Company Name             ", "Type of Medicine           ", "Issue Date                      ",
            "Expiry Date                    ", "Side Effect                     ", "Warnings                        ", "Dosage                           ",
            "Price                               ", "Product Quantity           ", "Uses                                ", "Medicine Name              ", "Lot.No                             "
        ]

      
        max_heading_width = max(c.stringWidth(header + ":", "Helvetica-Bold", heading_font_size) for header in headers)
        max_data_width = max(c.stringWidth(str(value), "Helvetica", data_font_size) for value in item_values)
        max_width = max_heading_width + max_data_width + 200 

        
        content_x = (width - max_width) / 2
        y_position = height - 100

        c.setFont("Helvetica-Bold", heading_font_size)
        for header, value in zip(headers, item_values):
            header_text = header + ":       "
            header_width = c.stringWidth(header_text, "Helvetica-Bold", heading_font_size)
            data_text = str(value)
            data_width = c.stringWidth(data_text, "Helvetica", data_font_size)

            header_x = content_x
            data_x = header_x + header_width + 10 

            c.drawString(header_x, y_position, header_text)
            
            c.setFont("Helvetica", data_font_size)
            c.drawString(data_x, y_position, data_text)
            
            
            c.setFont("Helvetica-Bold", heading_font_size)
            y_position -= line_height

     
        c.showPage()
        c.save()
        
      
        pdf_buffer.seek(0)
        with open("pharmacy_invoice.pdf", "wb") as f:
            f.write(pdf_buffer.getvalue())

        pdf_buffer.close()
        messagebox.showinfo("Success", "PDF has been generated and saved as 'pharmacy_invoice.pdf'.")

    def AddMed(self):
        try:
            conn = mysql.connector.connect(host="localhost", username="root", password=os.environ["PHARMACY_DB_PASSWORD"], database="pharmacy_demo")
            my_cursor = conn.cursor()
            my_cursor.execute("INSERT INTO toaddress(CmpName,Address,City,State,Country,PinCode,Contact,email) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (
                self.cmpName_var.get(),
                self.Address_var.get(),
                self.City_var.get(),
                self.State_var.get(),
                self.Country_var.get(),
                self.PinCode_var.get(),
                self.Contact_var.get(),
                self.email_var.get(),
            ))
            conn.commit()
            conn.close()
            messagebox.showinfo('Success','Address has been Added!')
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def UpdateMed(self):
        try:
            # Establish the database connection
            conn = mysql.connector.connect(
                host="localhost",
                username="root",
                password=os.environ["PHARMACY_DB_PASSWORD"],
                database="pharmacy_demo"
            )
            my_cursor = conn.cursor()
            
            
            query = """
            UPDATE toaddress
            SET CmpName=%s, Address=%s, City=%s, State=%s, Country=%s, PinCode=%s, Contact=%s, email=%s
            """
                        
            
            my_cursor.execute(query, (
                self.cmpName_var.get(),
                self.Address_var.get(),
                self.City_var.get(),
                self.State_var.get(),
                self.Country_var.get(),
                self.PinCode_var.get(),
                self.Contact_var.get(),
                self.email_var.get(),
            ))
            
   
            conn.commit()
            
         
            self.fetch_address()
            
           
            conn.close()
            
            messagebox.showinfo("Success", "Address has been updated!")
            
        except mysql.connector.Error as err:
         
            messagebox.showerror("Error", f"Database error: {err}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")


    def ClearFields(self):
        self.cmpName_var.set("")
        self.Address_var.set("")
        self.City_var.set("")
        self.State_var.set("")
        self.Country_var.set("")
        self.PinCode_var.set("")
        self.Contact_var.set("")
        self.email_var.set("")

    def get_cursor(self,event=""):
        cursor_row=self.address_table.focus()
        content=self.address_table.item(cursor_row)
        row=content["values"]
        self.cmpName_var.set(row[0])
        self.Address_var.set(row[1])
        self.City_var.set(row[2])
        self.State_var.set(row[3])
        self.Country_var.set(row[4])
        self.PinCode_var.set(row[5])
        self.Contact_var.set(row[6])
        self.email_var.set(row[7])

    def delete(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                username="root",
                password=os.environ["PHARMACY_DB_PASSWORD"],
                database="pharmacy_demo"
            )
            my_cursor = conn.cursor()

            sql = "DELETE FROM toaddress WHERE CmpName = %s"
            val = (self.cmpName_var.get(),)

            my_cursor.execute(sql, val)
            conn.commit()

            conn.close()

            messagebox.showinfo("Success", "Address Data Deleted Successfully!")
        except Exception as e:

            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            ref_number_to_delete =Ref_no


if __name__ == "__main__":
    root = Tk()
    app = PharmacyManagementSystem(root)
    root.mainloop()
