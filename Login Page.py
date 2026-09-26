import sys
import tkinter as tk
from tkinter import messagebox
import subprocess
from PIL import Image, ImageTk

class PharmacyManagementSystem:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Agent Login")
        self.root.geometry("1920x1080")

        self.bg = ImageTk.PhotoImage(file=r"Images\bg.jpg")
        lbl_bg = tk.Label(self.root, image=self.bg)
        lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)

        txt = "Blaze Pharmacy Management System!.....\nAgent Login...."
        count = 0
        text = ' '

        label = tk.Label(self.root, text=txt, font=("times new roman", 30, "bold"), fg="red",bg="black")
        label.pack(pady=50)

        def slider():
            nonlocal count, text
            if count >= len(txt):
                count = -1
                text = ''
                label.configure(text=text)
            else:
                text = text + txt[count]
                label.configure(text=text)
            count += 1
            label.after(100, slider)

        slider()

        frame = tk.Frame(self.root, bg="black", relief=tk.RIDGE, bd=10)
        frame.pack(padx=100, pady=100, anchor="center")

    
        self.username_label = tk.Label(frame, text="Username:", font=("times new roman", 26, "bold"), fg="white", bg="black")
        self.username_entry = tk.Entry(frame, font=("Arial", 24))
        self.password_label = tk.Label(frame, text="Password:", font=("times new roman", 26, "bold"), fg="white", bg="black")
        self.password_entry = tk.Entry(frame, show="*", font=("Arial", 24))
        login_button = tk.Button(frame, text="Login", command=self.fun2, font=("times new roman", 20, "bold"), bg="red", fg="white")

        self.username_label.grid(row=0, column=0, padx=10, pady=10)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)
        self.password_label.grid(row=1, column=0, padx=10, pady=50)
        self.password_entry.grid(row=1, column=1, padx=10, pady=50)
        login_button.grid(row=2, columnspan=2, padx=10, pady=10)

    def fun1(self):
        subprocess.Popen([sys.executable, r"Pharmacy Management System Project.py"])

    def fun2(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "agent" and password == "pharma":
            messagebox.showinfo("Success", "Login successful! Redirecting...")
            self.fun1()
        else:
            messagebox.showerror("Error", "Invalid credentials. Please try again.")

if __name__ == "__main__":
    app = PharmacyManagementSystem()
    app.root.mainloop()
