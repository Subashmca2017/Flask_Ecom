from flask import request, redirect, render_template, flash, url_for, session, current_app
from shop import db, app, app_root, search
from .models import Brand, Category, Addproduct
from .forms import Addproducts
import os
import secrets
import secrets
import sqlite3


def brands():
    brands = Brand.query.join(Addproduct, Brand.id ==
                              Addproduct.brand_id).all()
    return brands


def categories():
    categorys = Category.query.join(
        Addproduct, (Category.id == Addproduct.category_id)).all()
    return categorys


# Back to Dashboard

@app.route('/')
def first():
    page = request.args.get('page', 1, type=int)
    products = Addproduct.query.filter(
        Addproduct.stock > 0).paginate(page=page, per_page=12)
    brands = Brand.query.join(Addproduct, Brand.id ==
                              Addproduct.brand_id).all()
    categorys = Category.query.join(
        Addproduct, (Category.id == Addproduct.category_id)).all()
    return render_template('products/first.html', products=products, brands=brands, categorys=categorys)


# Returns the Dashboard

@app.route('/first')
def home():
    page = request.args.get('page', 1, type=int)
    products = Addproduct.query.filter(
        Addproduct.stock > 0).paginate(page=page, per_page=12)
    brands = Brand.query.join(Addproduct, Brand.id ==
                              Addproduct.brand_id).all()
    categorys = Category.query.join(
        Addproduct, (Category.id == Addproduct.category_id)).all()
    return render_template('products/index.html', products=products, brands=brands, categorys=categorys)


@app.route('/result')
def result():
    searchword = request.args.get('q')
    products = Addproduct.query.msearch(
        searchword, fields=['name', 'desc', 'price'], limit=6)
    return render_template('products/result.html', products=products, brands=brands(), categorys=categories())


# To Get individual Product info

@app.route('/product/<int:id>')
def detail_page(id):
    brands = Brand.query.join(Addproduct, Brand.id ==
                              Addproduct.brand_id).all()
    categorys = Category.query.join(
        Addproduct, (Category.id == Addproduct.category_id)).all()
    product = Addproduct.query.get_or_404(id)
    return render_template('products/detail_page.html', product=product, brands=brands, categorys=categorys)


# To Retrieve the brand

@app.route('/brand/<int:id>')
def get_brand(id):
    brand = Addproduct.query.filter_by(brand_id=id)
    brands = Brand.query.join(Addproduct, Brand.id ==
                              Addproduct.brand_id).all()
    categorys = Category.query.join(
        Addproduct, (Category.id == Addproduct.category_id)).all()
    return render_template('products/index.html',  brand=brand, brands=brands, categorys=categorys)


# To Retrieve the category

@app.route('/categorys/<int:id>')
def get_categorys(id):
    """
    args: Category id
    """
    get_cat = Addproduct.query.filter_by(category_id=id)
    brands = Brand.query.join(Addproduct, Brand.id ==
                              Addproduct.brand_id).all()
    categorys = Category.query.join(
        Addproduct, (Category.id == Addproduct.category_id)).all()
    return render_template('products/index.html', get_cat=get_cat, brands=brands, categorys=categorys)


# To create the brand

@app.route('/addbrand', methods=['POST', 'GET'])
def addbrand():
    if 'username' not in session:
        flash(f'please login first', 'danger')
        return redirect(url_for('login'))
    if request.method == "POST":
        getbrand = request.form.get('brand')
        brand = Brand(name=getbrand)
        db.session.add(brand)
        flash(f'The brand {getbrand} was added to your database', 'success')
        db.session.commit()
        return redirect(url_for('addbrand'))
    return render_template('products/addbrand.html', brands='brands')


# To update the brand

@app.route('/updatebrand/<int:id>', methods=['GET', 'POST'])
def update(id):
    """
    args: Brand id
    """
    if 'username' not in session:
        flash(f'please login first', 'danger')
    updatebrand = Brand.query.get_or_404(id)
    brand = request.form.get('brand')
    if request.method == "POST":
        updatebrand.name = brand
        flash(f'your brand has been updated', 'success')
        db.session.commit()
        return redirect(url_for('brands'))

    return render_template('products/update_brand.html', title='updatebarand', updatebrand=updatebrand)


# To delete the brand

@app.route('/deletebrand/<int:id>', methods=['POST'])
def deletebrand(id):
    """
    args: Brand id
    """
    brand = Brand.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(brand)
        flash(f' The brand {brand.name} is deleted successfully', 'success')
        db.session.commit()
        return redirect(url_for('brands'))
    flash(f' The brand {brand.name} is cannot be deleted ', 'warning')
    return redirect(url_for('admin'))


# To update the category

@app.route('/updatecat/<int:id>', methods=['GET', 'POST'])
def updatecat(id):
    """
    args: catgeory id
    """
    if 'username' not in session:
        flash(f'please login first', 'danger')
    updatecategory = Category.query.get_or_404(id)
    category = request.form.get('category')
    if request.method == "POST":
        updatecategory.name = category
        flash(f'your category has been updated successfully', 'success')
        db.session.commit()
        return redirect(url_for('category'))
    return render_template('products/update_brand.html', title='updatecategory', updatecategory=updatecategory)


# To Delete the category

