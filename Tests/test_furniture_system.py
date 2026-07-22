# Automated tests for the Home Furniture Retail Store
# Furniture Stock Management System

import os
import sys

# Allow tests to import files from the main project folder
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from furniture import Sofa, Table, Wardrobe
from stock_manager import StockManager


def create_test_store():
    """Create fresh furniture inventory for each test."""

    store = StockManager()

    store.add_furniture(
        Sofa("F001", "Corner Sofa", 699.00, 8, 5)
    )

    store.add_furniture(
        Table("F002", "Oak Dining Table", 599.00, 10, "Oak")
    )

    store.add_furniture(
        Wardrobe("F003", "Three-Door Wardrobe", 799.00, 2, 3)
    )

    return store


def test_tc01_add_valid_furniture():
    """TC01 - Valid furniture is added successfully."""

    store = StockManager()

    success, message = store.add_furniture(
        Sofa("F001", "Corner Sofa", 699.00, 8, 5)
    )

    assert success is True
    assert len(store.inventory) == 1
    assert "added successfully" in message


def test_tc02_duplicate_furniture_id():
    """TC02 - Duplicate furniture IDs are rejected."""

    store = create_test_store()

    success, message = store.add_furniture(
        Sofa("F001", "Duplicate Sofa", 500.00, 4, 4)
    )

    assert success is False
    assert message == "Furniture ID already exists."


def test_tc03_empty_furniture_name():
    """TC03 - Empty furniture names are rejected."""

    store = StockManager()

    success, message = store.add_furniture(
        Sofa("F009", "", 499.00, 4, 3)
    )

    assert success is False
    assert message == "Furniture name cannot be empty."


def test_tc04_negative_price():
    """TC04 - Negative prices are rejected."""

    store = StockManager()

    success, message = store.add_furniture(
        Table("F005", "Invalid Table", -250.00, 5, "Oak")
    )

    assert success is False
    assert message == "Furniture price must be greater than 0."


def test_tc05_negative_quantity():
    """TC05 - Negative stock quantities are rejected."""

    store = StockManager()

    success, message = store.add_furniture(
        Wardrobe("F006", "Invalid Wardrobe", 650.00, -2, 2)
    )

    assert success is False
    assert message == "Furniture quantity cannot be negative."


def test_tc06_valid_stock_allocation():
    """TC06 - Valid allocation reduces furniture stock."""

    store = create_test_store()

    success, message = store.allocate_stock("F001", 3)

    sofa = store.find_by_id("F001")

    assert success is True
    assert sofa.quantity == 5
    assert "Remaining stock: 5" in message


def test_tc07_over_allocation():
    """TC07 - Allocation above available stock is rejected."""

    store = create_test_store()

    success, message = store.allocate_stock("F003", 10)

    wardrobe = store.find_by_id("F003")

    assert success is False
    assert wardrobe.quantity == 2
    assert "Insufficient stock" in message


def test_tc08_exact_stock_allocation():
    """TC08 - Allocating exact available quantity leaves zero."""

    store = StockManager()

    store.add_furniture(
        Sofa("F007", "Display Sofa", 399.00, 3, 2)
    )

    success, message = store.allocate_stock("F007", 3)

    sofa = store.find_by_id("F007")

    assert success is True
    assert sofa.quantity == 0


def test_tc09_zero_allocation():
    """TC09 - Zero allocation is rejected."""

    store = create_test_store()

    success, message = store.allocate_stock("F002", 0)

    assert success is False
    assert message == "Allocation quantity must be greater than 0."


def test_tc10_search_valid_furniture():
    """TC10 - Existing furniture can be found."""

    store = create_test_store()

    results = store.search_inventory("F001")

    assert len(results) == 1
    assert results[0].name == "Corner Sofa"


def test_tc11_search_unknown_furniture():
    """TC11 - Unknown furniture returns no search results."""

    store = create_test_store()

    results = store.search_inventory("F999")

    assert results == []


