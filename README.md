# Event Management System

This is a full-stack **Event Management System** built with Django (backend) and modern frontend technologies. It allows users to create, manage, and register for events in a streamlined way.

## 🚀 Features

- User registration and authentication
- Create, update, and delete events
- Event categories and filtering
- User event participation
- Admin panel for managing events and users
- Responsive UI

## 🛠️ Tech Stack

- **Backend:** Django, Django REST Framework
- **Database:** SQLite
- **Frontend:** React, Tailwind CSS
- **Authentication:** JWT
- **API:** RESTful APIs using DRF


## ⚙️ Installation & Setup

**Clone the Repository**
   ```bash
   git clone https://github.com/Stropurbo/event-management.git
   cd event-management

python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

python manage.py createsuperuser
