# Stock management logic for the Home Furniture Retail Store

import csv
import os
from datetime import datetime

from furniture import Sofa, Table, Wardrobe


class StockManager:
    """Manages furniture inventory for the home furniture retail store."""

    LOW_STOCK_THRESHOLD = 3

    def __init__(self, audit_log_path="data/stock_audit.log"):
        self.inventory = []
        self.audit_log_path = audit_log_path

    # ---------------------------------------------------------
    # AUDIT LOGGING
    # ---------------------------------------------------------

    def write_audit_log(self, action, item, details):
        """Record important furniture-stock operations with a timestamp."""

        try:
            log_directory = os.path.dirname(self.audit_log_path)

            if log_directory:
                os.makedirs(log_directory, exist_ok=True)

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            log_entry = (
                f"{timestamp} | "
                f"{action} | "
                f"{item.furniture_id} | "
                f"{item.name} | "
                f"{details}\n"
            )

            with open(
                self.audit_log_path,
                "a",
                encoding="utf-8"
            ) as log_file:
                log_file.write(log_entry)

            return True

        except OSError:
            # Stock operations should not crash if the audit file
            # cannot be written.
            return False

    # ---------------------------------------------------------
    # FURNITURE ENTRY AND VALIDATION
    # ---------------------------------------------------------

    def add_furniture(self, furniture):
        """Add validated furniture while preventing invalid records."""

        # Prevent duplicate furniture IDs
        for item in self.inventory:
            if item.furniture_id == furniture.furniture_id:
                return False, "Furniture ID already exists."

        # Validate required text
        if not furniture.furniture_id.strip():
            return False, "Furniture ID cannot be empty."

        if not furniture.name.strip():
            return False, "Furniture name cannot be empty."

        if not furniture.category.strip():
            return False, "Furniture category cannot be empty."

        # Validate numeric values
        if furniture.price <= 0:
            return False, "Furniture price must be greater than 0."

        if furniture.quantity < 0:
            return False, "Furniture quantity cannot be negative."

        self.inventory.append(furniture)

        return True, f"{furniture.name} added successfully."

    # ---------------------------------------------------------
    # SEARCHING AND FILTERING
    # ---------------------------------------------------------

    def search_inventory(self, search_term):
        """Search furniture by ID, partial name, or category."""

        search_term = search_term.strip().lower()

        if not search_term:
            return []

        return [
            item
            for item in self.inventory
            if (
                search_term in item.furniture_id.lower()
                or search_term in item.name.lower()
                or search_term in item.category.lower()
            )
        ]

    def filter_by_category(self, category):
        """Return furniture matching a selected category."""

        return [
            item
            for item in self.inventory
            if item.category.lower() == category.strip().lower()
        ]

    def find_by_id(self, furniture_id):
        """Return one furniture item using its exact ID."""

        furniture_id = furniture_id.strip().lower()

        for item in self.inventory:
            if item.furniture_id.lower() == furniture_id:
                return item

        return None

    # ---------------------------------------------------------
    # STOCK ALLOCATION
    # ---------------------------------------------------------

    def allocate_stock(self, furniture_id, requested_quantity):
        """Allocate furniture without allowing invalid stock changes."""

        item = self.find_by_id(furniture_id)

        if item is None:
            return False, "Furniture not found."

        if requested_quantity <= 0:
            return False, "Allocation quantity must be greater than 0."

        if requested_quantity > item.quantity:
            return (
                False,
                f"Insufficient stock. Only {item.quantity} unit(s) available."
            )

        item.quantity -= requested_quantity

        # Record successful furniture allocation in the audit log
        self.write_audit_log(
            "ALLOCATION",
            item,
            (
                f"Allocated: {requested_quantity} | "
                f"Remaining stock: {item.quantity}"
            )
        )

        return (
            True,
            f"Allocation successful: {item.name}. "
            f"Remaining stock: {item.quantity}"
        )

    # ---------------------------------------------------------
    # STOCK UPDATES / DELIVERIES
    # ---------------------------------------------------------

    def update_stock(self, furniture_id, additional_quantity):
        """Add newly received furniture stock."""

        item = self.find_by_id(furniture_id)

        if item is None:
            return False, "Furniture not found."

        if additional_quantity <= 0:
            return False, "Added quantity must be greater than 0."

        item.quantity += additional_quantity

        # Record successful furniture delivery in the audit log
        self.write_audit_log(
            "STOCK UPDATE",
            item,
            (
                f"Added: {additional_quantity} | "
                f"New stock: {item.quantity}"
            )
        )

        return (
            True,
            f"Stock updated: {item.name}. "
            f"New quantity: {item.quantity}"
        )

    # ---------------------------------------------------------
    # STOCK CALCULATIONS
    # ---------------------------------------------------------

    def calculate_stock_value(self, item):
        """Calculate the current value of one furniture product."""

        return item.price * item.quantity

    def calculate_total_inventory_value(self):
        """Calculate total value of all furniture inventory."""

        return sum(
            self.calculate_stock_value(item)
            for item in self.inventory
        )

    def check_low_stock(self, item):
        """Return stock status for one furniture product."""

        if item.quantity <= self.LOW_STOCK_THRESHOLD:
            return "LOW STOCK"

        return "IN STOCK"

    # ---------------------------------------------------------
    # INVENTORY REPORTING
    # ---------------------------------------------------------

    def generate_report(self):
        """Return a detailed furniture inventory report."""

        report_lines = [
            "HOME FURNITURE RETAIL STORE - INVENTORY REPORT",
            "-" * 95
        ]

        for item in self.inventory:
            stock_value = self.calculate_stock_value(item)
            status = self.check_low_stock(item)

            report_lines.append(
                f"{item.furniture_id} | "
                f"{item.name} | "
                f"{item.category} | "
                f"GBP {item.price:.2f} | "
                f"Qty: {item.quantity} | "
                f"Value: GBP {stock_value:.2f} | "
                f"{status}"
            )

        report_lines.append("-" * 95)

        report_lines.append(
            f"TOTAL INVENTORY VALUE: "
            f"GBP {self.calculate_total_inventory_value():.2f}"
        )

        return "\n".join(report_lines)

    def generate_category_report(self, category):
        """Return a report for one furniture category."""

        matches = self.filter_by_category(category)

        if not matches:
            return f"No furniture found in category: {category}"

        lines = [
            f"CATEGORY REPORT: {category.upper()}",
            "-" * 70
        ]

        total_units = 0

        for item in matches:
            lines.append(item.display_details())
            total_units += item.quantity

        lines.append("-" * 70)
        lines.append(f"Total Units: {total_units}")

        return "\n".join(lines)

    # ---------------------------------------------------------
    # CSV PERSISTENCE - SAVE INVENTORY
    # ---------------------------------------------------------

    def save_inventory_to_csv(
        self,
        file_path="data/furniture_inventory.csv"
    ):
        """Save the current furniture inventory to a CSV file."""

        file_directory = os.path.dirname(file_path)

        if file_directory:
            os.makedirs(file_directory, exist_ok=True)

        try:
            with open(
                file_path,
                "w",
                newline="",
                encoding="utf-8"
            ) as csv_file:

                writer = csv.writer(csv_file)

                writer.writerow(
                    [
                        "furniture_type",
                        "furniture_id",
                        "name",
                        "category",
                        "price",
                        "quantity",
                        "special_value"
                    ]
                )

                for item in self.inventory:

                    if isinstance(item, Sofa):
                        furniture_type = "Sofa"
                        special_value = item.seating_capacity

                    elif isinstance(item, Table):
                        furniture_type = "Table"
                        special_value = item.material

                    elif isinstance(item, Wardrobe):
                        furniture_type = "Wardrobe"
                        special_value = item.number_of_doors

                    else:
                        furniture_type = "FurnitureItem"
                        special_value = ""

                    writer.writerow(
                        [
                            furniture_type,
                            item.furniture_id,
                            item.name,
                            item.category,
                            item.price,
                            item.quantity,
                            special_value
                        ]
                    )

            return True, f"Inventory saved successfully to {file_path}."

        except OSError as error:
            return False, f"Unable to save inventory: {error}"

    # ---------------------------------------------------------
    # CSV PERSISTENCE - LOAD INVENTORY
    # ---------------------------------------------------------

    def load_inventory_from_csv(
        self,
        file_path="data/furniture_inventory.csv"
    ):
        """Load furniture inventory from a CSV file."""

        if not os.path.exists(file_path):
            return False, "Inventory CSV file was not found."

        loaded_inventory = []
        skipped_rows = 0

        try:
            with open(
                file_path,
                "r",
                newline="",
                encoding="utf-8"
            ) as csv_file:

                reader = csv.DictReader(csv_file)

                required_headers = {
                    "furniture_type",
                    "furniture_id",
                    "name",
                    "category",
                    "price",
                    "quantity",
                    "special_value"
                }

                if reader.fieldnames is None:
                    return False, "Inventory CSV file has no headers."

                if not required_headers.issubset(set(reader.fieldnames)):
                    return False, "Inventory CSV file has invalid headers."

                for row in reader:

                    try:
                        furniture_type = row[
                            "furniture_type"
                        ].strip()

                        furniture_id = row[
                            "furniture_id"
                        ].strip()

                        name = row[
                            "name"
                        ].strip()

                        price = float(
                            row["price"]
                        )

                        quantity = int(
                            row["quantity"]
                        )

                        special_value = row[
                            "special_value"
                        ].strip()

                        if furniture_type == "Sofa":
                            item = Sofa(
                                furniture_id,
                                name,
                                price,
                                quantity,
                                int(special_value)
                            )

                        elif furniture_type == "Table":
                            item = Table(
                                furniture_id,
                                name,
                                price,
                                quantity,
                                special_value
                            )

                        elif furniture_type == "Wardrobe":
                            item = Wardrobe(
                                furniture_id,
                                name,
                                price,
                                quantity,
                                int(special_value)
                            )

                        else:
                            skipped_rows += 1
                            continue

                        # Reuse existing validation before accepting loaded data
                        temp_manager = StockManager(
                            audit_log_path=self.audit_log_path
                        )

                        temp_manager.inventory = (
                            loaded_inventory.copy()
                        )

                        success, _ = (
                            temp_manager.add_furniture(item)
                        )

                        if success:
                            loaded_inventory.append(item)

                        else:
                            skipped_rows += 1

                    except (
                        ValueError,
                        TypeError,
                        KeyError
                    ):
                        # Skip damaged furniture records instead of
                        # crashing the whole retailer inventory system.
                        skipped_rows += 1

            self.inventory = loaded_inventory

            return (
                True,
                f"Inventory loaded successfully. "
                f"{len(loaded_inventory)} item(s) loaded; "
                f"{skipped_rows} invalid row(s) skipped."
            )

        except OSError as error:
            return False, f"Unable to load inventory: {error}"
        
        # ---------------------------------------------------------
# TC23 - STOCK ALLOCATION CREATES AUDIT LOG
# ---------------------------------------------------------

def test_tc23_allocation_creates_audit_log(tmp_path):
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

    success, _ = store.allocate_stock("F001", 3)

    assert success is True
    assert log_file.exists()

    log_content = log_file.read_text(encoding="utf-8")

    assert "ALLOCATION" in log_content
    assert "F001" in log_content
    assert "Corner Sofa" in log_content
    assert "Allocated: 3" in log_content
    assert "Remaining stock: 5" in log_content


# ---------------------------------------------------------
# TC24 - STOCK UPDATE CREATES AUDIT LOG
# ---------------------------------------------------------

def test_tc24_stock_update_creates_audit_log(tmp_path):
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

    success, _ = store.update_stock("F003", 5)

    assert success is True
    assert log_file.exists()

    log_content = log_file.read_text(encoding="utf-8")

    assert "STOCK UPDATE" in log_content
    assert "F003" in log_content
    assert "Three-Door Wardrobe" in log_content
    assert "Added: 5" in log_content
    assert "New stock: 7" in log_content