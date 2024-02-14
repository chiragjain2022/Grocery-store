from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, DateField
from wtforms.validators import DataRequired, Length, Email

class AdminSignupForm(FlaskForm):
    firstName = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    lastName = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])


class UserSignupForm(FlaskForm):
    firstName = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    lastName = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])



class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])



class ResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])



class AddProduct(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    category = StringField('Category', validators=[DataRequired()])
    price = StringField('Price', validators=[DataRequired()])
    discount = StringField('Discount', validators=[DataRequired()])
    MFG_date = DateField('MFG_date', validators=[DataRequired(False)])
    status = StringField('Status', validators=[DataRequired()])
    stock = StringField('Stock', validators=[DataRequired()])
    unit = StringField('Unit', validators=[DataRequired()])



class AddCategory(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    status = StringField('Status', validators=[DataRequired(), Length(min=2, max=20)])
    image = FileField('Image', validators=[DataRequired()])


class AddCart(FlaskForm):
    quantity = StringField('Quantity', validators=[DataRequired()])


class AddUserDetail(FlaskForm):
    fullName = StringField('First Name', validators=[DataRequired()])
    mobileNumber = StringField('Mobile Number', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    zipCode = StringField('Zip Code', validators=[DataRequired()])


class AddBill(FlaskForm):
    fullName = StringField('First Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    zip = StringField('Zip Code', validators=[DataRequired()])
    paymentMethod = StringField('Payment Method', validators=[DataRequired()])
    promoCode = StringField('Promo Code')
    place_order = SubmitField('Place Order') 

class UpdateStatus(FlaskForm):
    status = StringField('Status', validators=[DataRequired()])


class SearchForm(FlaskForm):
    search_query = StringField("Search products", validators=[DataRequired()])


class PromoCode(FlaskForm):
    promoCode = StringField('Code', validators=[DataRequired()])