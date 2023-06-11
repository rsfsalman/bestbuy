import pytest
from products import Product, LimitedProduct
from store import Store



def test_create_normal_product():
    name = "Mac"
    price = 1498.99
    quantity = 20

    product = Product(name, price, quantity)

    assert product.name == name
    assert product.price == price
    assert product.quantity == quantity
    assert product.is_active() is True


def test_create_product_with_invalid_name():
    price = 1498.99
    quantity = 20

    with pytest.raises(ValueError, match="Name cannot be empty"):
        empty_name_product = Product("", price, quantity)


def test_create_product_with_invalid_price():
    name = "MacPro"
    price = 0
    quantity = 20

    with pytest.raises(ValueError, match="price/quantity cannot be negative!"):
        empty_name_product = Product("GGF", price, quantity)


def test_create_product_with_invalid_quantity():
    name = "MacPro"
    price = 33
    quantity = -19

    with pytest.raises(ValueError, match="price/quantity cannot be negative!"):
        empty_name_product = Product("GGF", price, quantity)


def test_product_becomes_inactive_at_zero_quantity():
    # Create a product with an initial quantity of 3
    product = Product("Product Name", 10.99, 3)

    assert product.is_active() is True

    output, price = product.buy(3)

    assert product.is_active() is False


def test_product_purchase_modifies_quantity_and_returns_correct_output():
    # Create a product with an initial quantity of 10
    product = Product("Apple Mac", 10.99, 10)
    output, price = product.buy(3)
    assert product.quantity == 7
    assert output == "Purchased 3 units of Apple Mac."

    output, price = product.buy(7)
    assert product.quantity == 0
    assert product.active is False
    assert output == "Purchased 7 units of Apple Mac. Apple Mac is out of stock."


def test_buying_larger_quantity_than_exists_invokes_exception():
    product = Product("Mac Pro", 2000.0, 5)
    # with pytest.raises(ValueError, match="Insufficient quantity available for MacPro"):
    with pytest.raises(ValueError, match=f"The {product.name} has insufficient quantity available."):
        product.buy(10)


def test_quick_test():
    """
    Performs a quick test of the functionality of the Store and Product classes.

    The test includes the following steps:
    1. Initializes the initial stock of inventory with specific products.
    2. Attempts to set a negative price for a product, which should raise a ValueError.
    3. Prints the details of the 'mac' product, including its name, price, quantity, and promotion.
    4. Compares the 'mac' product with the 'bose' product, printing True if the 'mac' price is
        higher.
    5. Checks if the 'mac' product is present in the 'best_buy' store, printing True if it is.
    6. Checks if the 'pixel' product is present in the 'best_buy' store,
        printing False if it is not.

    :return: None
    """
    # setup initial stock of inventory
    mac = Product("MacBook Air M2", price=1450, quantity=100)
    bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    pixel = LimitedProduct("Google Pixel 7", price=500, quantity=250, limit=1)
    best_buy = Store([mac, bose])

    print("\n ---> Executing a quick test as requested in the exercise to verify\n"
          " the functionality of the magic methods. <---")

    try:
        mac.price = -100  # Should give error
    except ValueError as error:
        print("Error:", str(error))

    print(mac)  # Should print 'MacBook Air M2, Price: $1450 Quantity:100, Promotion: None'
    print(mac > bose)  # Should print True
    print(mac in best_buy)  # Should print True
    print(pixel in best_buy)  # Should print False

    print(" ---> The test was successfully completed. <---\n")
