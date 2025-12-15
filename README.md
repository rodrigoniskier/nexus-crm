# 💼 Nexus CRM | Freelance Deal Management System

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit)
![Status](https://img.shields.io/badge/Status-Production-success?style=for-the-badge)

## 📋 System Overview
**Nexus CRM** is a lightweight, cloud-ready Customer Relationship Management tool designed for freelancers and boutique agencies. Unlike static dashboards, Nexus implements a **Full CRUD (Create, Read, Update, Delete)** architecture with persistent data storage.

It enables professionals to track deal flow, manage client contact details, and visualize revenue pipelines without the complexity of enterprise tools like Salesforce.

## ✨ Key Features
* **Persistent Storage:** Built-in SQLite database ensures data survives between sessions.
* **Pipeline Analytics:** Real-time calculation of Total Pipeline, Win Rates, and Average Deal Size.
* **Deal Management:** Add, Edit, and Delete records via a secure UI.
* **Visual Insights:** Interactive revenue distribution charts powered by Plotly.
* **Modern UI:** Designed with a "Corporate Clean" aesthetic (Inter font, high-contrast palette) for professional environments.

## 🛠️ Tech Stack
* **Frontend:** Streamlit (Custom CSS)
* **Backend Logic:** Python
* **Database:** SQLite3 (SQLAlchemy compatible)
* **Visualization:** Plotly Express

## 🚀 Installation

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/SEU-USUARIO/nexus-crm.git](https://github.com/SEU-USUARIO/nexus-crm.git)
    cd nexus-crm
    ```

2.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application**
    ```bash
    streamlit run app.py
    ```

---
**License:** MIT License
<br>
**Developer:** Rodrigo Niskier
