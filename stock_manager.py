# Stock management logic for the Home Furniture Retail Store


class StockManager:
    """Manages furniture inventory for the home furniture retail store."""

    LOW_STOCK_THRESHOLD = 3

    def __init__(self):
        self.inventory = []

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

        return (
            True,
            f"Allocation successful: {item.name}. "
            f"Remaining stock: {item.quantity}"
        )

    def update_stock(self, furniture_id, additional_quantity):
        """Add newly received furniture stock."""

        item = self.find_by_id(furniture_id)

        if item is None:
            return False, "Furniture not found."

        if additional_quantity <= 0:
            return False, "Added quantity must be greater than 0."

        item.quantity += additional_quantity

        return (
            True,
            f"Stock updated: {item.name}. "
            f"New quantity: {item.quantity}"
        )

    def find_by_id(self, furniture_id):
        """Return one furniture item using its exact ID."""

        furniture_id = furniture_id.strip().lower()

        for item in self.inventory:
            if item.furniture_id.lower() == furniture_id:
                return item

        return None

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