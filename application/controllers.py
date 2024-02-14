from flask import current_app as app
from flask import render_template, request, redirect, url_for, flash, session
from flask_login import  login_user, login_required, current_user
from application.models import User, Category, Product, Order, Bill, Cart, OrderItem
from .helpers import calculate_total_price_with_delivery, rename_and_save_image
from .database import db
from flask_bcrypt import Bcrypt
from .forms import AdminSignupForm, LoginForm,PromoCode, UserSignupForm, ResetForm, AddProduct, SearchForm, AddCategory, AddCart, AddUserDetail, AddBill, UpdateStatus, SearchForm
from datetime import datetime

bcrypt = Bcrypt(app)

# ******************************** creating routes for the app  ********************************

@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    form = AddCart()
    allcategory = Category.query.filter_by(status='Active').all()
    allproduct = Product.query.filter_by(status='Active').all() 
    return render_template('index.html', allcategory=allcategory, allproduct=allproduct, form=form)

@app.route('/admin')
@login_required
def admin():
    allorders = Order.query.all()
    total_amount = 0
    total_orders = 0
    completed_orders = 0

    for order in allorders:
        if order.status == 'Completed':
            completed_orders += 1
        total_orders += 1
        total_amount += order.total_amount
    rest_orders = total_orders - completed_orders
    return render_template('admin.html', allorders=allorders, total_amount=total_amount, total_orders=total_orders, completed_orders=completed_orders, rest_orders=rest_orders)

# ******************************** Signup, Login and Logout routes  ********************************

@app.route('/user/signup',  methods=['GET', 'POST'])
def user_signup():

    form = UserSignupForm(request.form)

    if form.validate_on_submit():
        firstName = form.firstName.data
        lastName = form.lastName.data
        email = form.email.data
        password = form.password.data
        confirm_password = form.confirm_password.data

        email_exist = User.query.filter_by(email=email).first()

        if email_exist:
            flash('Email already exists', category='warning')
        elif confirm_password != confirm_password:
            flash('Passwords do not match', category='warning')
        else:

            hashed_password = bcrypt.generate_password_hash(
                password).decode('utf-8')

            user = User(firstName=firstName, lastName=lastName,
                        email=email, password=hashed_password, user_type='user')
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('user_signup.html', form=form)


