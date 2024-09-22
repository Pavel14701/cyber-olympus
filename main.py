from app import CyberOlympusApp
from models import db

app=CyberOlympusApp(db, debug=True)

if __name__ == '__main__':
    app.run()