from flask import Blueprint, flash, redirect, render_template, request

# internal imports
from pet_shop.models import Product, Customer, Order, db
from pet_shop.forms import ProductForm
from pet_shop.helpers import get_info

site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/')
def shop():
    allprods = Product.query.all()
    allcustomers = Customer.query.all()
    allorders = Order.query.all()

    shop_stats = {
        'products': len(allprods),
        'sales': sum([order.order_total for order in allorders]),
        'customers': len(allcustomers)
    }

    return render_template('shop.html', shop=allprods, stats=shop_stats) 


@site.route('/shop/create', methods=['GET', 'POST'])
def create():

    createform = ProductForm()
    if request.method == 'POST' and createform.validate_on_submit():
        animal_type = createform.animal_type.data
        color = createform.color.data
        image = createform.image.data
        description = createform.description.data
        price = createform.price.data
        quantity = createform.quantity.data

        pet = Product(animal_type, price, quantity, color, image, description)

        db.session.add(pet)
        db.session.commit()

        flash(f"You have successfully added {animal_type}", category='success')
        return redirect('/')
    
    elif request.method == 'POST':
        flash("Unable to process your request.  Please try again.", category='warning')
        return redirect('/shop/create')
    
    return render_template('create.html', form=createform)


@site.route('/shop/update/<id>', methods=['GET', 'POST'])
def update(id):
    pet = Product.query.get(id)

    updateform = ProductForm()

    if request.method == 'POST' and updateform.validate_on_submit():
        pet.animal_type = updateform.animal_type.data
        pet.color = updateform.color.data
        pet.image = pet.set_image(updateform.image.data, updateform.animal_type.data)
        pet.description = updateform.description.data
        pet.price = updateform.price.data
        pet.quantity = updateform.quantity.data

        db.session.commit()

        flash(f"You have successfully updated {pet.animal_type}", category='success')
        return redirect('/')
    
    elif request.method == 'POST':
        flash("Unable to process your request.  Please try again.", category='warning')
        return redirect(f'/shop/update/{pet.prod_id}')
    
    return render_template('/update.html', form=updateform, product=pet)


@site.route('/shop/delete/<id>')
def delete(id):
    pet = Product.query.get(id)

    db.session.delete(pet)
    db.session.commit()

    return redirect('/')