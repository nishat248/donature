# 🌍 Donature – A Donation Management System

**Donature** is a web-based donation management platform built with **Django**.  
It connects **donors**, **NGOs**, and **recipients** under one system — enabling users to donate, request, and manage resources transparently and efficiently.

---

## 🚀 Features

- 🧍 **User Roles:** Donor, Recipient & NGO  
- 🎁 **Donation Management:** Create, view & manage donation posts  
- 🏆 **Reward System:** Earn badges and points for contributions  
- 📦 **Item & Campaign Tracking:** Keep track of donation status  
- 🧾 **Request & Approval System:** Requests are verified by admin  
- 🖼️ **Media Uploads:** Supports images & documents  
- ⚙️ **Admin Panel:** Manage users, NGOs, categories, and donations  
- 💬 **Contact & Feedback:** Easy communication system  
- 🎨 **Responsive Design:** Mobile-friendly, clean & elegant UI  

---

## 🏗️ Tech Stack

| Category         | Technology               |
|------------------|--------------------------|
| **Framework**    | Django (Python)          |
| **Frontend**     | HTML5, CSS3, JavaScript  |
| **Database**     | SQLite3                  |
| **Tools**        | Git, VS Code             |
| **Version Control** | GitHub                |

---

## 📁 Project Structure
```
DonationManagementSystem/            # Root folder (only for organization)
│
├── venv/                            # Virtual environment (ignored by git)
│
└── donature/                        # Outer Django project folder (Git repo root)
    ├── donature/                    # Inner project folder (settings, urls, wsgi)
    ├── donations/                   # App: donation-related features
    ├── ngos/                        # App: NGO management
    ├── custom_admin/                # App: Custom admin functions
    ├── media/                       # Uploaded user images & docs
    ├── static/                      # Static files (CSS, JS, images)
    ├── templates/                   # HTML templates
    ├── db.sqlite3                   # SQLite database
    ├── manage.py                    # Django management file
    └── .gitignore                  
```
---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/nishat248/donature.git
cd donature
```
### 2️⃣ Activate Virtual Environment
```bash
venv\Scripts\activate
```
### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
### 4️⃣ Run the Server
```bash
python manage.py runserver
```
### 5️⃣ Access the App
Open your browser and go to 👉 http://127.0.0.1:8000/

## 🧠 Usage
Donors: Create and manage donation posts

Recipients: Request items or campaigns

NGOs: Manage donation appeals & campaigns

Admin: Approve, reject, and oversee all activity

## 👩‍💻 Developer
👤 Nishat Anjum

GitHub: @nishat248

### 📘 Project: Donature – Django Donation Management System

🏫 Department of Computer Science & Engineering

🎓 Academic Project – 2025

### ⚠️ Disclaimer
This project is developed for academic and learning purposes.
All data, media, and content used here are for demonstration only.
