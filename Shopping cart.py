class Product:
    def __init__(self, product_id, name, price, quantity_available):
        self._product_id = product_id
        self._name = name
        self._price = price
        self._quantity_available = quantity_available

    def get_product_id(self):
        return self._product_id

    def get_name(self):
        return self._name

    def get_price(self):
        return self._price

    def get_quantity_available(self):
        return self._quantity_available

    def set_quantity_available(self, value):
        if value >= 0:
            self._quantity_available = value

    def decrease_quantity(self, amount):
        if amount <= self._quantity_available:
            self._quantity_available -= amount
            return True
        return False

    def increase_quantity(self, amount):
        if amount > 0:
            self._quantity_available += amount

    def display_details(self):
        return f"ID: {self._product_id}, Name: {self._name}, Price: {self._price}, Available: {self._quantity_available}"

    def to_dict(self):
        return {
            "type": "product",
            "product_id": self._product_id,
            "name": self._name,
            "price": self._price,
            "quantity_available": self._quantity_available
        }


class PhysicalProduct(Product):
    def __init__(self, product_id, name, price, quantity_available, weight):
        super().__init__(product_id, name, price, quantity_available)
        self._weight = weight

    def get_weight(self):
        return self._weight

    def display_details(self):
        return f"ID: {self._product_id}, Name: {self._name}, Price: {self._price}, Available: {self._quantity_available}, Weight: {self._weight}kg"

    def to_dict(self):
        return {
            "type": "physical",
            "product_id": self._product_id,
            "name": self._name,
            "price": self._price,
            "quantity_available": self._quantity_available,
            "weight": self._weight
        }


class DigitalProduct(Product):
    def __init__(self, product_id, name, price, quantity_available, download_link):
        super().__init__(product_id, name, price, quantity_available)
        self._download_link = download_link

    def get_download_link(self):
        return self._download_link

    def display_details(self):
        return f"ID: {self._product_id}, Name: {self._name}, Price: {self._price}, Download Link: {self._download_link}"

    def to_dict(self):
        return {
            "type": "digital",
            "product_id": self._product_id,
            "name": self._name,
            "price": self._price,
            "quantity_available": self._quantity_available,
            "download_link": self._download_link
        }


class CartItem:
    def __init__(self, product, quantity):
        self._product = product
        self._quantity = quantity

    def get_product(self):
        return self._product

    def get_quantity(self):
        return self._quantity

    def set_quantity(self, value):
        if value >= 0:
            self._quantity = value

    def calculate_subtotal(self):
        return self._product.get_price() * self._quantity

    def __str__(self):
        return f"Item: {self._product.get_name()}, Quantity: {self._quantity}, Price: {self._product.get_price()}, Subtotal: {self.calculate_subtotal()}"

    def to_dict(self):
        return {
            "product_id": self._product.get_product_id(),
            "quantity": self._quantity
        }


class ShoppingCart:
    def __init__(self):
        self._items = {}
        self._catalog = {}

    def add_product_to_catalog(self, product):
        self._catalog[product.get_product_id()] = product

    def add_item(self, product_id, quantity):
        if product_id in self._catalog:
            product = self._catalog[product_id]
            if product.decrease_quantity(quantity):
                if product_id in self._items:
                    self._items[product_id].set_quantity(self._items[product_id].get_quantity() + quantity)
                else:
                    self._items[product_id] = CartItem(product, quantity)
                return True
        return False

    def remove_item(self, product_id):
        if product_id in self._items:
            item = self._items.pop(product_id)
            item.get_product().increase_quantity(item.get_quantity())
            return True
        return False

    def update_quantity(self, product_id, new_quantity):
        if product_id in self._items:
            item = self._items[product_id]
            diff = new_quantity - item.get_quantity()
            if diff > 0:
                if item.get_product().decrease_quantity(diff):
                    item.set_quantity(new_quantity)
                    return True
            elif diff < 0:
                item.get_product().increase_quantity(-diff)
                item.set_quantity(new_quantity)
                return True
        return False

    def get_total(self):
        return sum(item.calculate_subtotal() for item in self._items.values())

    def display_cart(self):
        print("\nCart Items:")
        for item in self._items.values():
            print(item)
        print("Total:", self.get_total())

    def display_products(self):
        print("\nAvailable Products:")
        for product in self._catalog.values():
            print(product.display_details())


def main():
    cart = ShoppingCart()

    cart.add_product_to_catalog(PhysicalProduct("v_27", "COREMAN(Dsa Book)", 5000, 10, 1))
    cart.add_product_to_catalog(DigitalProduct("Y_27", "E-Book of COREMAN(Dsa Book)", 250, 20, "www.download.com/ebook"))

    while True:
        print("\n1. View Products")
        print("2. Add Item to Cart")
        print("3. View Cart")
        print("4. Update Quantity")
        print("5. Remove Item")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            cart.display_products()
        elif choice == '2':
            product_id = input("Enter Product ID: ")
            qty = int(input("Enter Quantity: "))
            if cart.add_item(product_id, qty):
                print("Added to cart.")
            else:
                print("Failed to add. Check stock or ID.")
        elif choice == '3':
            cart.display_cart()
        elif choice == '4':
            product_id = input("Enter Product ID: ")
            qty = int(input("Enter New Quantity: "))
            if cart.update_quantity(product_id, qty):
                print("Quantity updated.")
            else:
                print("Update failed.")
        elif choice == '5':
            product_id = input("Enter Product ID to remove: ")
            if cart.remove_item(product_id):
                print("Item removed.")
            else:
                print("Item not found in cart.")
        elif choice == '6':
            print("Thanks for shopping! \nHave a good day.\nPlease come again.")
            break
        else:
            print("Oops! Invalid choice. Please try again......")


if __name__ == "__main__":
    main()
