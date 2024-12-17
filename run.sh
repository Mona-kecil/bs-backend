PYTHONPATH=$(pwd) python app/models/database.py
PYTHONPATH=$(pwd) uvicorn app.main:app --reload
