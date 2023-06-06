// Adapter Pattern

// Define an interface for the cart management
class CartInterface {
  addItem(item) {}
  getItems() {}
  clearItems() {}
}

// Implement the cart management using localStorage
class LocalStorageCartAdapter extends CartInterface {
  addItem(item) {
    // Check if the cart items exist in localStorage
    var cartItems = localStorage.getItem('cartItems');
    if (cartItems) {
      // Parse the existing cart items from localStorage
      cartItems = JSON.parse(cartItems);
    } else {
      // If no cart items exist, initialize an empty array
      cartItems = [];
    }

    // Add the new cart item to the array
    cartItems.push(item);

    // Save the updated cart items back to localStorage
    localStorage.setItem('cartItems', JSON.stringify(cartItems));

    // Show a success message (you can customize this)
    alert('Product added to cart!');
  }

  getItems() {
    var cartItems = localStorage.getItem('cartItems');
    if (cartItems) {
      return JSON.parse(cartItems);
    } else {
      return [];
    }
  }

  clearItems() {
    localStorage.removeItem('cartItems');
  }
}

// Bridge Pattern

// Define the abstraction for the cart operation
class CartOperation {
  constructor(cartInterface) {
    this.cartInterface = cartInterface;
  }

  addItem(item) {
    this.cartInterface.addItem(item);
  }

  getItems() {
    return this.cartInterface.getItems();
  }

  clearItems() {
    this.cartInterface.clearItems();
  }
}
// Singleton Pattern

class CartSingleton {
  constructor() {
    if (!CartSingleton.instance) {
      CartSingleton.instance = this;
      this.cartInterface = new LocalStorageCartAdapter();
    }
    return CartSingleton.instance;
  }

  addItem(item) {
    this.cartInterface.addItem(item);
  }

  getItems() {
    return this.cartInterface.getItems();
  }

  clearItems() {
    this.cartInterface.clearItems();
  }
}

// Get the "ADD TO CART" buttons
var addToCartButtons = document.querySelectorAll('.button-content');

// Create an instance of the cart using the Singleton pattern
var cartInstance = new CartSingleton();


// Add a click event listener to the button
$('.button-contentt').click(function () {
    t = $(this).parent().parent().parent().children(".name").text();
    t2 = $(this).parent().parent().parent().children(".price-section").children(".price").text();
    var product = {
      name: t,
      price: t2
    };
    cartInstance.addItem(product);
});
// Function to display cart items
function displayCartItems() {
  var cartItems = cartInstance.getItems();

  if (cartItems.length === 0) {
    // Show a message if the cart is empty
    alert('Your cart is empty.');
  } else {
    var cartContent = '';
    // Create a string with the cart item details
    cartItems.forEach(function(item) {
      cartContent += item.name + ' - ' + item.price + '\n';
    });
    alert(cartContent);
  }
}

// Call the displayCartItems function to initially display the cart items
$('.bagt').click(function() {
  displayCartItems();
});

// Clear cart items when the page is refreshed or closed
window.addEventListener('beforeunload', function() {
  cartInstance.clearItems();
});