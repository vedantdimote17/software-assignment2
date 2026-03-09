from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "secretkey"

# Temporary storage (instead of database)
users = []
contacts_list = []
sos_alerts = []
incidents = []

# ------------------ ROUTES ------------------

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        users.append({
            "id": len(users)+1,
            "name": request.form['name'],
            "email": request.form['email'],
            "phone": request.form['phone'],
            "password": request.form['password']
        })
        return redirect('/login')
    return render_template("register.html")

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        for user in users:
            if user["email"] == request.form['email'] and user["password"] == request.form['password']:
                session['user_id'] = user["id"]
                return redirect('/dashboard')
    return render_template("login.html")

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        return render_template("dashboard.html")
    return redirect('/login')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# -------- CONTACTS --------

@app.route('/contacts', methods=['GET','POST'])
def contacts():
    if 'user_id' not in session:
        return redirect('/login')

    if request.method == 'POST':
        contacts_list.append({
            "user_id": session['user_id'],
            "name": request.form['name'],
            "phone": request.form['phone']
        })

    user_contacts = [c for c in contacts_list if c["user_id"] == session['user_id']]
    return render_template("contacts.html", contacts=user_contacts)

# -------- SOS --------

@app.route('/sos', methods=['GET','POST'])
def sos():
    if 'user_id' not in session:
        return redirect('/login')

    if request.method == 'POST':
        sos_alerts.append({
            "user_id": session['user_id'],
            "latitude": request.form['latitude'],
            "longitude": request.form['longitude']
        })
        return "SOS Alert Sent Successfully!"

    return render_template("sos.html")

# -------- REPORT INCIDENT --------

@app.route('/report', methods=['GET','POST'])
def report():
    if 'user_id' not in session:
        return redirect('/login')

    if request.method == 'POST':
        incidents.append({
            "user_id": session['user_id'],
            "location": request.form['location'],
            "description": request.form['description']
        })
        return redirect('/dashboard')

    return render_template("report.html")

# -------- VIEW ALERTS --------

@app.route('/alerts')
def alerts():
    if 'user_id' not in session:
        return redirect('/login')

    user_alerts = [a for a in sos_alerts if a["user_id"] == session['user_id']]
    return render_template("alerts.html", alerts=user_alerts)

if __name__ == "__main__":
    app.run(debug=True)