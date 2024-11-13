# login_bp_folder/run.py
from app import create_app

appln = create_app()

if __name__ == "__main__":
    appln.run(debug=True)
