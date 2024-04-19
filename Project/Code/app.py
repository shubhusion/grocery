# -----------------------------------------------------IMPORTS--------------------------------------------------------------------------------
import datetime
import json
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    make_response,jsonify
)
from flask_login import (
    LoginManager,
    login_required,
    login_user,
    logout_user,
    current_user,
)
from Database import db , User, Section, Product, Cart, Order, OrderProduct
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from werkzeug.exceptions import HTTPException

# ----------------------------------------------------INITIALISATION--------------------------------------------------------------------------
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite3"
app.secret_key = "thisismysecretkey"
login_manager = LoginManager()
api = Api(app)  # Setting up Api for flask

with app.app_context():
    login_manager.init_app(app)
    db.init_app(app)
    db.create_all()
    # Check if the default user already exists
    existing_user = User.query.filter_by(email="shubham@gmail.com").first()

    if existing_user is None:
        # If the default user doesn't exist, create it
        adminuser = User(
            username="shubham2703",
            name="shubham",
            password="shubham",
            email="shubham@gmail.com",
            admin=1,
        )
        db.session.add(adminuser)
        db.session.commit()
        print("Default user added successfully.")
    else:
        print("Default user already exists.")

login_manager.login_view = "user_login"


@login_manager.user_loader
def loaduser(userid):  # fetched the data of user from Database which will now be considered as current user
    return User.query.get(userid)


# ----------------------------------------------------------ROUTES CODE STARTS HERE------------------------------------------------------------


@app.route("/")  # route for Main Landing Page
def Home():
    """
    Route for Main Landing Page.

    Returns:
        str: Rendered HTML template for the landing page.
    """
    return render_template("index.html", section=Section.query.all())


@app.route("/logout")  # route for Logout Page
def logout():
    """
    Route for Logout Page.

    Returns:
        redirect: Redirects to the main landing page.
    """
    logout_user()
    return redirect(url_for("Home"))


@app.route("/register", methods=["GET", "POST"])  # route for Login Page
def register():
    """
    Route for user registration.

    Returns:
        redirect: Redirects to the login page after successful registration.
        render_template: Renders the registration page template for GET request.
    """
    if request.method == "POST":
        uname = request.form["username"]
        email = request.form["email"]
        name = request.form["name"]
        password = request.form["password"]
        newuser = User(
            username=uname, name=name, password=password, email=email, admin=False
        )
        db.session.add(newuser)
        db.session.commit()
        flash("User registration successful", "Success")
        return redirect(url_for("user_login"))
    return render_template("register.html")


# ------------------------------------------------ROUTES FOR ADMIN SECTION-----------------------------------------------------------------


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        uname = request.form["username"]
        password = request.form["password"]
        user = User.query.get(uname)
        if not user:
            flash("User Not found", "Error")
        else:
            if user.password == password:
                if user.admin:
                    login_user(user)
                    return redirect(url_for("admin"))
                else:
                    flash("Not an Admin Account", "error")
            else:
                flash(" Incorrect Password! Try Again", "error")
    return render_template("login.html", admin=True)


@app.route("/admin")  # Route for admin dashboard
@login_required
def admin():
    if current_user.admin:
        return render_template("admin_dashboard.html", section=Section.query.all())
    else:
        flash("Not an Admin Account. User an admin account to Login", "warning")
        return redirect(url_for("user_login"))


# --------------------------------------------------ROUTES FOR CATEGORY IN ADMIN SECTION --------------------------------------------------------


@app.route(
    "/admin/section/create", methods=["GET", "POST"]
)  # route for Creating New Category
@login_required
def add_section():
    if request.method == "POST":
        # Retrieve form data
        secname = request.form["section_name"]
        sec_obj = Section(name=secname)
        db.session.add(sec_obj)
        db.session.commit()
        flash("Section added in Admin Section", "success")
        return redirect(url_for("admin"))
    return render_template("add_section.html")


@app.route(
    "/admin/section/update/<int:id>", methods=["GET", "POST"]
)  # route for updating existing Category
@login_required
def update_section(id):
    sec = Section.query.filter_by(id=id).first()
    if request.method == "POST":
        sec = Section.query.filter_by(id=id).first()
        sec.name = request.form.get("name")
        db.session.commit()
        flash("Section Updated in Admin Section", "success")
        return redirect(url_for("admin"))
    return render_template("update_section.html", sec=sec)


@app.route(
    "/admin/section/delete/<int:id>", methods=["GET", "POST"]
)  # route for deleting New Category
@login_required
def delete_section(id):
    sec = Section.query.filter_by(id=id).first()
    db.session.delete(sec)
    db.session.commit()
    return redirect(url_for("admin"))


