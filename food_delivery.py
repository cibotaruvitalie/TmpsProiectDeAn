import eel

# Initialize Eel
eel.init('web')

# Define the available food products
food_products = [
    {"name": "Pizza", "price": 10},
    {"name": "Burger", "price": 5},
    {"name": "Pasta", "price": 8},
    # Add more food products here
    {"name": "Salad", "price": 6},
]

# Define the cart to store selected items
cart = []

# Define the order total
total = 0


@eel.expose
def add_to_cart(product_index):
    global total
    product = food_products[int(product_index)]
    cart.append(product)
    total += product['price']


@eel.expose
def place_order():
    global cart, total
    if len(cart) > 0:
        print("Order placed!")
        print("Items:")
        for item in cart:
            print(item['name'])
        print("Total:", total)
        # Clear the cart and total
        cart = []
        total = 0
    else:
        print("Cart is empty!")


@eel.expose
def get_food_products():
    return food_products


# Start the web application
eel.start('main.html', size=(600, 400))