# Inventory Manager
The following application is an inventory manager. It is a light solution that only relies on a correctly formatted text file (.txt)

## Requirements
- Python 3.10+
    - Tabulate module
- Git

## Installation
The following steps are required to run this program:
1. Install the latest release of python3 from the official website: https://www.python.org/downloads/
2. Install the 'tabulate' module in your terminal/cmd with the following command:
    1. `pip install tabulate`
3. Install Git from the official source (select a version appropriate for your operating system; Windows, MacOS etc.): https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
4. From your terminal/cmd, clone the repository to your working directory with the following command:
    1. `git clone https://github.com/jigypeper/finalCapstone.git`
5. Run the program from the Terminal with the following steps:
    1. Open Terminal
    2. Change directory (cd) to the folder containing the 'inventory.py' file
    3. type `python3 inventory.py` and press enter to run the program

## How to use
The program initially reads from the file that comes in the repository 'inventory.txt'. Feel free to overwrite all the data from line 2 onwards. For the program to work as intended it must adhere to the same data structure (with no spaces):  
`Country,Code,Product,Cost,Quantity`  

Alternatively, it is possible to create a new inventory file by using the 'add shoe functionality' on first launch (if the inventory.txt is moved elsewhere).  
  
Note: it is important that the cost data is entered as either an integer or floating point number (decimal), and the quantity is entered as an integer. If these conditions are not met, the program will warn you and not gather the data from the file.