@app.route("/admin/promotion")
@login_required
def view_promotion():
    pass


@app.route("/admin/promotion/new")
@login_required
def insert_promotion():
    pass


# --------------------------------------------------ROUTES FOR PRODUCT---------------------------------------------------------


@app.route(
    "/admin/product/create", methods=["GET", "POST"]
)  # route for Creating New Product
@login_required
def add_product():
    if request.method == "POST":
        # Retrieve form data
        prdname = request.form["product_name"]
        # manufacture_date = request.form["manufacture_date"]
        # expiry_date = request.form["expiry_date"]
        price = request.form["price"]
        unit = request.form["unit"]
        quantity = request.form["quantity"]
        section_id = request.form["section_id"]
        # if not manufacture_date:
        #     manufacture_date = None
        # if not expiry_date:
        #     expiry_date = None
        prd_obj = Product(
            name=prdname,
            # manufacture_date=manufacture_date,
            # expiry_date=expiry_date,
            price=price,
            unit=unit,
            quantity=quantity,
        )
        prd_obj.section_id = section_id
        db.session.add(prd_obj)
        db.session.commit()
        flash(" Product Created in Admin Section", "success")
        return redirect(url_for("admin"))
    return render_template("add_product.html", secs=Section.query.all())


@app.route(
    "/admin/product/update/<int:id>", methods=["GET", "POST"]
)  # route for Creating New Product
@login_required
def update_product(id):
    prd = Product.query.filter_by(id=id).first()
    if request.method == "POST":
        prd = Product.query.filter_by(id=id).first()
        prd.name = request.form.get("product_name")
        # prd.manufacture_date = request.form.get("manufacture_date")
        # prd.expiry_date = request.form.get("expiry_date")
        prd.price = request.form.get("price")
        prd.unit = request.form.get("unit")
        prd.quantity = request.form.get("quantity")
        # if not request.form.get("manufacture_date"):
        #     prd.manufacture_date = None
        # if not request.form.get("expiry_date"):
        #     prd.expiry_date = None
        db.session.commit()
        flash(" Product Updated in Admin Section", "success")
        return redirect(url_for("admin"))
    return render_template("update_product.html", prd=prd)


@app.route("/admin/product/delete/<int:id>")  # route for Creating New
@login_required
def delete_product(id):
    prd = Product.query.filter_by(id=id).first()
    db.session.delete(prd)
    db.session.commit()
    flash(" Product Deleted from Admin Section")
    return redirect(url_for("admin"))


# ------------------------------------------------------USER SECTION-----------------------------------------------------------------


@app.route("/user/login", methods=["GET", "POST"])  # route for Login Page
def user_login():
    if request.method == "POST":
        uname = request.form["username"]
        password = request.form["password"]
        user = User.query.get(uname)
        if not user:
            flash("User Not found")
        else:
            if user.password == password:
                login_user(user)
                return redirect(url_for("view_sections"))
            else:
                flash(" Incorrect Password! Try Again", "error")
    return render_template("login.html")


@app.route("/user")  # User Dashboard
@login_required
def view_sections():
    if request.args.get("q"):
        if request.args.get("by") == "0":
            return render_template(
                "user_dashboard.html",
                section=Section.query.filter(
                    Section.name.like(f"%{request.args.get('q')}%")
                ),
                p=False,
            )
        else:
            return render_template(
                "user_dashboard.html",
                product=Product.query.filter(
                    Product.name.like(f"%{request.args.get('q')}%")
                ),
                p=True,
            )
    return render_template("user_dashboard.html", section=Section.query.all(), p=False)


# ------------------------------------------------------ROUTES FOR SHOPPING CART (USER) -----------------------------------------------------------------


@app.route(
    "/user/cart/view"
)  # Shows the items currently added to the user's shopping cart.
@login_required
def view_cart():
    return render_template(
        "view_cart.html",
        cart=Cart.query.filter_by(user_id=current_user.username),
        section=Section.query.all(),
    )


@app.route(
    "/user/cart/add/<int:id>"
)  # Adds the product with ID 123 to the user's cart.
@login_required
def addtocart(id):
    prd = Product.query.get(id)
    if not prd:
        flash("Product Not Found", "info")
        return redirect(url_for("view_sections"))
    else:
        if prd.quantity < 1:
            flash("Product Out of Stock", "info")
            return redirect(url_for("view_sections"))
        productexist = Cart.query.get((current_user.username, id))
        if productexist:
            productexist.quantity += 1
            db.session.commit()
        else:
            newobj = Cart(product_id=prd.id, quantity=1)
            current_user.cart.append(newobj)
            db.session.commit()
            flash("Product Added to Cart", "success")
        return redirect(url_for("view_sections"))


