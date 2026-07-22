# Final Furniture Stock Management System
# Scenario: Home Furniture Retail Store

from furniture import Sofa, Table, Wardrobe
from stock_manager import StockManager


def build_initial_inventory():
    """Create the starting furniture inventory for the retail store."""

    store = StockManager()

    furniture_items = [
        Sofa(
            "F001",
            "Corner Sofa",
            699.00,
            8,
            5
        ),
        Table(
            "F002",
            "Oak Dining Table",
            599.00,
            10,
            "Oak"
        ),
        Wardrobe(
            "F003",
            "Three-Door Wardrobe",
            799.00,
            2,
            3
        ),
        Sofa(
            "F004",
            "Two-Seater Sofa",
            449.00,
            3,
            2
        )
    ]

    for furniture in furniture_items:
        success, message = store.add_furniture(furniture)
        print(message)

    return store


def main():
    """Run the final furniture stock management demonstration."""

    print("=" * 70)
    print("HOME FURNITURE RETAIL STORE")
    print("FURNITURE STOCK MANAGEMENT SYSTEM")
    print("=" * 70)

    store = build_initial_inventory()

    # -----------------------------------------------------
    # 1. DISPLAY CURRENT INVENTORY
    # -----------------------------------------------------

    print()
    print(store.generate_report())

    # -----------------------------------------------------
    # 2. SEARCH INVENTORY
    # -----------------------------------------------------

    print("\nSEARCH RESULTS FOR 'SOFA'")
    print("-" * 70)

    search_results = store.search_inventory("sofa")

    for item in search_results:
        print(item.display_details())

    # -----------------------------------------------------
    # 3. CATEGORY REPORT
    # -----------------------------------------------------

    print()
    print(store.generate_category_report("Sofas"))

    # -----------------------------------------------------
    # 4. ALLOCATE EXISTING FURNITURE STOCK
    # -----------------------------------------------------

    print("\nSTOCK ALLOCATION")
    print("-" * 70)

    success, message = store.allocate_stock(
        "F001",
        3
    )

    print(message)

    # -----------------------------------------------------
    # 5. UPDATE STOCK
    # -----------------------------------------------------

    print("\nNEW STOCK DELIVERY")
    print("-" * 70)

    success, message = store.update_stock(
        "F003",
        5
    )

    print(message)

    # -----------------------------------------------------
    # 6. FINAL UPDATED INVENTORY REPORT
    # -----------------------------------------------------

    print()
    print(store.generate_report())


if __name__ == "__main__":
    main()