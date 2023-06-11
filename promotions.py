"""
promotions.py

The promotions module defines classes related to product promotions.

Module Contents:
    - Promotion: An abstract base class for promotions.
    - SecondHalfPrice: A promotion that offers a "buy one, get the second at half price" discount.
    - ThirdOneFree: A promotion that offers a "buy two, get one free" discount.
    - PercentDiscount: A promotion that applies a percentage discount.

Author:
    Salman Farhat

Date:
    [2023-06-01]
"""

from abc import ABC, abstractmethod
from products import Product


class Promotion(ABC):
    """
     The Promotion class is an abstract base class for different types of promotions.

      Attributes:
        name (str): The name of the promotion.

    Methods:
        apply_promotion(product, quantity): Applies the promotion to a product with the given quantity.
        calculate_discount_factor(product, quantity): Abstract method to calculate the
        discount factor for the promotion.
    """
    def __init__(self, name):
        """
        Initializes a new instance of the Promotion class.

        :param name: (str): The name of the promotion.
        """
        self.name = name

    @abstractmethod
    def calculate_discount_factor(self, product, quantity):
        """
        Abstract method to calculate the discount factor for the promotion.

        :param product: (Product): The product to apply the promotion to.
        :param quantity: (int): The quantity of the product.
        :return: float: The discount factor to apply to the product.

        """
        pass

    def apply_promotion(self, product, quantity):
        """
        Applies the promotion to a product with the given quantity.

        :param product: (Product): The product to apply the promotion to.
        :param quantity: (int): The quantity of the product.

        :return: float: The discounted price after applying the promotion.
        """
        items_to_pay_factor = self.calculate_discount_factor(product, quantity)
        discounted_price = product.price * items_to_pay_factor  # (1 - discount)

        return discounted_price


class SecondHalfPrice(Promotion):
    """
    The SecondHalfPrice class represents a promotion where every second item is half-priced.

    name (str): The name of the promotion.

    Methods:
        calculate_discount_factor(product, quantity): Calculates the discount factor for the promotion.
    """
    def __init__(self, name):
        """
        Initializes a new instance of the SecondHalfPrice class.

        :param name: (str): The name of the promotion.
        """
        super().__init__(name)

    def calculate_discount_factor(self, product, quantity):
        """
        Calculates the discount factor for the SecondHalfPrice promotion.

        :param product: (Product): The product to apply the promotion to.
        :param quantity: (int): The quantity of the product.

        :return: float: The discount factor to apply to the product. The discount factor to apply to the product.
        """
        items_to_pay_half_price = quantity // 2
        items_to_pay_full_price = quantity - items_to_pay_half_price
        items_to_pay_factor = (items_to_pay_full_price + (items_to_pay_half_price * 0.5)) # / quantity
        return items_to_pay_factor


class ThirdOneFree(Promotion):
    """
    The ThirdOneFree class represents a promotion where every third item is free.

    Attributes:
        name (str): The name of the promotion.

    Methods:
        calculate_discount_factor(product, quantity): Calculates the discount factor for the promotion.
    """
    def __init__(self, name):
        """
        Initializes a new instance of the ThirdOneFree class.

        :param name: (str): The name of the promotion.
        """
        super().__init__(name)

    def calculate_discount_factor(self, product, quantity):
        """
        Calculates the discount factor for the ThirdOneFree promotion.

        :param product: (Product): The product to apply the promotion to.
        :param quantity: (int): The quantity of the product.

        :return: float: The discount factor to apply to the product.
        """
        items_to_pay = quantity - (quantity // 3)
        return items_to_pay

class PercentDiscount(Promotion):
    """
    A class representing a promotion that applies a percentage discount.

    Attributes:
        name (str): The name of the promotion.
        percent (float): The percentage of discount to apply.

    Methods:
        calculate_discount_factor(product, quantity): Calculates the discount factor for the promotion.
    """
    def __init__(self, name, percent):
        """
        Initializes a new instance of the ThirdOneFree class.

        :param name: (str): The name of the promotion.
        :param percent: (float): The percentage of discount to apply.
        """
        super().__init__(name)
        self.percent = percent

    def calculate_discount_factor(self, product, quantity):
        """
        Calculates the discount factor for the PercentDiscount promotion.

        :param product: (Product): The product to apply the promotion to.
        :param quantity: (int): The quantity of the product.

        :return: float: The discount factor to apply to the product.
        """

        items_to_pay_factor = (100 - self.percent) / 100.0 * quantity
        return items_to_pay_factor