@app.route(
    "/user/cart/remove/<int:id>"
)  # Removes the product with ID 123 from the user's cart.
@login_required
def removefromcart(id):
    prd = Product.query.get(id)
    if not prd:
        flash("Product Not Found", "info")
        return redirect(url_for("view_sections"))
    else:
        Car = Cart.query.get((current_user.username, id))
        if not Car:
            flash("Product Not in Cart", "info")
        else:
            db.session.delete(Car)
            db.session.commit()
            flash("Product Deleted from Cart", "success")
    return redirect(url_for("view_sections"))


@app.route(
    "/user/cart/incr/<int:id>"
)  # increases the quantity of Product with the Specified Product id
def incrincart(id):
    prd = Product.query.get(id)
    if not prd:
        flash("Product Not Found in Cart")
        return redirect(url_for("view_sections"))
    else:
        if prd.quantity < 1:
            flash("Product Out of Stock", "info")
        Car = Cart.query.get((current_user.username, id))
        if not Car:
            flash("Product Not in Cart", "info")
        else:
            if Car.quantity is not None:
                Car.quantity = Car.quantity + 1

            db.session.commit()
            flash("Product Quantity Increase in Cart", "success")
    return redirect(url_for("view_sections"))


@app.route(
    "/user/cart/decr/<int:id>"
)  # decreases the quantity of Product with the Specified Product id
@login_required
def decrincart(id):
    prd = Product.query.get(id)
    if not prd:
        flash("Product Not Found in Cart", "info")
        return redirect(url_for("view_sections"))
    else:
        Car = Cart.query.get((current_user.username, id))
        if not Car:
            flash("Product Not in Cart")
        else:
            if Car.quantity is not None:
                Car.quantity = Car.quantity - 1

            db.session.commit()
            flash("Product Quantity Decrease in Cart", "success")
    return redirect(url_for("view_sections"))


@app.route("/user/Order")  # View the Order
@login_required
def Orderprds():
    return render_template(
        "orders.html",
        orders=Order.query.filter_by(user_id=current_user.username),
        section=Section.query.all(),
    )


@app.route("/checkout")  # Proceeds to the checkout process.
@login_required
def checkout():
    cart = current_user.cart
    if not cart:
        flash("Cart is Empty", "info")
        return redirect(url_for("view_cart"))
    ord = Order(user_id=current_user.username, order_date=datetime.datetime.today())
    db.session.add(ord)
    for p in cart:
        ordprd = OrderProduct(
            product_id=p.product_id, quantity=p.quantity, rate=p.product.price
        )
        ord.order_to_product.append(ordprd)
        db.session.delete(p)
    db.session.commit()
    flash("Order Placed Successfully", "success")
    return redirect(url_for("Orderprds"))


# ---------------------------------------------------------- ROUTES CODE END HERE -----------------------------------------------------------


# ------------------------------------------------------ API -----------------------------------------------------------------------------
@app.route("/api/register", methods=["POST"])
def api_register():
    if request.method == "POST":
        try:
            data = request.json
            uname = data.get("username")
            email = data.get("email")
            name = data.get("name")
            password = data.get("password")

            if not uname or not email or not name or not password:
                return jsonify({"error": "All fields are required"}), 400

            if User.query.filter_by(username=uname).first():
                return jsonify({"error": "Username already exists"}), 409

            new_user = User(
                username=uname, name=name, password=password, email=email, admin=False
            )
            db.session.add(new_user)
            db.session.commit()

            return jsonify({"message": "User registration successful"}), 201
        except KeyError as e:
            return jsonify({"error": f"Missing key: {e}"}), 400
    return jsonify({"message": "Hello"})


@app.route("/api/login", methods=["POST"])
def api_login():
    if request.method == "POST":
        try:
            data = request.json
            uname = data.get("username")
            password = data.get("password")

            if not uname or not password:
                return jsonify({"error": "Username and password are required"}), 400
            user = User.query.get(uname)
            if not user:
                return jsonify({"error": "User not found"}), 404
            if user.password == password:
                login_user(user)
                return jsonify({"message": "Login successful"}), 200
            else:
                return jsonify({"error": "Incorrect password"}), 401
        except ValueError:
            return jsonify({"error": "Invalid JSON data"}), 400
    return jsonify({"hi": "hello"})


