from flask import request, redirect, render_template, flash, url_for, session, current_app, make_response
from flask_login import login_required, current_user, logout_user, login_user
from shop import db, app, app_root, search, bcrypt, login_manager
from .forms import CustomerRegistration, CustomerLoginForm
from .models import Register, CustomerOrder
from shop.products .models import Addproduct
import os
import secrets
import secrets
import sqlite3
import pdfkit
import stripe

publishable_key = 'pk_test_51J3HcKSFB4OYhriuhC0EWzk6W4i3PxYO34Kk81hwiMTSWsE9jPndaRzDoUCTNDiLXXPfCgUHN4Qi51F17XfF4xqV00jQiXX9YP'
stripe.api_key = 'sk_test_51J3HcKSFB4OYhriu7wF0jzCoG1XhiI4TfDzrDR5ByUxwmKtGEDiPcEAmUQSNPzYklpCporeRctHQRiD2VFUksVYy0094d7X5fC'


# Processing the payment
@app.route('/payment', methods=['POST'])
@login_required
def payment():
    invoice = request.form.get('invoice')
    amount = request.form.get('amount')
    customer = stripe.Customer.create(
        email=request.form['stripeEmail'],
        source=request.form['stripeToken'],
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        description='My Shop',
        amount=amount,
        currency='inr',
    )
    orders = CustomerOrder.query.filter_by(
        customer_id=current_user.id, invoice=invoice).order_by(CustomerOrder.id.desc()).first()
    orders.status = 'paid'
    db.session.commit()
    return redirect(url_for('thanks'))


@app.route('/thanks')
def thanks():
    return render_template('customer/thank.html')


# Customer Registration
@app.route('/customer/register', methods=['GET', 'POST'])
def customer_register():
    form = CustomerRegistration()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        cust_register = Register(name=form.name.data, username=form.username.data, email=form.email.data, password=hash_password, state=form.state.data,
                                 country=form.country.data, contact=form.contact.data, city=form.city.data, address=form.address.data, pincode=form.pincode.data)
        db.session.add(cust_register)
        flash(f'welcome {form.name.data} Thank you for registering', 'success')
        db.session.commit()
        return redirect(url_for('customerLogin'))
    return render_template('customer/register.html', form=form)


# Customer Login
@app.route('/customer/login', methods=['GET', 'POST'])
def customerLogin():
    form = CustomerLoginForm()
    if form.validate_on_submit():
        user = Register.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("You are login now", 'success')
            next = request.args.get('next')
            return redirect(next or url_for('home'))
        flash("incorrect email and password ", 'danger')
        return redirect(url_for('customerLogin'))

    return render_template('customer/login.html', form=form)


# Logout method
@app.route('/customer/logout')
def customerlogout():
    logout_user()
    return redirect(url_for('home'))


# remove unwanted details from Shoppingcart
def updateshoppingcart():
    for _key, product in session['Shoppingcart'].items():
        session.modified = True
        del product['image']
        del product['colors']
    return updateshoppingcart


# Order status
@app.route('/getorder')
@login_required
def get_order():
    if current_user.is_authenticated:
        customer_id = current_user.id
        invoice = secrets.token_hex(5)
        updateshoppingcart()
        try:
            order = CustomerOrder(
                invoice=invoice, customer_id=customer_id, orders=session['Shoppingcart'])
            print(order)
            db.session.add(order)
            db.session.commit()
            session.pop('Shoppingcart')
            flash("your order has been Placed", 'success')
            return redirect(url_for('order', invoice=invoice))
        except Exception as e:
            print(e)
            flash('something went wrong while get order', 'danger')
            return redirect(url_for('getcart'))


# To get order by id
@app.route('/orders/<invoice>')
@login_required
def order(invoice):
    if current_user.is_authenticated:
        grandTotal = 0
        subTotal = 0
        customer_id = current_user.id
        customer = Register.query.filter_by(id=customer_id).first()
        orders = CustomerOrder.query.filter_by(
            customer_id=customer_id).order_by(CustomerOrder.id.desc()).first()
        for _key, product in orders.orders.items():
            discount = (product['discount']/100) * float(product['price'])
            subTotal += float(product['price']) * int(product['quantity'])
            subTotal -= discount
            tax = ("%.2f" % (.06 * float(subTotal)))
            grandTotal = ("%.2f" % (1.06 * float(subTotal)))

    else:
        return redirect((url_for('customerLogin')))
    return render_template('customer/order.html', invoice=invoice, tax=tax, subTotal=subTotal, grandTotal=grandTotal, customer=customer, orders=orders)


# To get the pdf by invoice ref
@app.route('/get_pdf/<invoice>', methods=['POST'])
@login_required
def get_pdf(invoice):
    if current_user.is_authenticated:
        gradTotal = 0
        subTotal = 0
        customer_id = current_user.id
        if request.method == "POST":
            customer = Register.query.filter_by(id=customer_id).first()
            orders = CustomerOrder.query.filter_by(
                customer_id=customer_id).order_by(CustomerOrder.id.desc()).first()
            for _key, product in orders.orders.items():
                discount = (product['discount']/100) * float(product['price'])
                subTotal += float(product['price']) * int(product['quantity'])
                subTotal -= discount
                tax = ("%.2f" % (.06 * float(subTotal)))
                grandTotal = float("%.2f" % (1.06 * subTotal))

            rendered = render_template('customer/pdf.html', invoice=invoice,
                                       tax=tax, grandTotal=grandTotal, customer=customer, orders=orders)
            pdf = pdfkit.from_string(rendered, False)
            response = make_response(pdf)
            response.headers['content-Type'] = 'application/pdf'
            response.headers['content-Disposition'] = 'inline: filename=' + \
                invoice+'.pdf'
            return response
    return request(url_for('order'))
