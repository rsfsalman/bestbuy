import pytest
from products import Product


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

