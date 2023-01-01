"""
Note: run 'pip install tabulate' from the terminal or command line, otherwise you will have errors running this app
This is an inventory program that handles and updates data from an external data source.
The program displays large data sets to the user in an easy to read tabular format.
"""

from tabulate import tabulate


class Shoe:
    # constructor for shoes (requires country, code, product, cost, quantity)
    def __init__(self, country: str, code: str, product: str, cost: float, quantity: int):
        self.country: str = country
        self.code: str = code
        self.product: str = product
        self.cost: float = cost
        self.quantity: int = quantity

    def get_cost(self):
        # returns the cost of the shoe object.
        return self.cost

    def get_quantity(self):
        # returns the quantity of the shoe object.
        return self.quantity

    def __str__(self):
        # returns the string representation of the shoe object.
        return f"""Shoe Object
---------------------------
Product:        {self.product}
Country:        {self.country}
Product Code:   {self.code}
Cost:           {self.cost}
Quantity:       {self.quantity}
---------------------------
"""

    def __eq__(self, other):
        # checks equality of shoes
        if (self.country == other.country) and (self.code == other.code) and (self.product == other.product) and \
                (self.cost == other.cost):
            return True
        else:
            return False


# =============Shoe list===========

# list to store a list of objects of shoes
shoe_list = []


# ==========Functions outside the class==============
def read_shoes_data():
    """
    This function will open the file inventory.txt
    and read the data from this file, then create a shoes object with this data
    and append this object into the shoes list.
    """
    # clear the shoe list dictionary to prevent appending endlessly to list
    shoe_list.clear()

    try:
        with open(file="./inventory.txt", mode="r") as inventory_file:
            # get data from inventory file (from second line onwards)
            inventory_data_import = inventory_file.readlines()[1:]

            # list comprehension to split data on "," and create a list of lists
            inventory_data_structured = [
                line.split(",") for line in inventory_data_import
            ]

            # loop through structured data list, enumerate for error messages (to show which line might have an error)
            for i, item in enumerate(inventory_data_structured):
                # declare variables to store aspects of shoe class for readability
                country = item[0]
                code = item[1]
                product = item[2]
                cost = float(item[3])
                quantity = int(item[4])

                # create a shoe object from the data and append to the shoe list
                shoe = Shoe(country, code, product, cost, quantity)
                shoe_list.append(shoe)

            # display complete message
            print("\nThe inventory list has been initialised from the file 'inventory.txt'\n")

    except FileNotFoundError:
        print("The inventory.txt file is either missing\nor not in the same folder as this program\n")
    except IndexError:
        # line number is i + 2, because first line is column headers, and count starts at 1 for humans.
        print(f"Line {i + 2} in the inventory.txt file is formatted incorrectly\n(too few data points)\n")
    except ValueError:
        # line number is i + 2, because first line is column headers, and count starts at 1 for humans.
        print(f"The cost or quantity on Line {i + 2} in the inventory.txt file is formatted "
              f"incorrectly\n(could be missing or not typed as a number)\n")


def update_inventory():
    """
    This function updates the inventory
    """
    # declare variable to write (initialize with column titles)
    write_data = "Country,Code,Product,Cost,Quantity\n"

    # loop through shoe list, concatenate the write_data variable with shoe data (in same order as source)
    for i, item in enumerate(shoe_list):
        write_data += f"{item.country},{item.code},{item.product},{item.cost},{item.quantity}\n"
        # check if it is last item, if not add new line (\n)
        # if i != len(shoe_list) - 1:
        #     write_data += f"{item.country},{item.code},{item.product},{item.cost},{item.quantity}\n"
        # else:
        #     write_data += f"{item.country},{item.code},{item.product},{item.cost},{item.quantity}"

    # open the inventory file in write mode (will overwrite the data), write the string to the file
    with open(file="./inventory.txt", mode="w") as updated_inventory_file:
        updated_inventory_file.write(write_data)


def capture_shoes():
    """
    This function will allow a user to capture data
    about a shoe and use this data to create a shoe object
    and append this object inside the shoe list.
    It will update the quantity of the shoe if the shoes are equal.
    A new inventory file will be created if one doesn't exist.
    """
    try:
        # declare variables to store aspects of shoe class
        country = input("Enter the country: ")
        code = input("Enter the code: ").upper()
        product = input("Enter the product: ")
        cost = float(input("Enter the cost: "))
        quantity = int(input("Enter the quantity: "))

        # create an instance of the shoe with user defined parameters
        new_shoe = Shoe(country, code, product, cost, quantity)

        # declare boolean for deciding if the shoe needs adding to list
        shoe_exists = False

        # loop through list of shoes and check for equality,
        for shoe in shoe_list:
            # if equal increment quantity by new_shoe quantity
            if shoe == new_shoe:
                shoe.quantity += new_shoe.quantity

                # change shoe exists to true
                shoe_exists = True

        # if shoe doesn't exist, add to the list
        if not shoe_exists:
            shoe_list.append(new_shoe)

    except ValueError:
        # display message to user
        print("The cost or quantity is formatted incorrectly\n(make sure you typed a number)\n")
    finally:
        # print a new line and update the inventory
        print("\n")
        update_inventory()


