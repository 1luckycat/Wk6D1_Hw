from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required

from pet_shop.models import Customer, Product, ProdOrder, Order, db, product_schema, products_schema

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/token', methods=['GET', 'POST'])
def token():
    data = request.json
    if data:
        client_id = data['client_id']
        access_token = create_access_token(identity=client_id)
        return {
            'status': 200,
            'access_token': access_token
        }
    else:
        return {
            'status': 400,
            'message': 'Missing Client ID.  Please try again.'
        }
    

@api.route('/shop')
@jwt_required()
def get_shop():
    allprods = Product.query.all()

    response = products_schema.dump(allprods)
    return jsonify(response)


@api.route('/order/create/<cust_id>', methods=['POST'])
@jwt_required()
def create_order(cust_id):
    data = request.json
    customer_order = data['order']
    customer = Customer.query.filter(Customer.cust_id == cust_id).first()

    if not customer:
        customer = Customer(cust_id)
        db.session.add(customer)

    order = Order()
    db.session.add(order)

    for pet in customer_order:
        prodorder = ProdOrder(pet['prod_id'], pet['quantity'], pet['price'], order.order_id, cust_id)
        db.session.add(prodorder)

        order.increment_ordertotal(prodorder.price)

        current_product = Product.query.get(pet['prod_id'])
        current_product.decrement_quantity(pet['quantity'])

    db.session.commit()

    return {
        'status': 200,
        'message': 'New order created!'
    }


@api.route('/order/<cust_id>')
@jwt_required()
def get_orders(cust_id):

    prodorder = ProdOrder.query.filter(ProdOrder.cust_id == cust_id).all()

    data = []

    for order in prodorder:
        pet = Product.query.filter(Product.prod_id == order.prod_id).first()

        pet_dict = product_schema.dump(pet)

        pet_dict['quantity'] = order.quantity
        pet_dict['order_id'] = order.order_id
        pet_dict['id'] = order.prodorder_id

        data.append(pet_dict)

    return jsonify(data)



@api.route('/order/update/<order_id>', methods=['PUT'])
@jwt_required()
def update_order(order_id):
    data = request.json
    new_quantity = int(data['quantity'])
    prod_id = data['prod_id']

    prodorder = ProdOrder.query.filter(ProdOrder.order_id == order_id, ProdOrder.prod_id == prod_id).first()
    order = Order.query.get(order_id)
    pet = Product.query.get(prod_id)

    order.decrement_ordertotal(prodorder.price)

    prodorder.set_price(pet.price, new_quantity)

    order.increment_ordertotal(prodorder.price)

    diff = abs(new_quantity - prodorder.quantity)

    if prodorder.quantity > new_quantity:
        pet.increment_quantity(diff)
    else:
        pet.decrement_quantity(diff)

    prodorder.update_quantity(new_quantity)

    db.session.commit()

    return {
        'status': 200,
        'message': 'Order was updated successfully!'
    }



@api.route('/order/delete/<order_id>', methods=['DELETE'])
@jwt_required()
def delete_order(order_id):
    data = request.json
    prod_id = data['prod_id']

    prodorder = ProdOrder.query.filter(ProdOrder.order_id == order_id, ProdOrder.prod_id == prod_id).first()
    order = Order.query.get(order_id)
    pet = Product.query.get(prod_id)

    order.decrement_ordertotal(prodorder.price)
    pet.increment_quantity(prodorder.quantity)

    db.session.delete(prodorder)
    db.session.commit()

    return {
        'status': 200,
        'message': 'Order was deleted successfully!'
    }