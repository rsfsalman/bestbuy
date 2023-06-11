# ==========================================================================
#						          Best Buy
# Implementation of a store application. The code consist mainly of 4 files
# main.py, products.py, store.py and promotions.py, main.py defines the main
# functions to interact with the store via command dispatcher,
# allowing the customer to add product, place an order,
# and display information about available products and quantities.
# Unit testing was added to the project, you can find it in 'test_products.py'
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
#   6-  a). The program offers 3 exciting promotions feature, and these are:
#       Second Half Price: With this promotion, when you purchase two identical items, you will
#       receive a 50% discount on the second item. This allows you to enjoy significant savings
#       while stocking up on your favorite products.
#
#       b). Third Item is Free: This promotion rewards your loyalty by offering a complimentary item
#       for every two items you purchase. When you add three identical items to your cart, the
#       system automatically deducts the price of the third item, making it absolutely free. It's a
#       great way to get more value from your purchases.
#
#       c). 30% Discount: The third promotion provides a generous 30% discount on eligible items.
#
#   7- Unit testing: Unit testing is a crucially implemented feature in the BestBuy program,
#   aiming to ensure the program's reliability and correctness.
#   The pytest framework is utilized to create a comprehensive suite of unit tests that
#   specifically target the behavior of the Product class.
#   These tests cover a wide range of scenarios, including creating products with valid and invalid parameters,
#   handling edge cases, and verifying the expected behavior of the product's functionality.
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
from products import Product, NonStockedProduct, LimitedProduct
from store import Store
import promotions


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
    print("Welcome to our store! We are delighted to have you here.\n"
          "Start exploring our wide range of products and enjoy your shopping experience.")
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

    print("Thank you for shopping with us, Wish you a fantastic day!"
          " We look forward to serving you again in the future.\n")


def main():
    """
    Main function to start the store application.
    """
    # Create a list of Product instances representing available products in the store
    product_list = [
        Product("MacBook Air M2", price=1450, quantity=100),
        Product("Bose QuietComfort Earbuds", price=250, quantity=500),
        Product("Google Pixel 7", price=500, quantity=250),
        NonStockedProduct("Windows License", price=125),
        LimitedProduct("Shipping", price=10, quantity=250, limit=1)
    ]

    # Create promotion catalog
    second_half_price = promotions.SecondHalfPrice("Second Half price!")
    third_one_free = promotions.ThirdOneFree("Third One Free!")
    thirty_percent = promotions.PercentDiscount("30% off!", percent=30)

    product_list[0].set_promotion(second_half_price)
    product_list[1].set_promotion(third_one_free)
    product_list[3].set_promotion(thirty_percent)

    # Create a Store instance named 'best_buy' using the 'product_list'
    best_buy = Store(product_list)
    # Start the store application by calling the 'start' function with the 'best_buy' store instance
    start(best_buy)


if __name__ == "__main__":
    main()
