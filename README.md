# 💊 Python Pharmacy Management System

A Python desktop application for maintaining medicine records, customer or hospital addresses, and generating PDF documents.

**Personalized project maintained by Gonela Surya Teja**  
**Institution:** SRM Institute of Science and Technology, Kattankulathur  
**Expected graduation:** 2029

This is an educational adaptation of an existing project. See [Acknowledgements](#acknowledgements) for the original source.

## Overview

The application uses Tkinter for its desktop interface and MySQL for persistent data storage. It includes separate login, medicine-management, and invoice windows.

## Features and current status

- Demo login with fixed credentials.
- Medicine reference and name management.
- Medicine details including company, type, issue date, expiry date, dosage, price, uses, and lot number.
- Record display, search, addition, and deletion workflows.
- Customer or hospital address records.
- PDF report and invoice generation code.

The application has been launched locally and the MySQL connection has been verified. Complete feature testing is still pending.

> **Known issue:** The original medicine and address Update queries lack a `WHERE` clause and can modify every row. Do not use these buttons until the queries are corrected and tested.

## Technology stack

| Component | Technology |
| --- | --- |
| Language | Python |
| Desktop interface | Tkinter / ttk |
| Database | MySQL Server |
| Database administration | MySQL Workbench |
| Database connector | mysql-connector-python |
| Image handling | Pillow |
| PDF generation | fpdf2, ReportLab |
| Development tools | VS Code, Git |

## Project files

| File or folder | Purpose |
| --- | --- |
| `Login Page.py` | Demo login and dashboard launch |
| `Pharmacy Management System Project.py` | Medicine records and reporting |
| `Bill Invoice.py` | Address records and invoice generation |
| `Images/` | Images referenced by the interface and invoice |
| `.venv/` | Local Python environment; exclude from Git |
| `README.md` | Project information and setup instructions |

## Setup on Windows

### 1. Open the project

Open the project folder in VS Code, then open a PowerShell terminal inside that folder.

### 2. Create the Python environment

```powershell
python --version
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install pillow mysql-connector-python fpdf2 reportlab
```

Verify the dependencies:

```powershell
.\.venv\Scripts\python.exe -c "import tkinter, PIL, mysql.connector, fpdf, reportlab; print('All packages are ready')"
```

The Python installation must include Tcl/Tk support. MySQL Server is installed separately from the Python connector.

### 3. Set up MySQL

Install MySQL Server and MySQL Workbench. Start the MySQL service, connect to the local server in Workbench, and execute the following SQL.

The column order is significant because the current application uses positional inserts and `SELECT *`. Dates remain text fields for compatibility with the existing input forms.

```sql
CREATE DATABASE IF NOT EXISTS pharmacy_demo;
USE pharmacy_demo;

CREATE TABLE IF NOT EXISTS pharma (
    Ref VARCHAR(50) PRIMARY KEY,
    MedName VARCHAR(150)
);

CREATE TABLE IF NOT EXISTS pharmacy (
    Ref_no VARCHAR(50) PRIMARY KEY,
    cmpName VARCHAR(150),
    TypeMed VARCHAR(100),
    Issuedate VARCHAR(50),
    Expdate VARCHAR(50),
    Sideeffect TEXT,
    warning TEXT,
    dosage VARCHAR(100),
    Price DECIMAL(10,2),
    product VARCHAR(100),
    Uses TEXT,
    MedName VARCHAR(150),
    LotNo VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS toaddress (
    CmpName VARCHAR(150) PRIMARY KEY,
    Address TEXT,
    City VARCHAR(100),
    State VARCHAR(100),
    Country VARCHAR(100),
    PinCode VARCHAR(20),
    Contact VARCHAR(30),
    email VARCHAR(150)
);

INSERT IGNORE INTO pharma (Ref, MedName)
VALUES ('REF001', 'Demo Item');

SHOW TABLES;
```

`CREATE TABLE IF NOT EXISTS` does not repair an existing table with a different schema. Back up existing data before making schema changes.

### 4. Configure database connections

Set the database password in the PowerShell session you will use to run the application:

```powershell
$env:PHARMACY_DB_PASSWORD = "YOUR_LOCAL_MYSQL_PASSWORD"
```

The application reads this variable for each MySQL connection. Do not commit the password or put it directly in the Python files.

```python
import os

mysql.connector.connect(
    host="localhost",
    username="root",
    password=os.environ["PHARMACY_DB_PASSWORD"],
    database="pharmacy_demo"
)
```

The password above is a placeholder. Do not commit actual credentials. Before publishing the code, move credentials into environment variables or a local configuration file excluded from Git, and use a dedicated application database account.

### 5. Configure images and script paths

Keep paths relative to the project, for example:

```python
self.bg = ImageTk.PhotoImage(file=r"Images\bg.jpg")
```

The application references these assets:

- `Images/bg.jpg`
- `Images/bg2.jpg`
- `Images/img1.jpg`
- `Images/img2.png`
- `Images/img3.jpg`
- `Images/img4.jpg`
- `Images/img5.jpg`
- `Images/stamp.jpg`

Supply appropriate images or temporary placeholders. The original repository did not include these assets. Use only images you have permission to redistribute.

Add `import sys` to each Python file that launches another script. Use the current interpreter for subprocesses:

```python
import sys
import subprocess

subprocess.Popen([
    sys.executable,
    r"Pharmacy Management System Project.py"
])
```

Remove paths tied to the original author's computer, including paths for opening generated PDFs. Run from the project folder so relative paths resolve correctly.

### 6. Run the application

```powershell
.\.venv\Scripts\python.exe "Login Page.py"
```

Demo login:

| Field | Value |
| --- | --- |
| Username | `agent` |
| Password | `pharma` |

These are fixed demo credentials, separate from the MySQL password. The current login does not provide user registration, password hashing, or role-based access control.

## Suggested verification

1. Log in and open the medicine dashboard.
2. Add a fictional medicine reference and a corresponding detail record.
3. Restart the application and confirm the record persists.
4. Search for the test record.
5. Test address entry and PDF generation using fictional data.
6. After fixing the Update queries, verify that updating one record leaves all other records unchanged.

## Troubleshooting

| Problem | Check |
| --- | --- |
| `py` is not recognized | Use `python` if it is available. |
| Missing Python module | Install dependencies with the `.venv` interpreter shown above. |
| Image file not found | Check `Images/`, exact filenames, and the working directory. |
| MySQL access denied | Check credentials in every connection call. |
| Cannot connect to MySQL | Confirm the MySQL Windows service is running. |
| Unknown database or column | Check `pharmacy_demo` and the schema above. |
| `sys` is not defined | Add `import sys` to the file using `sys.executable`. |

## Planned improvements

- Correct and test Update operations with record-specific conditions.
- Parameterize search values and restrict selectable SQL column names.
- Replace fixed credentials with hashed-password authentication and user roles.
- Centralize database configuration and remove embedded secrets.
- Add quantity tracking, low-stock notifications, and expiry alerts.
- Add date and numeric validation.
- Improve resizing, layout, and visual design.
- Improve invoice numbering, billing calculations, and report validation.

These are planned enhancements, not claims about implemented functionality.

## Maintainer

**Gonela Surya Teja**  
SRM Institute of Science and Technology, Kattankulathur  
Expected graduation: **2029**

This adaptation is used to learn Python desktop development, MySQL integration, debugging, and project documentation.

## Acknowledgements

Based on the [Pharmacy Management System Python–MySQL project by NandhaKumar1720](https://github.com/NandhaKumar1720/Pharmacy-Management-System-Python-MySQL-Project-).

Credit for the original application remains with its original author. Local setup, configuration, and documentation have been adapted for this learning project. Retain applicable notices and check the original repository's license terms before redistribution; this README does not grant a new license to the original code.

## Educational use

Use fictional demonstration data. This project is a learning prototype and has not been validated for real pharmacy operations or sensitive customer records.
