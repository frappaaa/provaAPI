from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def create_tables():
    print("Creating tables...")
    conn = sqlite3.connect('test_ist.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS Utenti (
                    id INTEGER PRIMARY KEY,
                    nome TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    password_hash TEXT NOT NULL
                )''')
    print("Utenti table checked/created.")

    c.execute('''CREATE TABLE IF NOT EXISTS LuoghiTest (
                    id INTEGER PRIMARY KEY,
                    nome TEXT NOT NULL,
                    indirizzo TEXT NOT NULL,
                    contatti TEXT,
                    tipologie_test TEXT
                )''')
    print("LuoghiTest table checked/created.")

    c.execute('''CREATE TABLE IF NOT EXISTS Prenotazioni (
                    id INTEGER PRIMARY KEY,
                    id_utente INTEGER,
                    id_luogo INTEGER,
                    data TEXT,
                    FOREIGN KEY(id_utente) REFERENCES Utenti(id),
                    FOREIGN KEY(id_luogo) REFERENCES LuoghiTest(id)
                )''')
    print("Prenotazioni table checked/created.")
    conn.commit()
    conn.close()
    print("Tables created successfully.")

@app.route('/register', methods=['POST'])
def register_user():
    print("Register endpoint called.")
    data = request.json
    print(f"Received data: {data}")
    conn = sqlite3.connect('test_ist.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO Utenti (nome, email, password_hash) VALUES (?, ?, ?)",
                  (data['nome'], data['email'], data['password_hash']))
        conn.commit()
        print("User registered successfully!")
        return jsonify({"message": "User registered successfully!"}), 201
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()
        print("Database connection closed.")

@app.route('/')
def home():
    print("Home endpoint called.")
    return "Welcome to the Test IST App!"

if __name__ == '__main__':
    print("Starting the application...")
    create_tables()
    app.run(debug=True)
