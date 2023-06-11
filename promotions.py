from abc import ABC, abstractmethod
from products import Product


class Promotion(ABC):
    def __init__(self, name):
        self.name = name

    def apply_promotion(self, product, quantity):
        items_to_pay_factor = self.calculate_discount_factor(product, quantity)
        discounted_price = product.price * items_to_pay_factor  # (1 - discount)

        return discounted_price

    @abstractmethod
    def calculate_discount_factor(self, product, quantity):
        pass


class SecondHalfPrice(Promotion):
    def __init__(self, name):
        super().__init__(name)

    def calculate_discount_factor(self, product, quantity):
        items_to_pay_half_price = quantity // 2
        items_to_pay_full_price = quantity - items_to_pay_half_price
        items_to_pay_factor = (items_to_pay_full_price + (items_to_pay_half_price * 0.5)) # / quantity

        # if quantity > 1:
        #     rem = quantity % 2
        #     sets = quantity // 2
        #     discount = (rem + (sets * 1.5)) / quantity
        # else:
        #     discount = 0
        return items_to_pay_factor


class ThirdOneFree(Promotion):
    def __init__(self, name):
        super().__init__(name)

    def calculate_discount_factor(self, product, quantity):
        items_to_pay = quantity - (quantity // 3)
        # items_to_pay_factor = items_to_pay  # / quantity
        return items_to_pay

class PercentDiscount(Promotion):
    def __init__(self, name, percent):
        super().__init__(name)
        self.percent = percent

    def calculate_discount_factor(self, product, quantity):
        items_to_pay_factor = (100 - self.percent) / 100.0 * quantity
        return items_to_pay_factor

