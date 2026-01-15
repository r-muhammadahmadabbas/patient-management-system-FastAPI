# 🏥 Patient Management System

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Frontend](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)

A full-stack Patient Health Monitoring System built with **FastAPI** (Backend) and **Vanilla JS/CSS** (Frontend). This application manages patient demographics, automatically calculates BMI, and determines health verdicts (e.g., Obese, Normal, Underweight) based on WHO standards.

---

## 🌟 Key Features

### Backend (FastAPI)
* **CRUD Operations:** Full Create, Read, Update, and Delete capabilities for patient records.
* **Computed Logic:** Automatically calculates `BMI` and `Verdict` using Pydantic computed fields.
* **Sorting Engine:** Server-side sorting of patients by `Weight`, `Height`, or `BMI` (Ascending/Descending).
* **Data Persistence:** Uses a lightweight JSON file (`patients.json`) as a database.
* **Input Validation:** Robust validation using Pydantic (e.g., Age 0-120, positive height/weight).

### Frontend (HTML/JS)
* **Glassmorphism UI:** Modern, responsive interface with visual animations.
* **Dynamic Tabs:** Seamless switching between View, Create, Edit, and Sort views without page reloads.
* **Real-time Feedback:** Visual badges for health status (Normal, Obese, etc.) and alert notifications for API responses.

---

## 🛠️ Project Structure

```bash
📦 Patient-Management-System
 ┣ 📜 main.py           # FastAPI Application entry point
 ┣ 📜 index.html        # Frontend User Interface
 ┣ 📜 patients.json     # JSON Database storage
 ┗ 📜 README.md         # Project Documentation