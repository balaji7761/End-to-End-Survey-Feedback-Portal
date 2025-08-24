# 📊 Survey Feedback Application

A lightweight **Survey Feedback Application** built with **HTML, CSS, JavaScript** for the frontend and **SQLite** for backend data storage.  
This project demonstrates **full-stack development using minimal technologies** — ideal for simple survey management and feedback collection.

---

## 🚀 Features

- **Survey Management**
  - Create and manage surveys with multiple question types.
  - Store surveys and responses in an SQLite database.

- **Feedback Collection**
  - Users can submit feedback through a clean, responsive interface.
  - Prevents duplicate submissions.

- **Results Dashboard**
  - View collected responses.
  - Summarized feedback for admins.

---

## 🏗️ Architecture

```mermaid
flowchart TD
    A[User] --> B[HTML/CSS/JS Frontend]
    B --> C[Backend Server (Python/Flask/Django)]
    C --> D[(SQLite Database)]
