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
from products import Product, NonStockedProduct, LimitedProduct


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


def find_quantity_of_added_item(lst, product_name):
    """
    Search for a specific product by its name and returns the quantity that has been ordered

    :param lst: (list) The order list, a list of tuples containing product name and its quantity.
    :param product_name: (str) The name of the product to search for in the list.

    :return: int: The quantity of the product that has been ordered if found, -1 otherwise.
    """
    for name, items_count in lst:
        if name == product_name:
            return items_count
    return -1


def display_limit_message(product_limit, product_name):
    """
    Displays a limit message indicating the maximum allowed quantity for a product.

    :param product_limit: (int): The maximum allowed quantity for the product.
    :param product_name: (str): The name of the product.
    :return: None
    """
    if product_limit == 1:
        print(f"Sorry, Only {product_limit} unit is allowed from {product_name}.")
    else:
        print(f"Sorry, Only {product_limit} units are allowed from {product_name}.")


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
    # The maximum number of items allowed as per the policy
    OUR_POLICY_MAX_ALLOWED_ITEMS = 10000

    def __init__(self, products):
        """
		Initialize the Store object.

		:param products: (list): A list of Product instances to be added to the store.
		"""
        self.products_list: List[Product] = products
        self.purchased_list = []
        self.order_list = []

    def __contains__(self, product):
        """
         The __contains__ method checks if a product exists in the store.

        :param product: (Product) The product to check.
        :return: (bool) True if the product exists in the store, False otherwise
        """
        return product in self.products_list

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
        active_products: List[Product] = []
        for product in self.products_list:
            if product.is_active():
                active_products.append(product)

        if display_flag:
            print("\n------- Available Items -------")
            for index, product in enumerate(active_products, start=1):
                # print(f"{index}. {product.name}, Price: ${product.price}, "
                #       f"Quantity: {product.quantity}")
                print(f"{index}.", product)
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
		Initializes the order list.

        This method is used to create an empty order list when it's first initialized

		:return: (list): An empty order list.
		"""
        # if len(self.purchased_list) > 0:
        # 	return self.purchased_list
        self.purchased_list = []
        return []

    def specify_product_quantity(self, max_num, selected_index, items_list, order_list):
        """
        Allows the user to specify the quantity to add to the order.

        :param max_num: (int): The maximum allowed quantity for the selected product.

        :param selected_index: The index of the selected product in the items_list
        :param items_list: A list of available products
        :param order_list: The current order list

        :return:
            tuple: A tuple containing the order status (True for confirmed, False for cancelled) and
               a flag indicating whether the order is completed (True) or still ongoing (False).
        """
        # reference status to indicate order status
        cancelled_status = False
        confirmed_status = True

        # assume confirmed status
        order_status = confirmed_status
        order_is_done = False

        while True:
            # Validate the entered range of quantity.
            stoked_item = isinstance(items_list[selected_index], NonStockedProduct)

            if stoked_item:
                previously_added_quantity = \
                    find_quantity_of_added_item(order_list, items_list[selected_index].name)
            else:
                previously_added_quantity = -1  # we don't care if it is non stocked items
            quantity = self.valid_range("What amount do you want? ", range(1, max_num), stoked_item,
                                        previously_added_quantity)

            if isinstance(items_list[selected_index], LimitedProduct):
                temp_product: LimitedProduct = items_list[selected_index]
                if quantity > temp_product.get_limit():
                    display_limit_message(temp_product.limit, items_list[selected_index.name])
                    continue

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
            if quantity == -1:
                continue

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
        return order_status, order_is_done

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
            # print(type(items_list[selected_index]))
            if isinstance(items_list[selected_index], NonStockedProduct):
                # Ensure that the maximum number of items does not exceed the policy limit
                max_num = Store.OUR_POLICY_MAX_ALLOWED_ITEMS
                # print(max_num)
            order_status, order_is_done = self.specify_product_quantity(max_num, selected_index,
                                                                        items_list, order_list)
            print("")
        # If the order is confirmed, proceed to generate a summary or bill
        # for the completed order
        if order_status == confirmed_status:
            # total_price = self.order(order_list)
            if len(order_list) > 0:
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
        if isinstance(product, NonStockedProduct):
            available_quantity = 2 ** 32

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
        Displays the order summary.

        :param order_list: (List[Product]): A list of products in the order, along with
                            their quantities
        :param total_price: The total price of the order
        :return: None
        """
        order_id = Store.generate_order_id(9)
        print(f"\n  <---- Order #{order_id} Summary ---->")
        print(" You have successfully purchased the following:")
        for index, obj in enumerate(order_list, start=1):
            print(f"{index}. {obj[0].ljust(18)} - Qty: {obj[1]}")
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
                    _, price = product.buy(item[1])
                    total_price += price
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
    def valid_range(prompt: str, the_range: range, non_stocked_product: bool,
                    previously_added_quantity: int) -> int:
        """
        Validates and returns a quantity within the specified range.

        This method prompts the user with the given prompt and validates their input against
        the available quantity of the selected product.
        It repeatedly prompts the user until a valid quantity is entered.

        :param prompt: (str) The prompt to display to the user.
        :param the_range: The range of valid values for the quantity.
        :param non_stocked_product: (bool) Indicates whether the product is non-stocked
        :param previously_added_quantity: The quantity of the product previously
                added to the order.

        :return: (int) The validated quantity within the specified range.
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
                    if non_stocked_product:
                        # print("Already added = ", items_allready_added)
                        if previously_added_quantity > -1:
                            max_items = end - previously_added_quantity
                        else:
                            max_items = end
                        if int(option) > max_items:
                            print("\n*** Sorry, we have a policy in place that restricts the number"
                                  " of non stocked "
                                  f"items per order to a maximum of {end} units.\nSince you have"
                                  " already purchased "
                                  f"{previously_added_quantity} items, you can still buy an "
                                  f"additional {max_items} within"
                                  " the allowed limit")
                            return -1
                    return int(option)

                if non_stocked_product:
                    print("\n*** Sorry, we have a policy in place that restricts the"
                          " number of non stocked "
                          f"items per order to a maximum of {end} units.")
                else:
                    print(f"\n*** Sorry, the option {option} is invalid. Maximum available"
                          f" quantity is ({end}) Try again! ***\n")
            else:
                print("*** Invalid option.*** Make sure to enter numeric values between"
                      f" {start, end}")
