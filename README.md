# AskPy
Built with Django, AJAX, ChatterBot &amp; spaCy, AskPy is a smooth-talking chatbot that answers your questions, learns new stuff through an admin panel, and handles unknowns like a champ. Retrain it, talk to it, break it—it's still standing.

---

## Setup Instructions

Follow these steps to get the project running on your machine:


### 1. Clone the Repo

"git clone https://github.com/Thaveesha-Sathsara/AskPy.git"


### 2. Create a Virtual Environment (optional but recommended)

python -m venv env
source env/bin/activate        # For Linux/Mac
env\Scripts\activate           # For Windows


### 3. Install Dependencies

pip install -r requirements.txt


### 4. Install spaCy English Model

python -m spacy download en_core_web_sm


### 5. Make Migrations & Migrate

python manage.py makemigrations
python manage.py migrate


### 6. Run the Server

python manage.py runserver


### 7. Access Chatbot

after running the server visit below address to use AskPy :
http://127.0.0.1:8000/blog/


### 8. Admin Access

to get admin panel access visit below address :
http://127.0.0.1:8000/admin/


### 9. Retrain Bot

to retrain the bot visit below address :
http://127.0.0.1:8000/blog/retrain/