@app.route('/deletecat/<int:id>', methods=['POST'])
def deletecat(id):
    """
    args: category id
    """
    category = Category.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(category)
        flash(f'The category {category.name} was deleted', 'success')
        db.session.commit()
        return redirect(url_for('admin'))
    flash(f'the category {category.name} was cannot be deleted', 'warning')
    return redirect(url_for('admin'))


# To create the category
@app.route('/addcat', methods=['GET', 'POST'])
def addcat():
    if 'username' not in session:
        flash(f'please login first', 'danger')
        return redirect(url_for('login'))
    if request.method == "POST":
        getbrand = request.form.get('category')
        cat = Category(name=getbrand)
        db.session.add(cat)
        flash(f'The category {getbrand} was added to your database', 'success')
        db.session.commit()
        return redirect(url_for('addcat'))
    return render_template('products/addbrand.html')


# To create the product

@app.route('/Addproduct', methods=['GET', 'POST'])
def addproduct():
    if 'username' not in session:
        flash(f'please login first', 'danger')
        return redirect(url_for('login'))
    brands = Brand.query.all()
    categorys = Category.query.all()
    form = Addproducts(request.form)
    if request.method == "POST":
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        desc = form.description.data
        colors = form.colors.data
        brands = request.form.get('brand')
        category = request.form.get('category')
        upload_image1 = request.files['image1']
        upload_image2 = request.files['image2']
        upload_image3 = request.files['image3']
        if upload_image1 != "" and upload_image2 != "" and upload_image3 != "":
            filepath1 = os.path.join(
                app.config['UPLOAD_FOLDER'], upload_image1.filename or secrets.token_hex(10) + "")
            filepath2 = os.path.join(
                app.config['UPLOAD_FOLDER'], upload_image2.filename or secrets.token_hex(10) + ".")
            filepath3 = os.path.join(
                app.config['UPLOAD_FOLDER'], upload_image3.filename or secrets.token_hex(10) + ".")

            upload_image1.save(filepath1)
            upload_image2.save(filepath2)
            upload_image3.save(filepath3)

        addpr = Addproduct(name=name, price=price, discount=discount, stock=stock, desc=desc, colors=colors,
                           brand_id=brands, category_id=category, image1=filepath1, image2=filepath2, image3=filepath3)
        db.session.add(addpr)
        flash(f'Your {name} product has been updated', 'success')
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('products/addproduct.html', title='add product page', form=form, brands=brands,
                           categorys=categorys)


# product update the product

@app.route('/updateproduct/<int:id>', methods=['GET', 'POST'])
def updateproduct(id):
    """
    args: product id
    """
    brands = Brand.query.all()
    categorys = Category.query.all()
    product = Addproduct.query.get_or_404(id)
    brand = request.form.get('brand')
    category = request.form.get('category')
    form = Addproducts(request.form)
    if request.method == 'POST':
        product.name = form.name.data
        product.price = form.price.data
        product.discount = form.discount.data
        product.stock = form.stock.data
        product.brand_id = brand
        product.colors = form.colors.data
        product.desc = form.description.data
        if request.files.get('image1'):
            try:
                upload_image1 = request.files['image1']
                os.unlink(os.path.join(current_app.root_path,
                          "static/images/" + product.image1))
                product.image1 = os.path.join(
                    app.config['UPLOAD_FOLDER'], os.path.join(upload_image1.filename))
            except:
                product.image1 = os.path.join(
                    app.config['UPLOAD_FOLDER'], upload_image1.filename)
        if request.files.get('image2'):
            try:
                upload_image2 = request.files['image2']
                os.unlink(os.path.join(current_app.root_path,
                          "static/images/" + product.image2))
                product.image2 = os.path.join(
                    app.config['UPLOAD_FOLDER'], upload_image2.filename)
            except:
                product.image2 = os.path.join(
                    app.config['UPLOAD_FOLDER'], upload_image2.filename)

        if request.files.get('image3'):
            try:
                upload_image3 = request.files['image3']
                os.unlink(os.path.join(current_app.root_path,
                          "static/images/" + product.image3))
                product.image3 = os.path.join(
                    app.config['UPLOAD_FOLDER'], os.path.join(upload_image3.filename))
            except:
                product.image3 = os.path.join(
                    app.config['UPLOAD_FOLDER'], os.path.join(upload_image3.filename))
        db.session.commit()
        flash(f'Your product "{product.name}" has been updated', 'success')
        return redirect(url_for('admin'))
    form.name.data = product.name
    form.price.data = product.price
    form.discount.data = product.discount
    form.stock.data = product.stock
    form.colors.data = product.colors
    form.description.data = product.desc
    return render_template('products/update_product.html', form=form, brands=brands, categorys=categorys,
                           product=product)


# To delete the product

@app.route('/deleteproduct/<int:id>', methods=['POST'])
def deleteproduct(id):
    """
    args: product id
    """
    product = Addproduct.query.get_or_404(id)
    if request.method == 'POST':
        try:

            os.unlink(os.path.join(current_app.root_path,
                      "static/images/" + product.image1))
            os.unlink(os.path.join(current_app.root_path,
                      "static/images/" + product.image2))
            os.unlink(os.path.join(current_app.root_path,
                      "static/images/" + product.image3))

        except Exception as e:
            print(e)
        db.session.delete(product)
        flash(f'The product {product.name} was deleted', 'success')
        db.session.commit()
        return redirect(url_for('admin'))
    flash(f'the product {product.name}was cannot be deleted', 'danger')
    return redirect(url_for('admin'))