def test_tc12_update_stock():
    """TC12 - New furniture delivery updates quantity correctly."""

    store = create_test_store()

    success, message = store.update_stock("F003", 5)

    wardrobe = store.find_by_id("F003")

    assert success is True
    assert wardrobe.quantity == 7
    assert "New quantity: 7" in message


def test_tc13_generate_inventory_report():
    """TC13 - Inventory report includes furniture records."""

    store = create_test_store()

    report = store.generate_report()

    assert "HOME FURNITURE RETAIL STORE" in report
    assert "Corner Sofa" in report
    assert "Oak Dining Table" in report
    assert "Three-Door Wardrobe" in report


def test_tc14_low_stock_warning():
    """TC14 - Quantity below threshold is marked LOW STOCK."""

    store = create_test_store()

    wardrobe = store.find_by_id("F003")

    assert store.check_low_stock(wardrobe) == "LOW STOCK"


def test_tc15_low_stock_boundary():
    """TC15 - Quantity exactly 3 is marked LOW STOCK."""

    store = StockManager()

    item = Table(
        "F008",
        "Side Table",
        149.00,
        3,
        "Oak"
    )

    store.add_furniture(item)

    assert store.check_low_stock(item) == "LOW STOCK"


def test_tc16_stock_value_calculation():
    """TC16 - Furniture stock value is calculated correctly."""

    store = StockManager()

    sofa = Sofa(
        "F001",
        "Corner Sofa",
        699.00,
        5,
        5
    )

    value = store.calculate_stock_value(sofa)

    assert value == 3495.00


def test_tc17_filter_by_category():
    """TC17 - Category filtering returns matching furniture."""

    store = create_test_store()

    sofas = store.filter_by_category("Sofas")

    assert len(sofas) == 1
    assert sofas[0].category == "Sofas"


def test_tc18_category_report():
    """TC18 - Category report calculates furniture units."""

    store = create_test_store()

    store.add_furniture(
        Sofa("F004", "Two-Seater Sofa", 449.00, 3, 2)
    )

    report = store.generate_category_report("Sofas")

    assert "CATEGORY REPORT: SOFAS" in report
    assert "Corner Sofa" in report
    assert "Two-Seater Sofa" in report
    assert "Total Units: 11" in report


# ---------------------------------------------------------
# TC19 - SAVE INVENTORY TO CSV
# ---------------------------------------------------------

def test_tc19_save_inventory_to_csv(tmp_path):
    """TC19 - Furniture inventory can be saved to CSV."""

    store = StockManager()

    sofa = Sofa(
        "F001",
        "Corner Sofa",
        699.00,
        8,
        5
    )

    success, _ = store.add_furniture(sofa)

    assert success is True

    test_file = tmp_path / "furniture_inventory.csv"

    success, message = store.save_inventory_to_csv(
        str(test_file)
    )

    assert success is True
    assert test_file.exists()
    assert "saved successfully" in message.lower()


# ---------------------------------------------------------
# TC20 - LOAD INVENTORY FROM CSV
# ---------------------------------------------------------

def test_tc20_load_inventory_from_csv(tmp_path):
    """TC20 - Saved furniture inventory can be restored."""

    original_store = StockManager()

    original_store.add_furniture(
        Sofa(
            "F001",
            "Corner Sofa",
            699.00,
            8,
            5
        )
    )

    test_file = tmp_path / "furniture_inventory.csv"

    save_success, _ = original_store.save_inventory_to_csv(
        str(test_file)
    )

    assert save_success is True

    loaded_store = StockManager()

    load_success, _ = loaded_store.load_inventory_from_csv(
        str(test_file)
    )

    assert load_success is True
    assert len(loaded_store.inventory) == 1
    assert loaded_store.inventory[0].furniture_id == "F001"
    assert loaded_store.inventory[0].name == "Corner Sofa"
    assert loaded_store.inventory[0].quantity == 8


