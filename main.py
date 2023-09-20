from flask import Flask, render_template, request, redirect, url_for, session, flash
from chain import BlockChain
import json

from send_email import send_email

app = Flask(__name__)
app.secret_key = "alkdjfalkdjf"


@app.route("/")
def home():
    return render_template('Main_Page.html')


@app.route("/x")
def x():
    if session.get("user"):
        return render_template('home.html')
    else:
        flash("Please login to access Verifier")
        return redirect(url_for('login'))


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        pswd = request.form["password"]

        if user == "Admin":
            if pswd == "password":
                session["user"] = "Admin"
                return redirect(url_for("admin"))

        elif user == "admin":
            if pswd == "password":
                session["user"] = "admin"
                return redirect(url_for("x"))

        else:
            flash("Invalid Login details")
            return redirect(url_for('login'))
    else:
        return render_template('login.html')


@app.route("/verify/<kid>", methods=["GET"])
def verify(kid):
    return render_template('verify.html', keyId=kid)


@app.route("/verify", methods=["POST"])
def success():
    post_data = request.form["keyId"]

    with open('./NODES/N1/blockchain.json', 'r') as bfile:
        n1_data = str(bfile.read())
    with open('./NODES/N2/blockchain.json', 'r') as bfile:
        n2_data = str(bfile.read())
    with open('./NODES/N3/blockchain.json', 'r') as bfile:
        n3_data = str(bfile.read())
    with open('./NODES/N4/blockchain.json', 'r') as bfile:
        n4_data = str(bfile.read())

    pd = str(post_data)

    if (pd in n1_data) and (pd in n2_data) and (pd in n3_data) and (pd in n4_data):

        with open('./NODES/N1/blockchain.json', 'r') as bfile:
            for x in bfile:
                if pd in x:
                    a = json.loads(x)["data"]
                    b = a.replace("'", "\"")
                    data = json.loads(b)

                    s_department = data["Department"]
                    s_name = data["PName"]
                    s_batch = data["PBatch"]
                    dob_date = data["PdobDate"]
                    pass_date = data["PpassDate"]
                    s_id = data["PId"]
                    s_cgpa = data["Pcgpa"]
                    s_grade = data["Pgrade"]
                    s_type = data["PType"]
                    s_hash = data["hash"]

        return render_template('success.html', department=s_department, name=s_name, batch=s_batch,
                               dob=dob_date, passdate=pass_date, id=s_id, cgpa=s_cgpa,
                               grade=s_grade, type=s_type,shash=s_hash)

    else:
        return render_template('fraud.html')


@app.route("/addproduct", methods=["POST", "GET"])
def addproduct():
    if request.method == "POST":
        department = request.form["department"]
        name = request.form["name"]
        batch = request.form["batch"]
        pid = request.form["id"]
        dob = request.form["dob"]
        passdate = request.form["passdate"]
        cgpa = request.form["cgpa"]
        grade = request.form["grade"]
        ptype = request.form["type"]

        print(department, name, batch, dob, passdate, pid, cgpa, grade, ptype)
        bc = BlockChain()
        bc.addProduct(department, name, batch, dob, passdate, pid, cgpa, grade, ptype)

        flash("Certificate added successfully to the Blockchain")
        # return render_template('home.html')
        return redirect(url_for('x'))
    else:
        # return render_template('home.html')
        return redirect(url_for('x'))


@app.route("/admin")
def admin():
    if session["user"] == "Admin":
        return render_template('admin.html')
    else:
        return redirect(url_for('login'))


@app.route("/verifyNodes")
def verifyNodes():
    bc = BlockChain()
    isBV = bc.isBlockchainValid()

    if isBV:
        flash("All Nodes of Blockchain are valid")
        return redirect(url_for('admin'))
    else:
        flash("Blockchain Nodes are not valid")
        return redirect(url_for('admin'))


@app.route("/addcertificatedetail")
def addcertificatedetail():
    return render_template('addCertificateDetails.html')


@app.route('/companydetails')
def companydetails():
    return render_template('companydetails.html')


@app.route('/submit', methods=['POST'])
def submit():
    # Get form data
    companyname = request.form['companyname']
    nameofverifier = request.form['nameofverifier']
    studentname = request.form['studentname']
    semail = request.form['semail']
    purpose = request.form['purpose']

    # Create dictionary with form data
    data = {'companyname': companyname, 'nameofverifier': nameofverifier,'studentname': studentname, 'semail': semail, 'purpose': purpose}

    # Read current data from JSON file
    with open('static/company.json', 'r') as f:
        current_data = json.load(f)

    # Add new data to JSON object
    current_data.append(data)

    # Send email to user
    subject = 'B-12'
    body = f'Dear {studentname},\n\n your details has been verified by {nameofverifier} ,{companyname}.\n\n for {purpose}\n\nSincerely,\nB12 Final year project '
    send_email(semail, subject, body)

    # Write updated data back to JSON file
    with open('static/company.json', 'w') as f:
        json.dump(current_data, f, indent=4)

    return redirect('verifier_QR_Hash')


@app.route('/submit-form', methods=['POST'])
def submit_form():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    semail = 'verifiercertificate@gmail.com'
    subject = f'New message from {name}'
    body = f'Name: {name}\nEmail: {email}\nMessage: {message}'
    send_email(semail, subject, body)
    return redirect('/')


@app.route("/logout")
def logout():
    session["user"] = ""
    return redirect(url_for('login'))


@app.route("/ContactUs")
def ContactUs():
    return render_template('contact_us.html')


@app.route("/AboutUs")
def AboutUs():
    return render_template('About_Us.html')


@app.route("/Student_QR_Hash")
def Student_QR_Hash():
    return render_template('studentQRandH.html')


@app.route("/verifier_QR_Hash")
def verifier_QR_Hash():
    return render_template('VerifierQRandH.html')

@app.route("/collegeviewforcompany")
def collegeviewforcompany():
    return render_template('collegeviewforcompany.html')


if __name__ == "__main__":
    app.run(debug=True)
    session["user"] = ""