# Get all categories
@app.route("/api/section", methods=["GET"])
def get_section():
    sec = Section.query.all()
    section_list = [{"id": section.id, "name": section.name} for section in sec]
    return jsonify({"section": section_list})


@app.route("/api/sections/<int:section_id>/products", methods=["GET"])
def get_products_by_category(section_id):
    sec = Section.query.filter_by(id=section_id).first()
    if sec:
        products = [
            {
                "id": product.id,
                "name": product.name,
                "Manufacture_date": product.manufacture_date,
                "Expiry_date": product.expiry_date,
                "unit": product.unit,
                "Price_per_unit": product.price,
                "quantity": product.quantity,
            }
            for product in sec.products
        ]
        return jsonify({"products": products})
    return jsonify({"message": "Category not found"}), 404


# ------------------------------------------------------- APIs Using Flask Restful-----------------------------------------------------------


# Common Errors
class NotFoundError(HTTPException):
    def __init__(self, status_code):
        self.response = make_response("", status_code)


class InternalServerError(HTTPException):
    def __init__(self, status_code):
        self.response = make_response("", status_code)


class ExistsError(HTTPException):
    def __init__(self, status_code):
        self.response = make_response("", status_code)


class NotExistsError(HTTPException):
    def __init__(self, status_code):
        self.response = make_response("", status_code)


class BuisnessValidationError(HTTPException):
    def __init__(self, status_code, error_code, error_message):
        message = {"error_code": error_code, "error_message": error_message}
        self.response = make_response(json.dumps(message), status_code)


# -----------------------------------------------------------SECTION API CODE STARTS HERE------------------------------------------------------
# SECTIONAPI
output_section = {
    "id": fields.Integer,
    "name": fields.String,
}

section_parser = reqparse.RequestParser()
section_parser.add_argument("name")


class sectionAPI(Resource):
    @marshal_with(output_section)
    def get(self, id):
        try:
            section_obj = Section.query.get(int(id))
            if section_obj:
                return section_obj
            else:
                raise NotFoundError(status_code=404)
        except NotFoundError as nfe:
            raise nfe
        except Exception as e:
            raise InternalServerError(status_code=500)

    @marshal_with(output_section)
    def put(self, id):
        try:
            args = section_parser.parse_args()
            section_name = args.get("name", None)
            if section_name is None:
                raise BuisnessValidationError(
                    status_code=400,
                    error_code="SECTION001",
                    error_message="Section Name is required",
                )
            section_obj = Section.query.filter_by(id=id).first()
            if section_obj:
                section_obj.name = section_name
                db.session.commit()
                updated_section = Section.query.filter_by(id=id).first()
                return updated_section, 200
            else:
                raise NotExistsError(status_code=404)

        except BuisnessValidationError as bve:
            raise bve
        except NotExistsError as nee:
            raise nee
        except Exception as e:
            raise InternalServerError(status_code=500)

    def delete(self, id):
        try:
            section_obj = Section.query.get(int(id))
            if section_obj:
                db.session.delete(section_obj)
                db.session.commit()
                return "", 200
            else:
                raise NotFoundError(status_code=404)
        except NotFoundError as nfe:
            raise nfe
        except Exception as e:
            raise InternalServerError(status_code=500)

    @marshal_with(output_section)
    def post(self):
        # try:
        args = section_parser.parse_args()
        section_name = args.get("name", None)
        if section_name is None:
            raise BuisnessValidationError(
                status_code=400,
                error_code="SECTION001",
                error_message="Section Name is required",
            )
        else:
            new_section = Section(name=section_name)
            db.session.add(new_section)
            db.session.commit()
            return new_section, 201

    # except BuisnessValidationError as bve:
    #     raise bve
    # except ExistsError as ee:
    #     raise ee
    # except Exception as e:
    #     raise InternalServerError(status_code=500)


api.add_resource(sectionAPI, "/api/admin/section", "/api/admin/section/<int:id>")

# -----------------------------------------------------------SECTION API CODE ENDS HERE------------------------------------------------------

# -----------------------------------------------------------PRODUCT API CODE STARTS HERE------------------------------------------------------

output_product = {
    "id": fields.Integer,
    "name": fields.String,
    "manufacture_date": fields.DateTime,
    "expiry_date": fields.DateTime,
    "unit": fields.String,
    "price": fields.Integer,
    "section_id": fields.Integer,
}