def view_all():
    """
    This function will iterate over the shoes list and
    print the details of the shoes in a table format
    using Python’s tabulate module.
    """

    # nested list comprehension to get list containing lists of shoe object data
    table = [
        [
            shoe_object.country,
            shoe_object.code,
            shoe_object.product,
            shoe_object.cost,
            shoe_object.quantity
         ] for shoe_object in shoe_list
    ]

    # print a table with the tabulate module including headers
    print("\n", tabulate(table, headers=["Country", "Code", "Product", "Cost", "Quantity", "Cost"]), "\n")


def re_stock():
    """
    This function will find the shoe object with the lowest quantity,
    which is the shoes that need to be re-stocked. Ask the user if they
    want to add this quantity of shoes and then update it (in the inventory file also)
    """

    # list comprehension to get list of quantities for each item
    quantities = [
        shoe.quantity for shoe in shoe_list
    ]

    # find the minimum
    min_qty = min(quantities)

    try:
        # loop through list and update all shoes who's qty is equal to the minimum
        # this is for the case that multiple shoes have the same quantity
        for shoe in shoe_list:
            if shoe.quantity == min_qty:
                # display shoe with low stock details.
                print(f"\n{shoe.product}({shoe.code}) has a low stock: {shoe.quantity}\n")

                # ask user for re-stocking option
                order_qty = input("Would you like to order the standard "
                                  "amount (20) or a custom amount? (enter s or c)\n> ").lower()

                # match on order_qty response
                match order_qty:
                    case "s":
                        # increment the quantity by 20
                        shoe.quantity += 20
                    case "c":
                        # ask how many to order and cast to integer, increment shoe quantity by custom quantity
                        custom_qty = int(input("How many would you like to order (enter digits)? "))
                        shoe.quantity += custom_qty
                    case _:
                        print("\nYou haven't made a valid selection.\n")
    except ValueError:
        print("\nYou have not entered a valid number, please try again.\n")

    # update the inventory
    update_inventory()


def search_shoe():
    """
     This function will search for a shoe from the list
     using the shoe code and return this object so that it will be printed.
    """

    # dictionary comprehension to create dictionary with product code as key and shoe object as value
    shoe_dictionary = {
        shoe.code: shoe for shoe in shoe_list
    }

    # loop until correct product code entered
    while True:

        # ask for code, upper for error handling
        code = input("\nEnter a code for the shoe you would\nlike details of (or 'Q' to quit): ").upper()

        # check if the code is in the dictionary, back to top of loop if it isn't, print shoe if it is
        if code not in shoe_dictionary and code != "Q":
            print("\nThat is an invalid shoe code, please try again.")
            continue
        elif code == "Q":
            break
        else:
            print("\n", shoe_dictionary[code], "\n")
            break


def value_per_item():
    """
    This function will calculate the total value for each item.
    It uses pythons tabulate module to organise the data
    """
    # nested list comprehension to get list containing lists of product and calculated value
    # with formula: value = cost * quantity
    table = [
        [
            shoe_object.product,
            round(shoe_object.cost * shoe_object.quantity, 2)

        ] for shoe_object in shoe_list
    ]

    # print a table with the tabulate module including headers
    print("\n", tabulate(table, headers=["Product", "Value"]), "\n")


def highest_qty():
    """
    Determines the product with the highest quantity.
    """

    # list comprehension to generate a list of tuples (quantity, product)
    product_quantities = [
        (shoe.quantity, shoe.product) for shoe in shoe_list
    ]

    # sort the list in reverse (this is why quantity is the first element in the tuple)
    product_quantities.sort(reverse=True)

    # display the first item (the highest quantity) and that its on sale
    print(f"\n{product_quantities[0][1]} has the highest stock ({product_quantities[0][0]}), and is on sale\n")


# ==========Main Menu=============

# initialize a variable to check if the shoe list has been populated
shoe_list_populated: bool = False

# display welcome message
print("Welcome to the inventory application!\n====================================")

# loop until user exits the program
while True:
    # ask user for input, lower for error handling
    choice = input("""What would you like to do?
====================================
r   -   Read the shoe data
cs  -   Add Shoes to inventory
va  -   View all Shoes in Inventory
vp  -   View value per item
hq  -   See sale item
s   -   Search for a shoe
rs  -   Re-Stock
q   -   Quit
------------------------------------
> """).lower()

    # check shoe list is populated, if not, run read shoe data function
    if not shoe_list_populated:
        read_shoes_data()
        shoe_list_populated = True

    # match on the user choice
    match choice:
        case "r":
            # run read shoe data function
            read_shoes_data()
        case "cs":
            # run capture shoe function
            capture_shoes()
        case "va":
            # run view all function
            view_all()
        case "vp":
            # run value per item function
            value_per_item()
        case "hq":
            # run highest quantity function
            highest_qty()
        case "s":
            # run search for shoe function
            search_shoe()
        case "rs":
            # run the restocking function
            re_stock()
        case "q":
            # quit the program
            print("\nGoodbye!")
            exit()
        case _:
            # show message
            print(f"\n'{choice}' is not a valid choice! Please try again.\n")