@app.route('/admin/signup', methods=['GET', 'POST'])
def admin_signup():
    form = AdminSignupForm(request.form)

    if form.validate_on_submit():
        firstName = form.firstName.data
        lastName = form.lastName.data
        email = form.email.data
        password = form.password.data
        confirm_password = form.confirm_password.data

        email_exist = User.query.filter_by(email=email).first()

        if email_exist:
            flash('Email already exists', category='warning')
        elif password != confirm_password:
            flash('Passwords do not match', category='warning')
        else:
            hashed_password = bcrypt.generate_password_hash(
                password).decode('utf-8')

            user = User(firstName=firstName, lastName=lastName,
                        email=email, password=hashed_password, user_type='admin')
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('admin_signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            session['email'] = email
            if user.user_type == 'user':
                login_user(user)
                return redirect(url_for('home'))
            else:
                login_user(user)
                return redirect(url_for('admin'))
        elif not user:
            flash("Login Unsuccessful. That email does not exist, please try again.")
            return redirect(url_for('login'))
        else:
            flash('Login Unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', form=form)


@app.route('/reset', methods=['GET', 'POST'])
def reset_password():

    form = ResetForm(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = form.password.data
        new_password = form.new_password.data

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            hashed_password = bcrypt.generate_password_hash(
                new_password).decode('utf-8')
            user.password = hashed_password
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    session.pop('email', None)
    return redirect(url_for('login'))

# ******************************** Signup, Login and Logout routes END ********************************


# ******************************** Search routes  ********************************

@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        search_query = form.search_query.data
        allproduct = Product.query.all()
        search_results = [product for product in allproduct if search_query.lower() in product.name.lower()]
        return render_template('search.html', form=form, results=search_results, search_query=search_query)
    return redirect(url_for('home'))



# ******************************** C R U D Operations  ********************************

# ******************************** All Add Routes (Create) ********************************

@app.route('/admin/add/product', methods=['GET', 'POST'])
def add_product():

    allcategory = Category.query.all()
    form = AddProduct()

    if form.validate_on_submit():
        name = form.name.data
        category = int(form.category.data)
        price = form.price.data
        discount = form.discount.data
        MFG_date= request.form.get('MFG_date')
        EXP_date= request.form.get('EXP_date')
        image = request.files.get("image")
        stock = form.stock.data
        status = form.status.data
        unit = form.unit.data
        
        MFG_date_str = request.form.get('MFG_date')
        if MFG_date_str is not None and MFG_date_str.strip() != '':
            MFG_date = datetime.strptime(MFG_date_str, '%Y-%m-%d').date()
        else:
            MFG_date = None 

        EXP_date_str = request.form.get('EXP_date')
        if EXP_date_str is not None and EXP_date_str.strip() != '':
            EXP_date = datetime.strptime(EXP_date_str, '%Y-%m-%d').date()
        else:
            EXP_date = None 

        product = Product(name=name, price=price, discount=discount, MFG_date=MFG_date , EXP_date=EXP_date ,stock=stock, status=status, category_id=category, unit=unit)
        
        if image:
           product.image = rename_and_save_image(image, name, folder= app.config['PRODUCT_UPLOAD_FOLDER'])
        
        db.session.add(product)
        db.session.commit()

        return redirect(url_for('view_product'))
    return render_template('add_product.html', form=form, allcategory=allcategory)


@app.route('/admin/add/category', methods=['GET', 'POST'])
def add_category():
    form = AddCategory()

    if request.method == "POST" and form.validate_on_submit():
        name = form.name.data
        status = form.status.data
        image = request.files.get("image")
        category = Category(name=name, status=status)
        if image:
           category.image = rename_and_save_image(image, name, folder= app.config['CATEGORY_UPLOAD_FOLDER'])

        db.session.add(category)
        db.session.commit()

        return redirect(url_for('view_category'))
    return render_template('add_category.html', form=form)

# ******************************** All View Routes (Read) ********************************

@app.route('/admin/view/category', methods=['GET', 'POST'])
def view_category():
    allcategory = Category.query.all()
    return render_template('view_category.html', allcategory=allcategory)

@app.route('/admin/view/products', methods=['GET', 'POST'])
def view_product():
    allproduct = Product.query.all()
    return render_template('view_products.html', allproduct=allproduct)

@app.route('/admin/view/product/<int:id>', methods=['GET', 'POST'])
def product_view(id):
    product = Product.query.filter_by(id=id).first()
    return render_template('product_view.html', product=product)

# ******************************** All Edit Routes (Update) ********************************

@app.route('/admin/edit/category/<int:id>', methods=['GET', 'POST'])
def edit_category(id):
    form = AddCategory()
    if request.method == "POST":
        name = request.form.get("name")
        status = request.form.get("status")
        image = request.files.get("image")
        category = Category.query.filter_by(id=id).first()
        category.name = name
        category.status = status
        if image:
            category.image = rename_and_save_image(image, name, folder= app.config['CATEGORY_UPLOAD_FOLDER'])
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('view_category'))
    category = Category.query.filter_by(id=id).first()
    return render_template('edit_category.html', form=form, category=category)

@app.route('/admin/edit/product/<int:id>', methods=['GET', 'POST'])
def product_edit(id):
    allcategory = Category.query.all()
    form = AddProduct()
    if request.method == "POST":
        name = form.name.data
        category = (form.category.data)
        price = form.price.data
        discount = form.discount.data
        MFG_date= request.form.get('MFG_date')
        EXP_date= request.form.get('EXP_date')
        image = request.files.get("image")
        stock = form.stock.data
        status = form.status.data
        unit = form.unit.data
        
        MFG_date_str = request.form.get('MFG_date')
        if MFG_date_str is not None and MFG_date_str.strip() != '':
            MFG_date = datetime.strptime(MFG_date_str, '%Y-%m-%d').date()
        else:
            MFG_date = None 

        EXP_date_str = request.form.get('EXP_date')
        if EXP_date_str is not None and EXP_date_str.strip() != '':
            EXP_date = datetime.strptime(EXP_date_str, '%Y-%m-%d').date()
        else:
            EXP_date = None 

        product = Product.query.filter_by(id=id).first()
        product.name = name 
        product.price = price 
        product.discount = discount 
        product.MFG_date = MFG_date  
        product.EXP_date = EXP_date 
        product.stock = stock 
        product.status = status 
        product.category_id = category 
        product.unit = unit
        if image:
           product.image = rename_and_save_image(image, name, folder= app.config['PRODUCT_UPLOAD_FOLDER'])
        
        db.session.add(product)
        db.session.commit()

        return redirect(url_for('view_product'))
    product = Product.query.filter_by(id=id).first()
    return render_template('edit_product.html', product=product, form=form, allcategory=allcategory)

# ******************************** All Delete Routes (Delete) ********************************

@app.route('/admin/delete/category/<int:id>', methods=['GET', 'POST'])
def delete_category(id):
    category = Category.query.filter_by(id=id).first()
    db.session.delete(category)
    db.session.commit()
    allcategory = Category.query.all()
    return render_template('view_category.html', allcategory=allcategory)

@app.route('/admin/delete/product/<int:id>', methods=['GET', 'POST'])
def delete_product(id):
    product = Product.query.filter_by(id=id).first()
    db.session.delete(product)
    db.session.commit()
    allproduct = Product.query.all()
    return render_template('view_products.html', allproduct=allproduct)

# ******************************** All User Routes (Read) ********************************

@app.route('/user/profile' , methods=['GET', 'POST'])
@login_required
def profile():
    form = AddUserDetail()
    user_id = current_user.id
    user = User.query.filter_by(id=user_id).first()
    allorders = Order.query.filter_by(user_id=user_id).all()
    return render_template('user_profile.html', user=user, form=form, allorders=allorders)

# ******************************** All Cart Functions ********************************

@app.route('/products/<int:id>', methods=['GET', 'POST'])
def products(id):
    form = AddCart()
    category = Category.query.filter_by(id=id).first()
    products = Product.query.filter_by(category_id=id).all()
    return render_template('products.html', products=products, category=category, form=form)

@app.route('/cart', methods=['GET', 'POST'])
@login_required
def cart():
    form = PromoCode()
    user_id = current_user.id
    cart_items = Cart.query.filter_by(user_id=user_id).all()
    total_price_with_delivery= calculate_total_price_with_delivery(cart_items)[0]
    promoCode = request.form.get('promoCode')
    total_price = 0
    total_saving = 0
    total_price_with_discount = None
    for cart_item in cart_items:
        total_price += cart_item.product.discount * cart_item.quantity
        total_saving += (cart_item.product.price - cart_item.product.discount) * cart_item.quantity

    has_previous_orders = Order.query.filter_by(user_id=current_user.id).first() is not None
    total_price_with_discount = None
    if form.validate_on_submit():
        if not has_previous_orders:
            if promoCode == 'FIRSTORDER20':
                discount = 0.2
                for cart_item in cart_items:
                    cart_item.promocode = "Yes"
                    db.session.commit()
                total_price_with_discount = total_price_with_delivery - (total_price_with_delivery * discount)
            else:
                flash('Invalid promo code', 'danger')
        else:
            flash('You have already placed an order', 'danger')

    # Apply delivery charges if the total price is less than 100
    delivery_charge = 50 if total_price < 100 else 0
    total_price_with_delivery = total_price + delivery_charge
    return render_template('cart.html', cart_items=cart_items,total_price=total_price, delivery_charge=delivery_charge, total_price_with_delivery=total_price_with_delivery, total_saving=total_saving, total_price_with_discount=total_price_with_discount, form=form)

@app.route('/update_cart_item/<int:item_id>', methods=['POST'])
def update_cart_item(item_id):
    new_quantity = int(request.form['quantity'])

    cart_item = Cart.query.get(item_id)
    if cart_item:
        cart_item.quantity = new_quantity
        db.session.commit()
    
    return redirect(url_for('cart'))

@app.route('/add_to_cart', methods=['GET', 'POST'])
@login_required
def add_to_cart():
    user_id = current_user.id
    product_id = request.form['product_id']
    quantity = int(request.form['quantity'])

    cart_item = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()

    if cart_item:
        cart_item.quantity = quantity
    else:
        cart_item = Cart(user_id=user_id, product_id=product_id, quantity=quantity)
        db.session.add(cart_item)

    db.session.commit()
    return redirect(url_for('home'))

@app.route('/cart/<int:id>', methods=['GET', 'POST'])
def delete_cart_item(id):
    cart = Cart.query.filter_by(id=id).first()
    db.session.delete(cart)
    db.session.commit()
    cart_items = Cart.query.all()
    return render_template('cart.html', cart_items=cart_items)

# ******************************** All Checkout and Invoice Functions ********************************

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    form = AddBill()
    user = current_user.id
    cart_items = Cart.query.filter_by(user_id=user).all()
    total_price_with_delivery, delivery_charge, total_price, total_saving = calculate_total_price_with_delivery(cart_items) 
    for cart_item in cart_items:
        if cart_item.promocode == "Yes":
            total_price_with_delivery = total_price_with_delivery - (total_price_with_delivery * 0.2)
            total_saving = total_saving + (total_price_with_delivery * 0.2)
            break
            
    if form.validate_on_submit():
        if 'place_order' in request.form:
            fullName = form.fullName.data
            phone = form.phone.data
            email = form.email.data
            address = form.address.data
            city = form.city.data
            zip = form.zip.data
            paymentMethod = request.form['paymentMethod']

            bill = Bill(user_id=user, fullname=fullName, phone=phone, email=email, address=address, city=city, zip=zip, payment_method=paymentMethod)
            db.session.add(bill)
            db.session.commit()

            order_date = datetime.utcnow()
            order = Order( user_id=user, bill_id=bill.id, order_date=order_date, total_amount=total_price_with_delivery, status='pending')
            db.session.add(order)
            db.session.commit()

            for cart_item in cart_items:
                product = Product.query.get(cart_item.product_id)
                if product and product.stock >= cart_item.quantity:
                    product.stock -= cart_item.quantity
                    db.session.commit()
                else:
                    flash('Insufficient stock for {}'.format(product.name), 'danger')
                    return redirect(url_for('checkout'))
                order_item = OrderItem(order_id=order.id, product_id=cart_item.product_id, quantity=cart_item.quantity ,price=(cart_item.product.discount*cart_item.quantity))
                db.session.add(order_item)
                db.session.commit()

            Cart.query.delete()
            db.session.commit()

        return redirect(url_for('order_placed'))
    return render_template('checkout.html', form=form ,cart_items=cart_items,total_price=total_price, delivery_charge=delivery_charge, total_price_with_delivery=total_price_with_delivery, total_saving=total_saving)

@app.route('/order_placed')
@login_required
def order_placed():
    order = Order.query.order_by(Order.id.desc()).first()
    order_id = order.id if order else None
    return render_template('order_placed.html', order_id=order_id)

@app.route('/invoice')
@login_required
def invoice():
    bill_detail = Bill.query.order_by(Bill.id.desc()).first()
    bill_details = Bill.query.filter_by(id=bill_detail.id).all()
    order = Order.query.order_by(Order.id.desc()).first()
    order_id = order.id 
    order_date = order.order_date 
    date = order_date.strftime('%Y-%m-%d')
    total_amount = order.total_amount 
    delivery_charge = 50 if total_amount < 100 else 0
    allitems = OrderItem.query.filter_by(order_id=order_id).all()
    return render_template('invoice.html', bill_details=bill_details, order_id=order_id, date=date, allitems=allitems, total_amount=total_amount, delivery_charge=delivery_charge)

@app.route('/user/invoice/<int:id>')
@login_required
def invoices(id):
    bill_details = Bill.query.filter_by(id=id).all()
    order = Order.query.filter_by(bill_id=id).first()
    order_id = order.id 
    order_date = order.order_date 
    date = order_date.strftime('%Y-%m-%d')
    total_amount = order.total_amount 
    delivery_charge = 50 if total_amount < 100 else 0
    allitems = OrderItem.query.filter_by(order_id=order_id).all()
    return render_template('invoice.html', bill_details=bill_details, order_id=order_id, date=date, allitems=allitems, total_amount=total_amount, delivery_charge=delivery_charge)


# ******************************** All Admin Functions ********************************

@app.route('/admin/coustomers', methods=['GET', 'POST'])
@login_required
def coustomers():
    allcustomer = User.query.filter_by(user_type='user').all()
    return render_template('coustomers.html', allcustomer=allcustomer)


@app.route('/admin/orders')
@login_required
def orders():
    allorders = Order.query.all()
    return render_template('orders.html', allorders=allorders)


@app.route('/admin/order/<int:id>', methods=['GET', 'POST'])
@login_required
def order(id):
    form = UpdateStatus()

    if form.validate_on_submit():
        status = request.form['status']
        order = Order.query.filter_by(id=id).first()
        order.status = status
        db.session.add(order)
        db.session.commit()
        return redirect(url_for('orders'))
    order = Order.query.filter_by(id=id).first()
    order_id = order.id
    order_date = order.order_date 
    bill = Bill.query.filter_by(id=order.bill_id).first()
    address = bill.address
    city = bill.city
    zip = bill.zip
    date = order_date.strftime('%Y-%m-%d')
    total_amount = order.total_amount 
    delivery_charge = 50 if total_amount < 100 else 0
    allitems = OrderItem.query.filter_by(order_id=order_id).all()
    return render_template('edit_order.html', order_id=order_id, date=date, allitems=allitems, total_amount=total_amount, delivery_charge=delivery_charge, address=address, city=city, zip=zip, form=form, order=order)

# main driver function
if __name__ == '__main__':
    app.run(debug=True)