product_parser = reqparse.RequestParser()
product_parser.add_argument("name")
product_parser.add_argument("manufacture_date")
product_parser.add_argument("expiry_date")
product_parser.add_argument("unit")
product_parser.add_argument("price")
product_parser.add_argument("quantity")
product_parser.add_argument("section_id")


class productAPI(Resource):
    @marshal_with(output_product)
    def get(self, id):
        try:
            product_obj = Product.query.get(int(id))
            if product_obj:
                return product_obj
            else:
                raise NotFoundError(status_code=404)
        except NotFoundError as nfe:
            raise nfe
        except Exception as e:
            raise InternalServerError(status_code=500)

    @marshal_with(output_product)
    def put(self, id):
        try:
            args = product_parser.parse_args()
            name = args.get("name", None)
            manufacture_date = args.get("manufacture_date", None)
            expiry_date = args.get("expiry_date", None)
            unit = args.get("unit", None)
            print(unit)
            price = args.get("price", None)
            quantity = args.get("quantity", None)
            section_id = args.get("section_id", None)
            if name is None:
                raise BuisnessValidationError(
                    status_code=400,
                    error_code="PRODUCT001",
                    error_message="Product Name is required",
                )
            if unit is None:
                raise BuisnessValidationError(
                    status_code=400,
                    error_code="PRODUCT002",
                    error_message="Product Unit is required",
                )
            if price is None:
                raise BuisnessValidationError(
                    status_code=400,
                    error_code="PRODUCT003",
                    error_message="Product Price is required",
                )
            if quantity is None:
                raise BuisnessValidationError(
                    status_code=400,
                    error_code="PRODUCT004",
                    error_message="Product quantity is required",
                )
            if section_id is None:
                raise BuisnessValidationError(
                    status_code=400,
                    error_code="PRODUCT004",
                    error_message="Product section_id is required",
                )

            product_obj = Product.query.filter_by(id=id).first()
            if product_obj:
                product_obj.name = name
                product_obj.manufacture_date = manufacture_date
                product_obj.expiry_date = expiry_date
                product_obj.unit = unit
                product_obj.price = price
                product_obj.quantity = quantity
                product_obj.section_id = section_id
                db.session.commit()
                updated_product = Product.query.filter_by(id=id).first()
                return updated_product, 200
            else:
                raise NotExistsError(status_code=404)

        except BuisnessValidationError as bve:
            raise bve
        except NotExistsError as nee:
            raise nee
        except Exception as e:
            raise InternalServerError(status_code=500)

    def delete(self, id):
        try:
            product_obj = Product.query.get(int(id))
            if product_obj:
                db.session.delete(product_obj)
                db.session.commit()
                return "", 200
            else:
                raise NotFoundError(status_code=404)
        except NotFoundError as nfe:
            raise nfe
        except Exception as e:
            raise InternalServerError(status_code=500)

    @marshal_with(output_product)
    def post(self):
        # try:
        args = product_parser.parse_args()
        name = args.get("name", None)
        manufacture_date = args.get("manufacture_date", None)
        expiry_date = args.get("expiry_date", None)
        unit = args.get("unit", None)
        price = args.get("price", None)
        quantity = args.get("quantity", None)
        section_id = args.get("section_id", None)
        if name is None:
            raise BuisnessValidationError(
                status_code=400,
                error_code="PRODUCT001",
                error_message="Product Name is required",
            )
        if unit is None:
            raise BuisnessValidationError(
                status_code=400,
                error_code="PRODUCT002",
                error_message="Product Unit is required",
            )
        if price is None:
            raise BuisnessValidationError(
                status_code=400,
                error_code="PRODUCT003",
                error_message="Product Price is required",
            )
        if quantity is None:
            raise BuisnessValidationError(
                status_code=400,
                error_code="PRODUCT004",
                error_message="Product quantity is required",
            )
        if section_id is None:
            raise BuisnessValidationError(
                status_code=400,
                error_code="PRODUCT005",
                error_message="Product section_id is required",
            )

        new_product = Product(
            name=name,
            manufacture_date=manufacture_date,
            expiry_date=expiry_date,
            unit=unit,
            price=price,
            quantity=quantity,
            section_id=section_id,
        )
        db.session.add(new_product)
        db.session.commit()
        return new_product, 201

    # except BuisnessValidationError as bve:
    #     raise bve
    # except ExistsError as ee:
    #     raise ee
    # except Exception as e:
    #     raise InternalServerError(status_code=500)


api.add_resource(productAPI, "/api/admin/product", "/api/admin/product/<int:id>")

# ------------------------------------------------------ RUN CALL ---------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
