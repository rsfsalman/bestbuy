"""
Product.py - File for the Product class

This file defines the Product class, which represents a product in the store inventory.
The class provides attributes and methods to manage the product's name, price, quantity,
and active status.

It also allows interaction such as getting the quantity, setting the quantity, getting
the price, activating, deactivating, showing product information, and purchasing the product.

Classes:
    Product: A class representing a product.

Author:
    Salman Farhat

Date:
    2023-Jun-05
"""


class Product:
    """
	A class representing a product.

	Attributes:
		name (str): The name of the product.
		price (float): The price of the product.
		quantity (int): The quantity of the product.
		active (bool): The active status of the product.
	"""

    def __init__(self, name, price=100, quantity=100):
        """
		The __init__ method initializes a new instance of the class with the provided arguments

		It sets the instance variables name, price, and quantity based on the provided values.
		If any of the input values are invalid, such as an empty name or negative price or quantity,
		a ValueError is raised with an appropriate error message.

		:param: name (str):The name of the product.
		:param: price (float, optional): The price of the product. Defaults to 100
		:param: quantity (int, optional): The quantity of the product. Defaults to 100.

		Raises:
			ValueError: If the name is empty or if the price or quantity is negative.
		"""
        if not name or price < 0 or quantity < 0:
            raise ValueError("Invalid input!"
                             "Name cannot be empty, and price/quantity cannot be negative!")

        self.name = name
        self.price = price
        self.quantity = quantity
        # self.active = False if quantity == 0 else True

        # The active status of the product. It is set to True if the quantity is > 0,
        # otherwise it is set to False
        self.active = quantity != 0

    def get_quantity(self):
        """
		Get the available quantity of the product

		:return: (int) the available quantity of the product
		"""
        return self.quantity

    def set_quantity(self, quantity):
        """
		set_quantity
		"""
        self.quantity += quantity
        if self.quantity == 0:
            self.deactivate()

    def get_price(self) -> float:
        """
		The get_price method returns the price of the product

		:return: (float) The price of the product.
		"""
        return self.price

    def activate(self):
        """
		The activate method activates the product.
		"""
        self.active = True

    def deactivate(self):
        """
		The deactivate method deactivates the product.
		"""
        self.active = False

    def is_active(self):
        """
		The is_active method checks if the product is active.

		:return: bool: True if the product is active, False otherwise.
		"""
        return self.active

    def show(self):
        """
		The show method displays information about the product.

		:return: (str) A string representation of the product with the following format:
						"{product name}, Price: {price}, Quantity: {quantity}".
		"""
        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}"

    def buy(self, purchase_quantity):
        """
		The buy method allows purchasing a specific quantity of the product.

		:param: purchase_quantity (int): The quantity of the product to be purchased.

		:return: (float) The total price of the purchased quantity of the product.

		Raises:
			ValueError: If there are no more items available (quantity is 0) or
			if the purchase quantity exceeds the available quantity.
			The exception message provides details on the error.

			Note: 	If an error occurs during the purchase process, None is returned
					and an error message is printed
		"""
        try:
            if self.quantity == 0:
                raise ValueError("No more items available.")

            self.quantity -= purchase_quantity
            if self.quantity == 0:
                self.deactivate()

            return self.price * purchase_quantity
        except ValueError as err:
            print("Error:", str(err))
            return None
