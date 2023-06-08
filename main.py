# ==========================================================================
#						          Best Buy
# Implementation of a store application. The code consist manily of 3 files
# main.py, products.py and sotre.py, main.py defines the main functions to
# interact with the store via command dispatcher,
# allowing the customer to add product, place an order,
# and display information about available products and quantities.
#
# The program uses the 'Product' and 'Store' classes from the 'products'
# and 'store' modules.
#
# It starts by creating a list of available products and initializing a
# 'Store' instance named 'best_buy' with this list Then, the 'start'
# function is called to begin the store application, allowing the user to
# interact with the store and perform various actions.
#
# Features:
#	1- Customers have the option to add multiple products to a list,
#	and they can make a purchase for the entire list at once.
#
#	2- Customers can repeatedly add the same items to the list as long as
#	there is available quantity.
#
#	3- Customers have the flexibility to cancel the order at any time
#	before proceeding to checkout.
#
#	4- The program generates a summary of the order, including an order ID,
#	the summary displays the items purchased by the customer along with
#	their respective quantities and the total price - like a bill.
#
#	5- The program effectively handles all potential errors and provides
#	appropriate responses. It displays clear and informative messages that
#	explain what is happening and guide the user in understanding the situation.
#
# The code is well-organized and modularized,
# adhering to the PEP8 guidelines for Python coding style
# ==========================================================================
"""
main.py
This module provides the main functionality for the store application.

It creates a list of available products, initializes a Store instance with the product list,
and starts the store application by calling the 'start' function with the Store instance.

Usage:
    Run this module directly to start the store application.

Author:
    Salman Farhat

Date:
    [2023-06-01]
"""
from products import Product
from store import Store


def start(store: Store):
    """
    Starts the store application and allows interaction with the store.

    :param: store (Store): The Store instance to be used.
    """
    # the_store
    commands = {"1": store.display_products_list,
                "2": store.display_total_quantity,
                "3": store.place_order
                }

    # assuming we are not done.
    # exit will be from within the loop
    done: bool = False
    while not done:
        store.display_store_menu()

        choice = input("\nPlease choose a number (1, 2, 3 or 4):>")

        if choice == "4":
            done = True
            continue

        if choice in commands:
            commands[choice]()
        else:
            print("\n  Please provide a valid input. Only values of 1, 2, 3, or 4 are allowed.")

    print("Thank you for shppoing with us, Wish you a fantastic day!"
          "We look forward to serving you again in the future.\n")


def main():
    """
    Main function to start the store application.
    """
    # Create a list of Product instances representing available products in the store
    product_list = [
        Product("MacBook Air M2", price=1450, quantity=100),
        Product("Bose QuietComfort Earbuds", price=250, quantity=500),
        Product("Google Pixel 7", price=500, quantity=250)
    ]

    # Create a Store instance named 'best_buy' using the 'product_list'
    best_buy = Store(product_list)
    # Start the store application by calling the 'start' function with the 'best_buy' store instance
    start(best_buy)


if __name__ == "__main__":
    main()
