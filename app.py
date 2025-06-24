from flask import Flask, render_template_string, request, redirect
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('redzone.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT, saldo INTEGER, point INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER, tipe TEXT, jumlah INTEGER)''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    conn = sqlite3.connect('redzone.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id=1")
    user = c.fetchone()
    conn.close()
    return render_template_string(template, user=user)

@app.route('/topup', methods=['POST'])
def topup():
    amount = int(request.form['amount'])
    conn = sqlite3.connect('redzone.db')
    c = conn.cursor()
    c.execute("UPDATE users SET saldo = saldo + ? WHERE id = 1", (amount,))
    c.execute("INSERT INTO transactions (user_id, tipe, jumlah) VALUES (1, 'Top Up', ?)", (amount,))
    conn.commit()
    conn.close()
    return redirect('/')

# HTML, CSS, JS dijadikan satu
template = '''
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>Redzone Store</title>
    <style>
        body { font-family: sans-serif; background: #fff; margin: 0; }
        header { background: red; color: white; padding: 15px; }
        .box { background: #f9f9f9; padding: 10px; margin: 10px; border-radius: 8px; }
        .menu { display: flex; justify-content: space-around; flex-wrap: wrap; }
        .menu div { width: 22%; background: #eee; margin: 5px; padding: 10px; border-radius: 10px; text-align: center; }
        .nav { position: fixed; bottom: 0; width: 100%; background: #fff; display: flex; justify-content: space-around; border-top: 1px solid #ccc; }
        .nav div { padding: 10px; }
        button { background: red; color: white; padding: 10px; border: none; border-radius: 8px; }
    </style>
</head>
<body>
    <header>
        <h2>Hai, {{ user[1] if user else 'User' }}</h2>
        <p>Saldo: Rp {{ user[2] if user else 0 }} | Poin: {{ user[3] if user else 0 }}</p>
    </header>
    <div class="box">
        <form action="/topup" method="POST">
            <input type="number" name="amount" placeholder="Jumlah Top Up" required>
            <button type="submit">Top Up</button>
        </form>
    </div>
    <div class="box menu">
        <div>Pulsa</div>
        <div>Token PLN</div>
        <div>E-Money</div>
        <div>Top Up Game</div>
        <div>Telkomsel</div>
        <div>Indosat</div>
        <div>Axis</div>
        <div>XL</div>
    </div>
    <div class="nav">
        <div>Home</div>
        <div>Transaksi</div>
        <div>+</div>
        <div>Balapan</div>
        <div>Akun</div>
    </div>
</body>
</html>
'''

if __name__ == '__main__':
    init_db()
    # Auto-create dummy user
    conn = sqlite3.connect('redzone.db')
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (id, name, saldo, point) VALUES (1, 'Lukman', 0, 0)")
    conn.commit()
    conn.close()
    app.run(debug=True)
