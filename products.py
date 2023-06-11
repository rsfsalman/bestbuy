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

    def __init__(self, name, price, quantity):
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
        if not name or price <= 0.0 or quantity < 0:
            raise ValueError("Invalid input!"
                             "Name cannot be empty, and price/quantity cannot be negative!")

        self.name = name
        self.price = price
        self.quantity = quantity
        self.promotion = None

        # The active status of the product. It is set to True if the quantity is > 0,
        # otherwise it is set to False
        self.active = self.quantity > 0

    def get_quantity(self):
        """
		Get the available quantity of the product

		:return: (int) the available quantity of the product
		"""
        return self.quantity

    def set_quantity(self, quantity):
        """
		Updates the quantity of the product to the specified value.

		:param: quantity: (int) The new quantity value to set for the product.
		"""
        self.quantity = quantity
        if self.quantity == 0:
            self.deactivate()
        if self.quantity > 0:
            self.activate()

    def get_promotion(self):
        """
        Retrieves the promotion associated with the product.

        :return: The promotion object associated with the product.
        """
        return self.promotion

    def set_promotion(self, promotion):
        """
        Sets the promotion for the product.

        :param promotion: The promotion object to set for the product.
        :return: None
        """
        self.promotion = promotion

    def get_price(self) -> float:
        """
        Getter method for retrieving the price of the product.

		The get_price method returns the price of the product

		:return: (float) The price of the product.
		"""
        return self.price

    @property
    def price(self):
        """
        Getter method for retrieving the price of the product.

        :return: (float) The price of the product.
        """
        return self._price

    @price.setter
    def price(self, value):
        """
         Setter method for updating the price of the product.

        :param value:  (float): The new price value to be set

        Raises:
            ValueError: If the provided value is negative.
        """
        if value < 0:
            raise ValueError("Price cannot be negative")
        self._price = value

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

    def __str__(self):
        """
		The __str__ method displays information about the product.

		:return: (str) A string representation of the product with the following format:
						"{product name}, Price: {price}, Quantity: {quantity}".
		"""
        promotion_string = f"Promotion: {getattr(self.promotion, 'name', 'None')}"
        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}, {promotion_string}"

        # return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}"

    def __gt__(self, other):
        return self.price > other.price

    def __lt__(self, other):
        return self.price < other.price

    # def __getitem__(self, index):
    #     return self.items[index]

    def buy(self, quantity_to_purchase):
        """
    	The buy method allows purchasing a specific quantity of the product.

    	param: purchase_quantity (int): The quantity of the product to be purchased.

    	:return: (float) The total price of the purchased quantity of the product.

    	Raises:
    		ValueError: If there are no more items available (quantity is 0) or
    		if the purchase quantity exceeds the available quantity.
    		The exception message provides details on the error.

    		Note: 	If an error occurs during the purchase process, None is returned
    				and an error message is printed
    	"""
        total_price = 0.0
        if self.active:
            if quantity_to_purchase > self.quantity:
                raise ValueError(f"The {self.name} has insufficient quantity available.")

            self.quantity -= quantity_to_purchase
            if self.promotion:
                total_price = self.promotion.apply_promotion(self, quantity_to_purchase)
            else:
                total_price = self.price * quantity_to_purchase
            if self.quantity == 0:
                self.deactivate()
                return f"Purchased {quantity_to_purchase} units of {self.name}. {self.name} is" \
                       " out of stock.", total_price
            return f"Purchased {quantity_to_purchase} units of {self.name}.", total_price
        return f"{self.name} is out of stock.", total_price


class NonStockedProduct(Product):
    """
    A subclass of Product representing non-stocked products.

    NonStockedProduct inherits from the Product class and represents products
    that are not kept in stock. These products may have special characteristics or promotions
    but are subject to quantity limitations.

    Note: Non-stocked products are subject to quantity limitations as defined by the store's policy.
    Customers can purchase the non-stocked product up to the maximum allowed quantity specified
    by the policy.
    """
    def __init__(self, name, price):
        super().__init__(name, price, quantity=0)
        self.activate()

    def set_quantity(self, quantity):
        """
        Updates the quantity of the non-stocked product to the specified value.

        :param: quantity: (int) The new quantity value to set for the non-stocked product.
                            Note that non-stocked products do not have a physical inventory,
                            so the quantity value is not directly related to available stock.
                            Instead, it represents the maximum allowed quantity as per
                            the store's policy.
        """
        self.quantity = 0

    def deactivate(self):
        """
		Overrides the deactivate method from the superclass but does not deactivate
		the non-stocked product.
		"""
        # Method implementation goes here (if any)
        # Since we don't want to deactivate the non-stocked product, this method can be left empty

    def __str__(self):
        """
    	The __str__ method displays information about the product.

    	:return: (str) A string representation of the product with the following format:
    						"{product name}, Price: {price}, Quantity: Unlimited".
    	"""
        promotion_string = f"Promotion: {getattr(self.promotion, 'name', 'None')}"
        return f"{self.name}, Price: {self.price}, Quantity: Unlimited, {promotion_string}"

    def buy(self, quantity_to_purchase):
        """
    	The buy method allows purchasing a specific quantity of non-stocked the product.

    	param: purchase_quantity (int): The quantity of the product to be purchased.

    	:return: (tuple) A tuple containing the purchase message and
    	            the total price of the purchased quantity.

        Please note that the quantity of the purchase is subject to the maximum allowed quantity
        specified by the store policy.
    	"""
        total_price = 0.0
        if self.active:
            if self.promotion:
                total_price = self.promotion.apply_promotion(self, quantity_to_purchase)
            else:
                total_price = self.price * quantity_to_purchase
            return f"Purchased {quantity_to_purchase} units of {self.name}.", total_price
        return f"{self.name} is disabled right now, call the customer services to activate it.", \
            total_price


class LimitedProduct(Product):
    """
    A class representing a limited product.

    limit (int): The maximum allowed quantity for this product.
    """
    def __init__(self, name, price, quantity, limit):
        super().__init__(name, price, quantity)
        self.limit = limit

    def __str__(self):
        """
		Return a string representation of the product.

		:return: (str) A string representation of the product with the following format:
						"{product name}, Price: {price}, Quantity: {quantity},
						Limited to {limit} per order, Promotion: {promotion}".
						If no promotion is set, the promotion field will display as "None".
		"""
        promotion_string = f"Promotion: {getattr(self.promotion, 'name', 'None')}"
        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}, " \
               f"Limited to {self.limit} per order, {promotion_string}"

    def get_limit(self):
        """
        Get the limit value for the limited product.

        :return: int: The limit value indicating the maximum quantity allowed per order.
        """
        return self.limit

    def set_limit(self, limit):
        """
        Set the limit value for the limited product.

        :param limit: (int): The new limit value to set for the maximum quantity allowed per order.
        :return:
        """
        self.limit = limit
