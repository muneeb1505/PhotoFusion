from flask import Flask, render_template,request, flash
from werkzeug.utils import secure_filename
import os
import cv2
import numpy as np



UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'webp', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = 'the random string'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def ProcessImage(filename, operation):
    print(f"operation is {operation} and filename is {filename}")
    img = cv2.imread(f"uploads/{filename}")
    match operation:
        case "cpng":
            newFilename = f"static/{filename.split('.')[0]}.png"
            cv2.imwrite(newFilename, img)
            return newFilename
        
        case "cjpg":
            newFilename = f"static/{filename.split('.')[0]}.jpg"
            cv2.imwrite(newFilename, img)
            return newFilename
        
        case "cgray":
            imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            newFilename = f"static/{filename}"
            cv2.imwrite(newFilename, imgGray)
            return newFilename
        
        case "cwebp":
            newFilename = f"static/{filename.split('.')[0]}.webp"
            cv2.imwrite(newFilename, img)
            return newFilename
        
        case "cjpg2":
            newFilename = f"static/{filename.split('.')[0]}.jpg"
            cv2.imwrite(newFilename, img)
            return newFilename
        
        case "cgif":
            newFilename = f"static/{filename.split('.')[0]}.gif"
            cv2.imwrite(newFilename, img)
            return newFilename
        
        case "ccar":
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            gray = cv2.medianBlur(gray,5)
            edges = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,9,9)
            color = cv2.bilateralFilter(img, 9, 250, 250)
            cartoon = cv2.bitwise_and(color, color, mask=edges)
            newFilename = f"static/{filename.split('.')[0]}.jpg"
            cv2.imwrite(newFilename, cartoon)

    return newFilename
    pass

@app.route("/")
def home():
    return render_template("imageWeb.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/use")
def use():
    return render_template("use.html")

@app.route("/contact")
def contact():
    return render_template("YTContact.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/edit", methods = ['GET', 'POST'])
def edit():
    if request.method == 'POST':
        operation = request.form.get("operation")
        if 'file' not in request.files:
            flash('No file part')
            return "Error"
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return "Error no selected file"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new = ProcessImage(filename, operation)
            flash(f"Your image has been ready <a href='/{new}' target='_blank'> here </a>")
            return render_template("imageWeb.html")
        
    return render_template("imageWeb.html")

app.run(debug=True)