from flask import render_template, request, redirect, url_for, flash, session
import email_validator
from shop import app, db, bcrypt
from .forms import RegistrationForm, LoginForms
from .models import User
from shop .products .models import Addproduct, Brand, Category
import sqlite3
import os


@app.route('/admin')
def admin():
    if 'username' not in session:
        flash(f'please login first', 'danger')
        return redirect(url_for('login'))
    products = Addproduct.query.all()
    return render_template('admin/index.html', title='Adminpage', products=products)


# display the brands in admin
@app.route('/brands')
def brands():
    if 'username' not in session:
        flash(f'please login first', 'danger')
        return redirect(url_for('login'))
    brands = Brand.query.order_by(Brand.id.description)
    return render_template('admin/brand.html', brands=brands)


# display the category
@app.route('/category')
def category():
    if 'username' not in session:
        flash(f'please login first', 'danger')
        return redirect(url_for('login'))
    category = Category.query.order_by(Category.id.description)
    return render_template('admin/category.html', category=category)


# Admin Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if User.query.filter_by(email=form.email.data).first():
        flash('Email Already Registered!', 'danger')
    elif request.method == 'POST' and form.validate():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = User(name=form.name.data, username=form.username.data,
                    email=form.email.data, password=hash_password)
        db.session.add(user)
        db.session.commit()
        flash(f'welocme { form.name.data } Thanks for registering', 'success')
        return redirect(url_for('login'))
    return render_template('admin/register.html', form=form, title="Registration page")


# Admin login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForms(request.form)
    if request.method == "POST" and form.validate():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['username'] = form.username.data
            flash(f'welcome {form.username.data} your loggedin 😍😍😍', 'success')
            return redirect(request.args.get('next') or url_for('admin'))

        else:
            form = LoginForms(request.form)
            flash("wrong password please try again 😫😫😫", 'danger')
            return redirect(request.args.get('next') or url_for('login'))

    else:
        return render_template('admin/login.html', form=form, title='Login page')
