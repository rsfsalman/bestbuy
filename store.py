"""
store.py - Module file containing the Store class

This module defines the Store class, which represents a store.

The class provides attributes and methods to manage the store's products,
display the store menu, get active products, add and remove products, place an order,
find a product by name, generate an order ID, display the order summary,
validate user input, and more.

Classes:
    Store: A class representing a store.

Author:
    Salman Farhat

Date:
    2023-Jun-06
"""

import random
import string
from typing import List, Tuple, Optional
from products import Product


def order_intro():
    """
	Provides an introduction to the ordering process.
	"""
    # start the shopping
    print("\nEnter the number of the item you want to order (or 0 to cancel)")
    # When you want to finish order, enter empty text.
    print("To proceed with the checkout, simply input an empty text.")


def make_option_list(start: int, end: int) -> List[str]:
    """
	Create a list of string options based on the provided range.

	:param start: (int) The starting number of the range (inclusive)
	:param end: (int) The ending number of the range (exclusive)

	:return: (List[str]) A list of string options.
	"""
    # prepare the valid options menu
    options = []
    for num in range(start, end):
        options.append(str(num))
    options.append("")
    return options


class Store:
    """
	A class representing a store

	Attributes:
		products_list (List[Product]): A list of Product instances available in the store.

	Methods:
		__init__: Initialize the Store object.
		display_store_menu: Displays a list of available items and
							allows the customer to select an item by number.
		get_products: Get a list of active products available in the store.
		add_product: Add a product to the store.
		remove_product: Remove a product from the store.
		order: Place an order for a given shopping list and calculate the total price.
	"""

    def __init__(self, products):
        """
		Initialize the Store object.

		:param products: (list): A list of Product instances to be added to the store.
		"""
        self.products_list = products
        self.purchased_list = []
        self.order_list = []

    @classmethod
    def display_store_menu(cls):
        """
		Displays the store menu.
		"""
        print("\n   Store Menu")
        print("   ----------")
        print(" 1. List all products in store")
        print(" 2. Show total amount in store")
        print(" 3. Make an order")
        print(" 4. Quit")

    def get_products(self, display_flag: bool = False) -> Tuple[List[Product], int]:
        """
		Get a list of active products available in the store.

		:display_flag:	(bool, optional): specifies whether to display the available items.
						defaults to False.
		Returns:
			List[Product]: A list of active products available in the store.
		"""
        active_products = []
        for product in self.products_list:
            if product.is_active():
                active_products.append(product)

        if display_flag:
            print("\n------- Available Items -------")
            for index, product in enumerate(active_products, start=1):
                print(f"{index}. {product.name}, Price: ${product.price}, "
                      f"Quantity: {product.quantity}")
            # print(f"--- {len(active_products)} categories were found! ---")

            if len(active_products) == 1:
                print(f"--- {len(active_products)} category was found! ---")
            elif len(active_products) > 1:
                print(f"--- {len(active_products)} categories were found! ---")
            else:
                print("--- No categories were found! ---")

        return active_products, len(active_products)

    def display_products_list(self):
        """
		Displays a list of available items and allows the user to select
		an item by number.
		"""
        self.get_products(display_flag=True)

    def add_product(self, product):
        """
		Add a product to the store.

		:param: product (Product): The product instance to be added to the store.
		"""
        self.products_list.append(product)

    def remove_product(self, product):
        """
		Remove a product from the store.

		:param: product (Product): The product instance to be removed from the store.
		"""
        if product in self.products_list:
            self.products_list.remove(product)

    def get_total_quantity(self) -> int:
        """
		Returns the total number of all products in the store.

		:return: (int) The total quantity of all products in the store
		"""
        total_quantity: int = 0
        for product in self.products_list:
            total_quantity += product.quantity
        return total_quantity

    def display_total_quantity(self):
        """
		Display the total number of all products in the store.
		"""
        total_quantity = self.get_total_quantity()
        print(f"\nTotal of {total_quantity} items in store")

    def init_order_list(self) -> List:
        """
		A special method to initialize the order list

		:return: (list)
		"""
        # if len(self.purchased_list) > 0:
        # 	return self.purchased_list
        self.purchased_list = []
        return []

    def place_order(self):
        """
		Displays a list of available items and allows the user to select
		an item by number
		"""
        items_list, max_num = self.get_products(display_flag=True)
        # max_num = len(items_list)

        # check if the store is empty
        if max_num == 0:
            print("--- Currently, there are no items available for sale in the store."
                  "Please visit us again later! ---")
            return

        order_intro()

        # prepare the valid options menu
        options = make_option_list(0, max_num + 1)

        # if this is the first purchase or not
        order_list = self.init_order_list()

        # reference status to indicate order status
        cancelled_status = False
        confirmed_status = True

        # assume confirmed status
        order_status = confirmed_status

        # assume the order is going and not finished yet
        order_is_done = False

        # track the order
        while not order_is_done:
            # prompt the user to select his item
            selected_item = self.valid_input("Which product # do you want? ", options)

            # If the user enters an empty text, it indicates that the order has been completed
            # and the purchasing process was successful.
            if selected_item == "":
                order_is_done = True
                continue

            # If the user enters "0", it indicates that the order has been cancelled,
            # and the purchasing process has been ignored.
            if selected_item == "0":
                order_status = cancelled_status
                order_is_done = True
                continue

            # if the order is not cancelled, move on ask for the quantity
            # find the index of the selected item
            selected_index = int(selected_item) - 1

            # find the maximum available quantity
            max_num = items_list[selected_index].quantity

            while True:
                # Validate the entered range of quantity.
                quantity = self.valid_range("What amount do you want? ", range(1, max_num))
                # if quantity is zero then cancel the current process and ignore it.
                if quantity == 0:
                    # is_accepted = True
                    order_status = cancelled_status
                    order_is_done = True
                    break
                if quantity == -6:
                    order_status = confirmed_status
                    order_is_done = True
                    # print("Salman it is = -6")
                    break
                # Try to add this item to the order.
                success, qty_to_adjust = self.add_product_to_order(items_list[selected_index].name,
                                                                   quantity, order_list)

                # Determine if the entered quantity exceeds the available range.
                if qty_to_adjust > 0:
                    max_num = quantity - qty_to_adjust
                    if max_num == 0:
                        # print(f"No more items available from {items_list[selected_index].name}")
                        print(f"The {items_list[selected_index].name} is currently out of stock.")
                        print(f"{items_list[selected_index].name} item is deactivated!")
                        break
                    print("--- The available quantity for purchase is insufficient, "
                          f"with a maximum limit of {max_num} units. ---")
                    continue

                # if every thing went smoothly,it indicates that the process has been accepted
                # and successful
                if success and qty_to_adjust == 0:
                    # is_accepted = True
                    print(f"  <---- You have successfully added {quantity} of "
                          f"{items_list[selected_index].name}"
                          " to your order. ---->")
                    self.purchased_list = order_list
                    break

            print("")
        # If the order is finalized, proceed with generating a summary or bill
        # for the completed order
        if order_status == confirmed_status:
            # total_price = self.order(order_list)
            print("--- Order confirmed ---")
            print("You have purchased the following items:")
            self.display_order_summary(order_list, self.order(order_list))
        # self.purchased_list = order_list
        else:
            # Inform the customer that the order has been cancelled
            print("--- Order cancelled ----")

    def find_product_by_name(self, product_name: str) -> Optional[Product]:
        """
		Finds a product by its name

		:return: (Product) Return the product if found; otherwise, return None
		"""
        for product in self.products_list:
            if product.name == product_name:
                return product
        return None

    def add_product_to_order(self, product_name, req_quantity, lst: List[Tuple[str, int]]) -> Tuple:
        """
		Adds a product to the order list.

		:param: product_name (str): The name of the product.
		:param: req_quantity (int): The requested quantity of the product.
		:param:lst (List[Tuple[str, int]]): The order list as a list of tuples.

		:return: Tuple[bool, int]: A tuple containing the success status of adding the product
									(True if successful, False otherwise) and the quantity
									difference if there is insufficient quantity
									(positive value indicating the shortage)
		"""
        product = self.find_product_by_name(product_name)
        available_quantity = product.quantity
        for index, item in enumerate(lst):
            if item[0] == product_name:
                old_item = item
                old_quantity = old_item[1]
                if (old_quantity + req_quantity) > available_quantity:
                    return False, abs(available_quantity - old_quantity - req_quantity)
                item = (old_item[0], old_quantity + req_quantity)
                lst[index] = item
                # print(f"item = {item[0]} , {item[1]} ")
                # print(f"item = {lst[index][0]} , {lst[index][1]} ")
                return True, 0
        if req_quantity > available_quantity:
            return False, abs(available_quantity - req_quantity)
        lst.append((product_name, req_quantity))
        return True, 0

    @classmethod
    def generate_order_id(cls, num_cells: int):
        """
		Generates a random order ID with a fixed number of cell

		:return: (str) The generated random order ID
		"""
        chars = string.ascii_letters + string.digits
        order_id = "".join(random.choices(chars, k=num_cells)).upper()
        return order_id

    @staticmethod
    def display_order_summary(order_list: List[Product], total_price: float) -> None:
        """
		display_order_summary
		"""
        order_id = Store.generate_order_id(9)
        print(f"\n  <---- Order #{order_id} Summary ---->")
        print(" You have successfully purchased the following:")
        for index, item in enumerate(order_list, start=1):
            print(f"{index}. {item[0]} - Qty: {item[1]}")
        print("------------------------------------------")
        print(f"   Total price:         ${total_price}")

    def order(self, shopping_list: List[Tuple[str, int]]) -> float:
        """
		Place an order for a given shopping list and calculate the total price.

		:param: shopping_list:  (List[Tuple[Product, int]]): The shopping list containing
								the products and quantities
		:return: float: The total price of the order.
		"""
        total_price: float = 0.0
        for item in shopping_list:
            # product.quantity -= quantity
            for product in self.products_list:
                if product.name == item[0]:
                    total_price += product.buy(item[1])
                    break
        return total_price

    @staticmethod
    def valid_input(prompt, options):
        """
		Validates user input against a list of options.

		This function prompts the user with the given prompt and validates their input against
		the provided list of options. It continues to prompt the user until a valid option is entered.

		:param prompt: (str) The prompt to display to the user.
		:param options: (list) A list of valid options.
		:return: (str) The user's input, which is a valid option.
		"""
        while True:
            option = input(prompt).lower()
            if option in options:
                return option
            print(f"\n*** Sorry, the option {option} is invalid. Try again! ***\n")

    @staticmethod
    def valid_range(prompt: str, the_range: range) -> int:
        """
        Validates user input against a list of options.

        This function prompts the user with the given prompt and validates their input against
        the provided list of options. It continues to prompt the user until a valid option
        is entered.

        :param prompt: (str) The prompt to display to the user.
        :param the_range:
        :return: (str) The user's input, which is a valid option.
        """
        start = the_range.start
        end = the_range.stop
        while True:
            option = input(prompt).lower()
            if option == "0":  # == "0" or option == "":
                return 0
            if option == "":
                return -6
            if option.isdigit():
                if start <= int(option) <= end:
                    return int(option)
            print(f"\n*** Sorry, the option {option} is invalid. Maximum available quantity is "
                  f"({end}) Try again! ***\n")