# ---------------------------------------------------------
# TC21 - MALFORMED CSV DATA HANDLED SAFELY
# ---------------------------------------------------------

def test_tc21_malformed_csv_handled_safely(tmp_path):
    """TC21 - Invalid CSV data does not crash the system."""

    test_file = tmp_path / "damaged_inventory.csv"

    test_file.write_text(
        "furniture_type,furniture_id,name,category,"
        "price,quantity,special_value\n"
        "Sofa,F999,Damaged Sofa,Sofas,"
        "INVALID_PRICE,5,3\n",
        encoding="utf-8"
    )

    store = StockManager()

    success, message = store.load_inventory_from_csv(
        str(test_file)
    )

    assert success is True
    assert len(store.inventory) == 0
    assert "1 invalid row(s) skipped" in message


# ---------------------------------------------------------
# TC22 - CSV SAVE AND LOAD ROUND TRIP
# ---------------------------------------------------------

def test_tc22_csv_persistence_round_trip(tmp_path):
    """TC22 - All furniture types survive save/load."""

    original_store = StockManager()

    original_store.add_furniture(
        Sofa(
            "F001",
            "Corner Sofa",
            699.00,
            8,
            5
        )
    )

    original_store.add_furniture(
        Table(
            "F002",
            "Oak Dining Table",
            599.00,
            10,
            "Oak"
        )
    )

    original_store.add_furniture(
        Wardrobe(
            "F003",
            "Three-Door Wardrobe",
            799.00,
            2,
            3
        )
    )

    test_file = tmp_path / "furniture_inventory.csv"

    save_success, _ = original_store.save_inventory_to_csv(
        str(test_file)
    )

    assert save_success is True

    restored_store = StockManager()

    load_success, _ = restored_store.load_inventory_from_csv(
        str(test_file)
    )

    assert load_success is True
    assert len(restored_store.inventory) == 3

    assert restored_store.find_by_id("F001").quantity == 8
    assert restored_store.find_by_id("F002").material == "Oak"
    assert restored_store.find_by_id("F003").number_of_doors == 3


# ---------------------------------------------------------
# TC23 - STOCK ALLOCATION CREATES AUDIT LOG
# ---------------------------------------------------------

def test_tc23_allocation_creates_audit_log(tmp_path):
    """TC23 - Successful allocation creates an audit record."""

    log_file = tmp_path / "stock_audit.log"

    store = StockManager(
        audit_log_path=str(log_file)
    )

    store.add_furniture(
        Sofa(
            "F001",
            "Corner Sofa",
            699.00,
            8,
            5
        )
    )

    success, _ = store.allocate_stock(
        "F001",
        3
    )

    assert success is True
    assert log_file.exists()

    log_content = log_file.read_text(
        encoding="utf-8"
    )

    assert "ALLOCATION" in log_content
    assert "F001" in log_content
    assert "Corner Sofa" in log_content
    assert "Allocated: 3" in log_content
    assert "Remaining stock: 5" in log_content


# ---------------------------------------------------------
# TC24 - STOCK UPDATE CREATES AUDIT LOG
# ---------------------------------------------------------

def test_tc24_stock_update_creates_audit_log(tmp_path):
    """TC24 - Successful stock delivery creates audit record."""

    log_file = tmp_path / "stock_audit.log"

    store = StockManager(
        audit_log_path=str(log_file)
    )

    store.add_furniture(
        Wardrobe(
            "F003",
            "Three-Door Wardrobe",
            799.00,
            2,
            3
        )
    )

    success, _ = store.update_stock(
        "F003",
        5
    )

    assert success is True
    assert log_file.exists()

    log_content = log_file.read_text(
        encoding="utf-8"
    )

    assert "STOCK UPDATE" in log_content
    assert "F003" in log_content
    assert "Three-Door Wardrobe" in log_content
    assert "Added: 5" in log_content
    assert "New stock: 7" in log_content