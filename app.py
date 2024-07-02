from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from pymongo import MongoClient
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os
import user_file

app = Flask(__name__, static_folder='static')
app.secret_key = 'your_secret_key'

MONGO_URI = "mongodb+srv://nithin:nithin@cluster0.ohw9t2m.mongodb.net/Foodie?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)

db = client.get_database('Foodie')
user_collection = db.users
menu_collection = db.menu

@app.route('/menu')
def show_menu():
    menu_data = list(menu_collection.find({}))
    return render_template("Menu.html", menu=menu_data)

@app.route('/home')
def home():
    return render_template("Home.html")

@app.route('/reservation')
def reservation():
    return render_template("Reservation.html")

@app.route('/confirm_reser', methods=["POST"])
def confirm_reser():
    if request.method == "POST":
        people = request.form.get("people")
        date = request.form.get("date")
        time = request.form.get("time")

        email = session.get("email")
        if email:
            user = user_collection.find_one({"email": email})
            if user:
                user_collection.update_one(
                    {"email": email},
                    {"$set": {"reservation": {"date": date, "time": time, "No of people": people}}}
                )
                return jsonify(success=True, message="Reservation Successful")
            else:
                return jsonify(success=False, message="User not found"), 404
        else:
            return jsonify(success=False, message="User not logged in"), 401

    return jsonify(success=False, message="Invalid request method"), 405

@app.route('/')
def login():
    return render_template("Login.html")

@app.route('/address', methods=['POST'])
def address():
    if request.method == "POST":
        address = request.form.get('address')
        dno = request.form.get('dno')
        landmark = request.form.get('landmark')

        email = session.get("email")
        if email:
            user_collection.update_one(
                {"email": email},
                {"$set": {"address": {"address": address, "dno": dno, "landmark": landmark}}}
            )
            return redirect(url_for('home'))
        else:
            return render_template('cart.html')

    return render_template('cart.html')

@app.route('/login_validate', methods=['POST'])
def login_validate():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = user_collection.find_one({"email": email,"password":password})
        if user:
            session['email'] = email
            cart = user.get("cart", [])
            session['cart'] = cart
            return redirect(url_for('home'))
    
    return jsonify(success=False, message="Invalid credentials")

@app.route('/signup')
def signup():
    return render_template("SignUp.html")

@app.route('/signup_validate', methods=['POST'])
def signup_validate():
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('cpass')

        if password != confirm_password:
            return "Passwords do not match", 400

        existing_user = user_collection.find_one({"email": email})

        if existing_user:
            return "User already exists", 400

        
        new_user = {
            "name": name,
            "username": username,
            "email": email,
            "password":password,
            "cart": []
        }

        user_collection.insert_one(new_user)
        return redirect(url_for('login'))

    return render_template("SignUp.html")

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    item = request.json
    email = session.get('email')
    if not email:
        return jsonify(success=False, message="User not logged in"), 401

    user = user_collection.find_one({"email": email})
    if user:
        cart = user.get("cart", [])
        cart.append(item)
        user_collection.update_one(
            {"email": email},
            {"$set": {"cart": cart}}
        )
        session['cart'] = cart
        return jsonify(success=True)
    else:
        return jsonify(success=False, message="User not found"), 404

@app.route('/clear_cart', methods=['POST'])
def clear_cart():
    email = session.get('email')
    if not email:
        return jsonify(success=False, message="User not logged in"), 401

    user_collection.update_one(
        {"email": email},
        {"$set": {"cart": []}}
    )
    session['cart'] = []
    return jsonify(success=True)

@app.route('/remove_cart', methods=['POST'])
def remove_cart():
    item = request.json.get('name')  # Retrieve the name of the item to remove
    email = session.get('email')

    if not email:
        return jsonify(success=False, message="User not logged in"), 401

    try:
        user_collection.update_one(
            {"email": email},
            {"$pull": {"cart": {"name": item}}}
        )
        session['cart'] = [item for item in session.get('cart') if item['name'] != item]
        return jsonify(success=True,message="Item removed")
    except Exception as e:
        return jsonify(success=False, message=str(e)), 500




@app.route('/cart')
def cart():
    email = session.get('email')
    if email:
        user = user_collection.find_one({"email": email})
        if user:
            cart = user.get("cart", [])
            return render_template("cart.html", cart=cart)
    
    return redirect(url_for('login'))

@app.route('/save_address', methods=['POST'])
def save_address():
    address = request.json
    email = session.get('email')
    if email:
        user_collection.update_one(
            {"email": email},
            {"$set": {"address": address}}
        )
        return jsonify(success=True)
    return jsonify(success=False, message="User not logged in"), 401

@app.route('/process_payment', methods=['POST'])
def process_payment():
    email = session.get('email')
    cart_items = session.get('cart', [])

    if email and cart_items:
        user = user_collection.find_one({"email": email})
        if user:
            user_collection.update_one(
                {"email": email},
                {"$set": {"cart": cart_items}}
            )
            return jsonify(success=True, message="Cart updated successfully")
        else:
            return jsonify(success=False, message="User not found"), 404
    else:
        return jsonify(success=False, message="Invalid data provided"), 400

@app.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('cart', None)
    return redirect(url_for('login'))

@app.route('/fetch_cart')
def fetch_cart():
    email = session.get('email')
    if email:
        user = user_collection.find_one({"email": email})
        if user:
            cart = user.get("cart", [])
            return jsonify(success=True, cart=cart)
    
    return jsonify(success=False, message="User not logged in"), 401

# Admin Section

ADMIN_EMAIL = 'admin@12'
ADMIN_PASSWORD = 'a'

@app.route('/admin_login')
def admin_login():
    return render_template("admin_login.html")

@app.route('/admin_login_validate', methods=['POST'])
def admin_login_validate():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            session['admin'] = email
            return redirect(url_for('admin'))
    
    return "Invalid credentials", 403

@app.route('/admin')
def admin():
    if 'admin' in session:
        return render_template("admin.html")
    return redirect(url_for('admin_login'))

@app.route('/add_menu_item', methods=['POST'])
def add_menu_item():
    category = request.form.get('category')
    name = request.form.get('name')
    price = request.form.get('price')
    description = request.form.get('description')
    image = request.files['image']

    filename = None
    if image:
        filename = secure_filename(image.filename)
        image.save(os.path.join('static', filename))

    new_item = {
        "category": category,
        "name": name,
        "price": price,
        "description": description,
        "image": filename
    }

    menu_collection.insert_one(new_item)

    return redirect(url_for('show_menu'))

@app.route('/users')
def users():
    users_data = list(user_collection.find({}))
    return render_template('users.html', users=users_data)

@app.route('/user/<email>')
@app.route('/user/<email>')
def user_details(email):
    user = user_collection.find_one({"email": email})
    if user:
        cart = user.get('cart', [])
        total_price = sum(item['price'] for item in cart)
    else:
        cart = []
        total_price = 0
    
    return render_template('user_details.html', user=user, cart=cart, total_price=total_price)

if __name__ == '__main__':
    app.run(debug=True)
