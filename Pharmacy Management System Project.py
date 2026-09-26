import os
import sys
from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk
import mysql.connector
from tkinter import messagebox
from fpdf import FPDF
import subprocess
class PharmacyManagementSystem:
    def __init__(self,root):
        #===================Main Page=======================#
        self.root=root
        self.root.title("Blaze Pharmacy Management System")
        self.root.geometry("1920x1080+0+0")

        self.addmed_var=StringVar()
        self.refMed_var=StringVar()

        self.ref_var=StringVar()
        self.cmpName_var=StringVar()
        self.typeMed_var=StringVar()
        self.medName_var=StringVar()
        self.lot_var=StringVar()
        self.issuedate_var=StringVar()
        self.expdate_var=StringVar()
        self.uses_var=StringVar()
        self.sideEffect_var=StringVar()
        self.warning_var=StringVar()
        self.dosage_var=StringVar()
        self.price_var=StringVar()
        self.product_var=StringVar()


        lbltitle=Label(self.root,text="BLAZE \nPHARMACY MANAGEMENT SYSTEM",bd=15,relief=RIDGE,bg='black',fg="gold",font=("times new roman",50,"bold"),padx=2,pady=4)
        lbltitle.pack(side=TOP,fill=X)
        
        img1=Image.open(r"Images\img2.png")
        img1=img1.resize((145,150))
        self.photoimg1=ImageTk.PhotoImage(img1)
        b1=Button(self.root,image=self.photoimg1,borderwidth=2)
        b1.place(x=12,y=15)
        
        img2=Image.open(r"Images\img1.jpg")
        img2=img2.resize((130,150))
        self.photoimg2=ImageTk.PhotoImage(img2)
        b1=Button(self.root,image=self.photoimg2,borderwidth=2)
        b1.place(x=1385,y=15)

        DataFrame=Frame(self.root,bd=15,relief=RIDGE,bg="lightgreen",padx=20)
        DataFrame.place(x=0,y=190,width=1540,height=400)

        DataFrameLeft=LabelFrame(DataFrame,bd=10,relief=RIDGE,padx=20,bg="lightgreen",text="Medicine Information",fg="darkgreen",font=("times new roman",25,"bold"))
        DataFrameLeft.place(x=-10,y=5,width=850,height=350)

        DataFrameRight=LabelFrame(DataFrame,bd=10,relief=RIDGE,bg="lightgreen",padx=20,text="Medicine Add Department",fg="darkgreen",font=("times new roman",25,"bold"))
        DataFrameRight.place(x=855,y=5,width=625,height=350)

        ButtonFrame=Frame(self.root,bd=10,relief=RIDGE,bg="lightgreen",padx=20)
        ButtonFrame.place(x=0,y=520,width=1530,height=65)

        btnAddData=Button(ButtonFrame,command=self.add_data,text="Medicine Add",font=("arial",15,"bold"),width=13,bg="darkgreen",fg="white")
        btnAddData.grid(row=0,column=0)
        btnAddData.place(x=-18,y=0)
        
        btnUpdateMed=Button(ButtonFrame,text="Update",command=self.Update,font=("arial",15,"bold"),bg="orange",fg="white")
        btnUpdateMed.grid(row=0,column=1)
        btnUpdateMed.place(x=155,y=0)

        btnDeleteMed=Button(ButtonFrame,text="Delete",command=self.delete,font=("arial",15,"bold"),padx=20,bg="red",fg="white")
        btnDeleteMed.grid(row=0,column=2)
        btnDeleteMed.place(x=250,y=0)

        btnRestMed=Button(ButtonFrame,text="Reset",command=self.reset,font=("arial",15,"bold"),bg="blue",fg="white")
        btnRestMed.grid(row=0,column=3)
        btnRestMed.place(x=375,y=0)

        btnPDFMed=Button(ButtonFrame,text="Invoice",font=("arial",15,"bold"),bg="green",fg="white",command=self.fun1)
        btnPDFMed.grid(row=0,column=4)
        btnPDFMed.place(x=450,y=0)

        lblSearch=Label(ButtonFrame,font=("arial",17,"bold"),text="Search By",padx=2,pady=5,bg="black",fg="gold")
        lblSearch.grid(row=0,column=5,sticky=W)
        lblSearch.place(x=635,y=0)



        btnRefreshMed=Button(ButtonFrame,text="Refresh",font=("arial",15,"bold"),command=self.refresh_page,bg="orangered",fg="white")
        btnRefreshMed.grid(row=0,column=4)
        btnRefreshMed.place(x=540,y=0)

        self.search_var=StringVar()
        search_combo=ttk.Combobox(ButtonFrame,textvariable=self.search_var,width=10,font=("arial",23,"bold"),state="readonly")
        search_combo["values"]=["Ref_No","MedName","LotNo"]
        search_combo.grid(row=0,column=6)
        search_combo.current(0)
        search_combo.place(x=760,y=0)

        self.searchTxt_var=StringVar()
        txtSearch=Entry(ButtonFrame,textvariable=self.searchTxt_var,bd=3,relief=RIDGE,width=15,font=("times new roman",23,"bold"))
        txtSearch.grid(column=9,row=0)
        txtSearch.place(x=955,y=0)

        searchBtn=Button(ButtonFrame,text="Search",command=self.search_data,font=("arial",15,"bold"),padx=2,pady=2,width=12,bg="orchid",fg="white")
        searchBtn.grid(row=0,column=8)
        searchBtn.place(x=1215,y=0)

        showAll=Button(ButtonFrame,text="Show All",command=self.fetch_data,font=("arial",15,"bold"),pady=2,width=8,bg="lime",fg="white")
        showAll.grid(row=0,column=8)
        showAll.place(x=1380,y=0)

        lblMedicineName=Label(DataFrameLeft,font=("arial",12,"bold"),bg="lightgreen",fg="red",text="Reference Number:",padx=2,pady=6)
        lblMedicineName.grid(row=0,column=0,sticky=W)
        lblMedicineName.place(x=-10,y=-7)

        conn=mysql.connector.connect(host="localhost",username="root",password=os.environ["PHARMACY_DB_PASSWORD"],database="pharmacy_demo")
        my_cursor=conn.cursor()
        my_cursor.execute("Select Ref from pharma")
        row=my_cursor.fetchall()
        
        ref_combo=ttk.Combobox(DataFrameLeft,textvariable=self.ref_var,width=27,font=("arial",12,"bold"),state="readonly")
        ref_combo["values"]=row
        ref_combo.grid(row=0,column=6)
        ref_combo.current(0)
        ref_combo.place(x=150,y=0)

        lblCmpName=Label(DataFrameLeft,font=("arial",12,"bold"),text="Company Name:",bg="lightgreen",fg="red",padx=2,pady=6)
        lblCmpName.grid(row=1,column=1,sticky=W)
        lblCmpName.place(x=-10,y=25)
        txtCmpName=Entry(DataFrameLeft,textvariable=self.cmpName_var,font=("arial",13,"bold"),bg="white",bd=2,relief=RIDGE,width=29)
        txtCmpName.grid(row=1,column=1)
        txtCmpName.place(x=150,y=30)

        
        lblTypeofMedicine=Label(DataFrameLeft,font=("arial",12,"bold"),text="Type Of Medicine:",fg="red",bg="lightgreen",padx=2,pady=6)
        lblTypeofMedicine.grid(row=2,column=0,sticky=W)
        lblTypeofMedicine.place(x=-10,y=57)
        comTypeofMedicine=ttk.Combobox(DataFrameLeft,textvariable=self.typeMed_var,state="readonly",font=("arial",12,"bold"),width=27)
        comTypeofMedicine['value']=("--SELECT--","Tablet","Syrup","Liquid","Capsules","Topical Medicines","Drops","Inhales","Injection","Syringes")
        comTypeofMedicine.current(0)
        comTypeofMedicine.grid(row=2,column=1)
        comTypeofMedicine.place(x=150,y=62)

        lblMedicineName=Label(DataFrameLeft,font=("arial",12,"bold"),text="Medicine Name:",fg="red",bg="lightgreen",padx=2,pady=6)
        lblMedicineName.grid(row=3,column=0,sticky=W)
        lblMedicineName.place(x=-10,y=91)
        conn=mysql.connector.connect(host="localhost",username="root",password=os.environ["PHARMACY_DB_PASSWORD"],database="pharmacy_demo")
        my_cursor=conn.cursor()
        my_cursor.execute("Select MedName from pharma")
        med=my_cursor.fetchall()
        
        comMedicineName=ttk.Combobox(DataFrameLeft,textvariable=self.medName_var,state="readonly",font=("arial",12,"bold"),width=27)
        comMedicineName['value']=med
        comMedicineName.current(0)
        comMedicineName.grid(row=3,column=1)
        comMedicineName.place(x=150,y=95)

        lblIssueDate=Label(DataFrameLeft,font=("arial",12,"bold"),text="Issue Date:",fg="red",bg="lightgreen",padx=2,pady=6)
        lblIssueDate.grid(row=5,column=0,sticky=W)
        lblIssueDate.place(x=-10,y=156)
        txtIssueDate=Entry(DataFrameLeft,textvariable=self.issuedate_var,font=("arial",13,"bold"),bg="white",bd=2,relief=RIDGE,width=29)
        txtIssueDate.grid(row=5,column=1)
        txtIssueDate.place(x=150,y=160)

        lblExDate=Label(DataFrameLeft,font=("arial",12,"bold"),text="Expiry Date:",fg="red",bg="lightgreen",padx=2,pady=6)
        lblExDate.grid(row=6,column=0,sticky=W)
        lblExDate.place(x=-10,y=190)
        txtExDate=Entry(DataFrameLeft,textvariable=self.expdate_var,font=("arial",13,"bold"),bg="white",bd=2,relief=RIDGE,width=29)
        txtExDate.grid(row=6,column=1)
        txtExDate.place(x=150,y=192)

        lblUses=Label(DataFrameLeft,font=("arial",12,"bold"),text="Uses:",bg="lightgreen",fg="red",padx=2,pady=6)
        lblUses.grid(row=7,column=0,sticky=W)
        lblUses.place(x=-10,y=219)
        txtUses=Entry(DataFrameLeft,textvariable=self.uses_var,font=("arial",13,"bold"),bg="white",bd=2,relief=RIDGE,width=29)
        txtUses.grid(row=7,column=1)
        txtUses.place(x=150,y=222)

        lblSideEffect=Label(DataFrameLeft,font=("arial",12,"bold"),text="Side-Effects:",fg="red",bg="lightgreen",padx=2,pady=6)
        lblSideEffect.grid(row=7,column=0,sticky=W)
        lblSideEffect.place(x=425,y=-7)
        txtSideEffect=Entry(DataFrameLeft,textvariable=self.sideEffect_var,font=("arial",13,"bold"),bg="white",bd=2,relief=RIDGE,width=29)
        txtSideEffect.grid(row=7,column=1)
        txtSideEffect.place(x=535,y=0)

        
        lblPrecWarnings=Label(DataFrameLeft,font=("arial",12,"bold"),text="Precaution &\nWarnings:",fg="red",bg="lightgreen",padx=2,pady=6)
        lblPrecWarnings.grid(row=7,column=0,sticky=W)
        lblPrecWarnings.place(x=425,y=25)
        txtPrecWarnings=Entry(DataFrameLeft,textvariable=self.warning_var,font=("arial",13,"bold"),bg="white",bd=2,relief=RIDGE,width=29)
        txtPrecWarnings.grid(row=7,column=1)
        txtPrecWarnings.place(x=535,y=35)

            
        lblDosage=Label(DataFrameLeft,font=("arial",12,"bold"),text="Dosage:",fg="red",bg="lightgreen",padx=2,pady=6)
        lblDosage.grid(row=7,column=0,sticky=W)
        lblDosage.place(x=425,y=70)
        txtDosage=Entry(DataFrameLeft,textvariable=self.dosage_var,font=("arial",13,"bold"),bg="white",bd=2,relief=RIDGE,width=29)
        txtDosage.grid(row=7,column=1)
        txtDosage.place(x=535,y=75)

        lblPrice=Label(DataFrameLeft,font=("arial",12,"bold"),text="Price:",fg="red",bg="lightgreen",padx=2,pady=6)
        lblPrice.grid(row=7,column=0,sticky=W)
        lblPrice.place(x=425,y=100)
        txtPrice=Entry(DataFrameLeft,textvariable=self.price_var,font=("arial",13,"bold"),bg="white",bd=2,relief=RIDGE,width=29)
        txtPrice.grid(row=7,column=1)
        txtPrice.place(x=535,y=110)
        
        lblProductQty=Label(DataFrameLeft,font=("arial",12,"bold"),text="Product \n Quantity:",fg="red",bg="lightgreen",padx=2,pady=6)
        lblProductQty.grid(row=7,column=0,sticky=W)
        lblProductQty.place(x=420,y=130)
        txtProductQty=Entry(DataFrameLeft,textvariable=self.product_var,font=("arial",13,"bold"),bg="white",bd=2,relief=RIDGE,width=29)
        txtProductQty.grid(row=7,column=1)
        txtProductQty.place(x=535,y=150)

        
        lblLotNo=Label(DataFrameLeft,font=("arial",12,"bold"),text="Lot Number:",fg="red",bg="lightgreen",padx=2,pady=6)
        lblLotNo.grid(row=4,column=0,sticky=W)
        lblLotNo.place(x=-10,y=123)
        txtLotNo=Entry(DataFrameLeft,textvariable=self.lot_var,font=("arial",13,"bold"),bg="white",bd=2,relief=RIDGE,width=29)
        txtLotNo.grid(row=4,column=1)
        txtLotNo.place(x=150,y=127)

        lblQuotes=Label(DataFrameLeft,font=("times new roman",15,"bold"),relief=RIDGE,bd=2,text="'Medicine is a Science of Uncertainity & \n an Art of Probability'\n\t\t\t--William Osler",fg="white",bg="orange",padx=3,pady=3)
        lblQuotes.grid(row=7,column=0,sticky=W)
        lblQuotes.place(x=425,y=185)

        DataFrameRight=LabelFrame(DataFrame,bd=10,relief=RIDGE,bg="lightgreen",padx=20,text="Medicine Add Department",fg="darkgreen",font=("times new roman",25,"bold"))
        DataFrameRight.place(x=855,y=5,width=625,height=350)

        img3=Image.open(r"Images\img3.jpg")
        img3=img3.resize((130,100))
        self.photoimg3=ImageTk.PhotoImage(img3)
        b1=Button(self.root,image=self.photoimg3,borderwidth=2)
        b1.place(x=910,y=250)

        img4=Image.open(r"Images\img4.jpg")
        img4=img4.resize((130,100))
        self.photoimg4=ImageTk.PhotoImage(img4)
        b1=Button(self.root,image=self.photoimg4,borderwidth=2)
        b1.place(x=1050,y=250)

        lblrefno=Label(DataFrameRight,font=("arial",15,"bold"),text="Reference No:",fg="red",bg="lightgreen",padx=2,pady=6)
        lblrefno.place(x=265,y=5)
        txtrefno=Entry(DataFrameRight,textvariable=self.refMed_var,font=("arial",12,"bold"),bg="white",bd=2,relief=RIDGE,width=34)
        txtrefno.place(x=270,y=35)

        lblmedName=Label(DataFrameRight,font=("arial",15,"bold"),text="Medicine Name:",fg="red",bg="lightgreen",padx=2,pady=6)
        lblmedName.place(x=265,y=60)
        txtmedName=Entry(DataFrameRight,textvariable=self.addmed_var,font=("arial",12,"bold"),bg="white",bd=2,relief=RIDGE,width=34)
        txtmedName.place(x=270,y=95)

        side_frame=Frame(DataFrameRight,bd=4,relief=RIDGE,bg="white")
        side_frame.place(x=-10,y=110,width=277,height=160)

        sc_x=ttk.Scrollbar(side_frame,orient=HORIZONTAL)
        sc_x.pack(side=BOTTOM,fill=X)

        sc_y=ttk.Scrollbar(side_frame,orient=VERTICAL)
        sc_y.pack(side=RIGHT,fill=Y)

        self.medicine_stable=ttk.Treeview(side_frame,column=("ref","medname"),xscrollcommand=sc_x.set,yscrollcommand=sc_y.set)
        sc_x.config(command=self.medicine_stable.xview)
        sc_y.config(command=self.medicine_stable.yview)

        self.medicine_stable.heading("ref",text="Ref")
        self.medicine_stable.heading("medname",text="Medname")

        self.medicine_stable["show"]="headings"
        self.medicine_stable.pack(fill=BOTH,expand=1)

        self.medicine_stable.column("ref",width=100)
        self.medicine_stable.column("medname",width=100)
        self.fetch_dataMed()

        self.medicine_stable.bind("<ButtonRelease-1>",self.Medget_cursor)
        
        down_frame=Frame(DataFrameRight,bd=4,relief=RIDGE,bg="darkgreen")
        down_frame.place(x=270,y=125,width=135,height=145)

        btnAddmed=Button(down_frame,text="ADD",command=self.AddMed,font=("arial",13,"bold"),width=12,bg="blue",fg="white")
        btnAddmed.grid(row=0,column=0)
        btnAddmed.place(x=0,y=0)

        btnUpdatemed=Button(down_frame,text="UPDATE",command=self.UpdateMed,font=("arial",13,"bold"),width=12,bg="green",fg="white")
        btnUpdatemed.grid(row=1,column=0)
        btnUpdatemed.place(x=0,y=35)

        btnClearmed=Button(down_frame,text="CLEAR",command=self.ClearMed,font=("arial",13,"bold"),width=12,bg="orange",fg="white")
        btnClearmed.grid(row=1,column=0)
        btnClearmed.place(x=0,y=70)

        btnDeletemed=Button(down_frame,text="DELETE",command=self.DeleteMed,font=("arial",13,"bold"),width=12,bg="red",fg="white")
        btnDeletemed.grid(row=1,column=0)
        btnDeletemed.place(x=0,y=105)

        

        img5=Image.open(r"Images\img5.jpg")
        img5=img5.resize((165,145))
        self.photoimg5=ImageTk.PhotoImage(img5)
        b1=Button(self.root,image=self.photoimg5,borderwidth=2)
        b1.place(x=1330,y=370)

        FrameDetails=Frame(self.root,bd=15,relief=RIDGE,bg="lightgreen")
        FrameDetails.place(x=0,y=590,width=1535,height=245)

        Table_frame=Frame(self.root,bd=15,relief=RIDGE)
        Table_frame.place(x=0,y=590,width=1535,height=245)

        scroll_x=ttk.Scrollbar(Table_frame,orient=HORIZONTAL)
        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y=ttk.Scrollbar(Table_frame,orient=VERTICAL)
        scroll_y.pack(side=RIGHT,fill=Y)

        self.medicine_table=ttk.Treeview(Table_frame,column=("Reference No","Company Name","Type of Medicine","Issue Date","Expiry Date","Side Effect","Precautions and Warnings","Dosage","Price","Product Quantity","Uses","Name","Lot.No"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
        scroll_x.config(command=self.medicine_table.xview)
        scroll_y.config(command=self.medicine_table.yview)


        self.medicine_table.heading("Reference No",text="Reference Number")
        self.medicine_table.heading("Company Name",text="Company Name")
        self.medicine_table.heading("Type of Medicine",text="Type of Medicine")
        self.medicine_table.heading("Issue Date",text="Issue Date")
        self.medicine_table.heading("Expiry Date",text="Expiry Date")
        self.medicine_table.heading("Side Effect",text="Side Effect")
        self.medicine_table.heading("Precautions and Warnings",text="Precautions and Warnings")
        self.medicine_table.heading("Dosage",text="Dosage")
        self.medicine_table.heading("Price",text="Price")
        self.medicine_table.heading("Product Quantity",text="Product Quantity")
        self.medicine_table.heading("Uses",text="Uses")
        self.medicine_table.heading("Name",text="Medicine Name")
        self.medicine_table.heading("Lot.No",text=" Lot.No")
        self.medicine_table.pack(fill=BOTH,expand=1)

        self.medicine_table.column("Reference No",width=100)
        self.medicine_table.column("Company Name",width=100)
        self.medicine_table.column("Type of Medicine",width=100)
        self.medicine_table.column("Issue Date",width=100)
        self.medicine_table.column("Expiry Date",width=100)
        self.medicine_table.column("Side Effect",width=100)
        self.medicine_table.column("Precautions and Warnings",width=100)
        self.medicine_table.column("Dosage",width=100)
        self.medicine_table.column("Price",width=100)
        self.medicine_table.column("Product Quantity",width=100)
        self.medicine_table.column("Uses",width=100)
        self.medicine_table.column("Name",width=100)
        self.medicine_table.column("Lot.No",width=100)
        self.fetch_data()
        self.medicine_table.bind("<ButtonRelease-1>",self.get_cursor)
        


        self.medicine_table["show"]="headings"
        self.medicine_table.pack(fill=BOTH,expand=1)

#===============Side Table - MySQL Database Connection==========================#
    def AddMed(self):
        conn=mysql.connector.connect(host="localhost",username="root",password=os.environ["PHARMACY_DB_PASSWORD"],database="pharmacy_demo")
        my_cursor=conn.cursor()
        my_cursor.execute("insert into pharma(Ref,MedName) values(%s,%s)",(

                                                                                                                                    self.refMed_var.get(),
                                                                                                                                    self.addmed_var.get(),


                                                                                                                                ))
        conn.commit()
        self.fetch_dataMed()
        conn.close()
        messagebox.showinfo('Success','Medicine has been Added!')

    def Medget_cursor(self,event=""):
        cursor_row=self.medicine_stable.focus()
        content=self.medicine_stable.item(cursor_row)
        row=content["values"]
        self.refMed_var.set(row[0])
        self.addmed_var.set(row[1])

    def fetch_dataMed(self):
        conn=mysql.connector.connect(host="localhost",username="root",password=os.environ["PHARMACY_DB_PASSWORD"],database="pharmacy_demo")
        my_cursor=conn.cursor()
        my_cursor.execute("select * from pharma")
        rows=my_cursor.fetchall()
        if len(rows)!=0:
            self.medicine_stable.delete(*self.medicine_stable.get_children())
            for i in rows:
                self.medicine_stable.insert("",END,values=i)
            conn.commit()
        conn.close()
                

    def UpdateMed(self):
        if self.refMed_var.get()==""or self.addmed_var.get()=="":
            messagebox.showerror("Error!!!","All Fields are Required!!!")
        else:
            conn=mysql.connector.connect(host="localhost",username="root",password=os.environ["PHARMACY_DB_PASSWORD"],database="pharmacy_demo")
            my_cursor=conn.cursor()
            my_cursor.execute("update pharma set MedName=%s where Ref=%s",(

                                                                                                                                self.addmed_var.get(),
                                                                                                                                self.refMed_var.get(),


                                                                                                                            ))
        conn.commit()
        self.fetch_dataMed()
        conn.close()

        messagebox.showinfo("Success","Medicine has been Updated!")
        
    def DeleteMed(self):
        conn=mysql.connector.connect(host="localhost",username="root",password=os.environ["PHARMACY_DB_PASSWORD"],database="pharmacy_demo")
        my_cursor=conn.cursor()

        sql="delete from pharma where Ref=%s"
        val=(self.refMed_var.get(),)
        my_cursor.execute(sql,val)

        conn.commit()
        self.fetch_dataMed()
        conn.close()

        messagebox.showinfo("Success","Medicine has been Deleted Successfully!")

    def ClearMed(self):
        self.refMed_var.set("")
        self.addmed_var.set("")

#===========Main Table - MySQL Database Connction========================#
    def add_data(self):
        if self.ref_var.get()=="" or self.lot_var.get()=="":
            messagebox.showerror("Error!!!","All Fields are Required!")
        else:
            conn=mysql.connector.connect(host="localhost",username="root",password=os.environ["PHARMACY_DB_PASSWORD"],database="pharmacy_demo")
            my_cursor=conn.cursor()
            my_cursor.execute("insert into pharmacy values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(
                                                                                                                                                            self.ref_var.get(),
                                                                                                                                                            self.cmpName_var.get(),
                                                                                                                                                            self.typeMed_var.get(),
                                                                                                                                                            self.issuedate_var.get(),
                                                                                                                                                            self.expdate_var.get(),
                                                                                                                                                            self.sideEffect_var.get(),
                                                                                                                                                            self.warning_var.get(),
                                                                                                                                                            self.dosage_var.get(),
                                                                                                                                                            self.price_var.get(),
                                                                                                                                                            self.product_var.get(),
                                                                                                                                                            self.uses_var.get(),
                                                                                                                                                            self.medName_var.get(),
                                                                                                                                                            self.lot_var.get(),
                                                                                                        ))
            conn.commit()
            self.fetch_data()
            conn.close()
            messagebox.showinfo("Success","Data has been Inserted")

    def fetch_data(self):
        conn=mysql.connector.connect(host="localhost",username="root",password=os.environ["PHARMACY_DB_PASSWORD"],database="pharmacy_demo")
        my_cursor=conn.cursor()
        my_cursor.execute("select * from pharmacy")
        row=my_cursor.fetchall()
        if len(row)!=0:
            self.medicine_table.delete(*self.medicine_table.get_children())
            for i in row:
                self.medicine_table.insert("",END,values=i)
            conn.commit()
        conn.close()

    def   get_cursor(self,event=""):
        cursor_row=self.medicine_table.focus()
        content=self.medicine_table.item(cursor_row)
        row=content["values"]
        self.ref_var.set(row[0])
        self.cmpName_var.set(row[1])
        self.typeMed_var.set(row[2])
        self.issuedate_var.set(row[3])
        self.expdate_var.set(row[4])
        self.sideEffect_var.set(row[5])
        self.warning_var.set(row[6])
        self.dosage_var.set(row[7])
        self.price_var.set(row[8])
        self.product_var.set(row[9])
        self.uses_var.set(row[10])
        self.medName_var.set(row[11])
        self.lot_var.set(row[12])

    def delete(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                username="root",
                password=os.environ["PHARMACY_DB_PASSWORD"],
                database="pharmacy_demo"
            )
            my_cursor = conn.cursor()

            sql = "DELETE FROM pharmacy WHERE Ref_no = %s"
            val = (self.ref_var.get(),)

            my_cursor.execute(sql, val)
            conn.commit()

            conn.close()

            messagebox.showinfo("Success", "Medicine Data Deleted Successfully!")
        except Exception as e:

            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            ref_number_to_delete =Ref_no

    def Update(self):
        if self.ref_var.get()=="" or self.lot_var.get()=="":
            messagebox.showerror("Error!!!","All Fields Are Required")
        else:
            conn=mysql.connector.connect(host="localhost",username="root",password=os.environ["PHARMACY_DB_PASSWORD"],database="pharmacy_demo")
            my_cursor=conn.cursor()
            my_cursor.execute("update pharmacy set  cmpName=%s,TypeMed=%s,Issuedate=%s,Expdate=%s,Sideeffect=%s,warning=%s,dosage=%s,Price=%s,product=%s,Uses=%s,MedName=%s,LotNo=%s",(
                
                                                                                                                                                                                                                                                                                                                        self.cmpName_var.get(),
                                                                                                                                                                                                                                                                                                                        self.typeMed_var.get(),
                                                                                                                                                                                                                                                                                                                        self.issuedate_var.get(),
                                                                                                                                                                                                                                                                                                                        self.expdate_var.get(),
                                                                                                                                                                                                                                                                                                                        self.sideEffect_var.get(),
                                                                                                                                                                                                                                                                                                                        self.warning_var.get(),
                                                                                                                                                                                                                                                                                                                        self.dosage_var.get(),
                                                                                                                                                                                                                                                                                                                        self.price_var.get(),
                                                                                                                                                                                                                                                                                                                        self.product_var.get(),
                                                                                                                                                                                                                                                                                                                        self.uses_var.get(),
                                                                                                                                                                                                                                                                                                                        self.medName_var.get(),
                                                                                                                                                                                                                                                                                                                        self.lot_var.get(),                                                                                                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                                                                                                            ))
            conn.commit()
            self.fetch_data()
            conn.close()
            messagebox.showinfo("Update!!!","Record has been Updated Successfully!")
            
    def reset(self):
            self.cmpName_var.set(""),
            self.lot_var.set(""),
            self.issuedate_var.set(""),
            self.expdate_var.set(""),
            self.uses_var.set(""),
            self.sideEffect_var.set(""),
            self.warning_var.set(""),
            self.dosage_var.set(r""),
            self.price_var.set(r""),
            self.product_var.set(r""),

    def search_data(self):
        conn=mysql.connector.connect(host="localhost",username="root",password=os.environ["PHARMACY_DB_PASSWORD"],database="pharmacy_demo")
        my_cursor=conn.cursor()
        my_cursor.execute("SELECT * FROM pharmacy WHERE " + str(self.search_var.get()) + " LIKE '%" + str(self.searchTxt_var.get()) + "%'") 

        rows=my_cursor.fetchall()
        if len(rows)!=0:
            self.medicine_table.delete(*self.medicine_table.get_children())
            for i in rows:
                self.medicine_table.insert("",END,values=i)
            conn.commit()
        conn.close()
        
    def refresh_page(self):
        
        self.root.destroy()
        new_root = Tk()
        new_obj = PharmacyManagementSystem(new_root)
        new_root.mainloop()

    def fun1(self):
        subprocess.Popen([sys.executable, r"Bill Invoice.py"])


        
if __name__=="__main__":
    root=Tk()
    obj=PharmacyManagementSystem(root)
    root.mainloop()
