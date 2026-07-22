# Furniture classes for the Home Furniture Retail Store Stock Management System


class FurnitureItem:
    """Represents a general furniture product in the home furniture retail store."""

    def __init__(self, furniture_id, name, category, price, quantity):
        self.furniture_id = furniture_id
        self.name = name
        self.category = category
        self.price = price
        self.quantity = quantity

    def display_details(self):
        """Return common furniture details."""
        return (
            f"{self.furniture_id} | "
            f"{self.name} | "
            f"{self.category} | "
            f"GBP {self.price:.2f} | "
            f"Qty: {self.quantity}"
        )


class Sofa(FurnitureItem):
    """Represents sofa furniture with seating capacity."""

    def __init__(
        self,
        furniture_id,
        name,
        price,
        quantity,
        seating_capacity
    ):
        super().__init__(
            furniture_id,
            name,
            "Sofas",
            price,
            quantity
        )
        self.seating_capacity = seating_capacity

    def display_details(self):
        """Return sofa-specific details."""
        return (
            f"{super().display_details()} | "
            f"Seats: {self.seating_capacity}"
        )


class Table(FurnitureItem):
    """Represents table furniture with material information."""

    def __init__(
        self,
        furniture_id,
        name,
        price,
        quantity,
        material
    ):
        super().__init__(
            furniture_id,
            name,
            "Tables",
            price,
            quantity
        )
        self.material = material

    def display_details(self):
        """Return table-specific details."""
        return (
            f"{super().display_details()} | "
            f"Material: {self.material}"
        )


class Wardrobe(FurnitureItem):
    """Represents wardrobe furniture with number of doors."""

    def __init__(
        self,
        furniture_id,
        name,
        price,
        quantity,
        number_of_doors
    ):
        super().__init__(
            furniture_id,
            name,
            "Wardrobes",
            price,
            quantity
        )
        self.number_of_doors = number_of_doors

    def display_details(self):
        """Return wardrobe-specific details."""
        return (
            f"{super().display_details()} | "
            f"Doors: {self.number_of_doors}"
        )