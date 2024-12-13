from django.db import models
from django.contrib.auth.models import User
from products.models import Product

# Cart model for storing a user's cart
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart")  # Link to the user
    updated = models.DateTimeField(auto_now=True)  # Timestamp when the cart was last updated
    created = models.DateTimeField(auto_now_add=True)  # Timestamp when the cart was created

    def __str__(self):
        return f"Cart for {self.user.username}"


# CartItem model for individual items in the cart
class CartItem(models.Model): 
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")  # Link to the cart
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cart_items")  # Link to the product
    quantity = models.PositiveIntegerField(default=1)  # Quantity of the product
    updated = models.DateTimeField(auto_now=True)  # Timestamp when the item was last updated
    created = models.DateTimeField(auto_now_add=True)  # Timestamp when the item was added to the cart

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.cart.user.username}'s cart"

    class Meta:
        ordering = ['-updated', '-created']