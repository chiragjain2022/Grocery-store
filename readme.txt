Grocery Store Flask App

Welcome to the Grocery Store Flask App! This application provides two main sections: one for users and the other for administrators. Users can add products from multiple categories to their cart, apply promo codes, place orders, and view their invoices. Administrators can access a dashboard to manage orders and perform CRUD operations on categories and products.

Table of Contents

- Features
- Installation
- Usage
- User Section
- Admin Section

Features

User Section

- Login, Signup and rest password
- Browse and add products from various categories to the shopping cart.
- Apply promo codes for discounts on orders.
- Place orders and view order invoices.

Admin Section

- Seperate Login, Signup and rest password for Admins
- Access an admin dashboard with insights on orders and income.
- Manage categories (Create, Read, Update, Delete operations).
- Manage products (Create, Read, Update, Delete operations).

Installation

1. Create a virtual environment:

   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

2. Install dependencies:

   pip install -r requirements.txt

3. Set up the database and configurations (database URI, secret keys, etc.) in config.py.

4. Run the application:

   flask run

Usage

Visit http://127.0.0.1:5000 in your browser to access the Grocery Store application.

User Section

1. Browse products by categories.
2. Add desired products to your cart.
3. Apply promo codes during checkout.
4. Place an order and view the invoice.
5. and many more things.

Admin Section

1. Access the admin dashboard by visiting /admin.
2. Monitor total income, orders, completed orders, and pending orders.
3. Perform CRUD operations on categories and products.
4. and many more things.


