FURNITURE STOCK MANAGEMENT SYSTEM
Home Furniture Retail Store

PROJECT OVERVIEW
This Python program was developed for a home furniture retail store to manage furniture stock accurately and efficiently.

The system manages furniture products including sofas, dining tables and wardrobes. It supports stock allocation, stock updates, inventory searching, category filtering, low-stock monitoring and inventory-value reporting.

MAIN FEATURES
- Add furniture products to inventory
- Validate furniture IDs, names, prices and quantities
- Prevent duplicate furniture IDs
- Search furniture by ID, name or category
- Filter furniture by category
- Allocate furniture stock safely
- Prevent allocation above available stock
- Record new stock deliveries
- Identify low-stock furniture
- Calculate individual stock values
- Calculate total inventory value
- Generate furniture inventory reports
- Generate category-specific reports

OBJECT-ORIENTED PROGRAMMING
The solution uses object-oriented programming.

FurnitureItem is the parent class.

The following specialised furniture classes inherit from FurnitureItem:
- Sofa
- Table
- Wardrobe

These classes demonstrate inheritance and polymorphism while storing furniture-specific information such as seating capacity, table material and number of wardrobe doors.

PROJECT FILES
furniture.py
Contains the FurnitureItem, Sofa, Table and Wardrobe classes.

stock_manager.py
Contains inventory management, validation, searching, allocation, stock updates, calculations and reporting functions.

main.py
Runs the final Home Furniture Retail Store Stock Management System and demonstrates its main functionality.

Tests/test_furniture_system.py
Contains automated pytest tests covering TC01-TC18.

RUNNING THE PROGRAM
Open a terminal in the project folder and enter:

python main.py

RUNNING AUTOMATED TESTS
Enter:

python -m pytest Tests/test_furniture_system.py -v

TESTING RESULT
18 formal automated test cases were executed successfully.

Result:
18/18 tests passed.

The tests cover valid and invalid furniture records, duplicate IDs, empty names, negative values, stock allocation, boundary conditions, searching, stock updates, reporting, low-stock detection, stock-value calculations and category filtering.

SCENARIO
This solution is specifically designed for the Home Furniture Retail Store stock-management scenario. The product classes, sample furniture records, stock rules, low-stock alerts, inventory calculations and reports are all based on furniture retail operations.