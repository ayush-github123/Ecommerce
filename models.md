### **App: `products`**

#### **Models for the `products` app**

```python
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Name of the category (e.g., Electronics, Clothing)
    slug = models.SlugField(max_length=100, unique=True)  # SEO-friendly URL
    description = models.TextField(blank=True, null=True)  # Optional detailed description of the category
    created = models.DateTimeField(auto_now_add=True)  # Timestamp when the category was created
    updated = models.DateTimeField(auto_now=True)  # Timestamp when the category was last updated

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)  # Name of the product
    slug = models.SlugField(max_length=200, unique=True)  # SEO-friendly URL for the product
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="products")  # Link to the category
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price of the product
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Optional discounted price
    stock = models.PositiveIntegerField(default=0)  # Available stock of the product
    description = models.TextField()  # Detailed description of the product
    image = models.ImageField(upload_to='products', blank=True, null=True)  # Main product image
    is_active = models.BooleanField(default=True)  # Whether the product is available for purchase
    created = models.DateTimeField(auto_now_add=True)  # Timestamp when the product was added
    updated = models.DateTimeField(auto_now=True)  # Timestamp when the product was last updated

    def __str__(self):
        return self.name
```

---

### **App: `reviews`**

#### **Models for the `reviews` app**

```python
class Review(models.Model):
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name="reviews")  # Link to the reviewed product
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)  # User who wrote the review
    rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # Rating from 1 to 5 stars
    comment = models.TextField(blank=True, null=True)  # Optional review comment
    created = models.DateTimeField(auto_now_add=True)  # Timestamp when the review was created

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
```

---

### **App: `users`**

#### **Models for the `users` app**

```python
class Profile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)  # Extend the built-in user model
    avatar = models.ImageField(upload_to='avatars', blank=True, null=True)  # Profile picture
    bio = models.TextField(blank=True, null=True)  # Short user bio
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # Optional phone number
    address = models.TextField(blank=True, null=True)  # Optional user address

    def __str__(self):
        return self.user.username
```

---

### **App: `cart`**

#### **Models for the `cart` app**

```python
class Cart(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name="cart")  # Link to the user
    created = models.DateTimeField(auto_now_add=True)  # Timestamp when the cart was created
    updated = models.DateTimeField(auto_now=True)  # Timestamp when the cart was last updated

    def __str__(self):
        return f"Cart for {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")  # Link to the cart
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)  # Link to the product
    quantity = models.PositiveIntegerField(default=1)  # Quantity of the product in the cart

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
```

---

### **App: `orders`**

#### **Models for the `orders` app**

```python
class Order(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)  # Link to the user who placed the order
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')])  # Order status
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # Total price of the order
    created = models.DateTimeField(auto_now_add=True)  # Timestamp when the order was created
    updated = models.DateTimeField(auto_now=True)  # Timestamp when the order was last updated

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")  # Link to the order
    product = models.ForeignKey('products.Product', on_delete=models.SET_NULL, null=True)  # Link to the purchased product
    quantity = models.PositiveIntegerField()  # Quantity of the product in the order
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price of the product at the time of purchase

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.id}"
```

---

### **App: `wishlist`**

#### **Models for the `wishlist` app**

```python
class Wishlist(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name="wishlist")  # Link to the user
    product = models.ManyToManyField('products.Product', related_name="wishlisted_by")  # Many-to-many relationship with products

    def __str__(self):
        return f"Wishlist for {self.user.username}"
```

---

### **App: `payments`** *(Optional for advanced functionality)*

#### **Models for the `payments` app**

```python
class Payment(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)  # Link to the user who made the payment
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE)  # Link to the order
    payment_method = models.CharField(max_length=50, choices=[('Credit Card', 'Credit Card'), ('PayPal', 'PayPal'), ('UPI', 'UPI')])  # Payment method
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Payment amount
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Success', 'Success'), ('Failed', 'Failed')])  # Payment status
    timestamp = models.DateTimeField(auto_now_add=True)  # Timestamp when the payment was made

    def __str__(self):
        return f"Payment {self.id} by {self.user.username} - {self.status}"
```

---

### **Summary**

- **`products` app**: `Category`, `Product`
- **`reviews` app**: `Review`
- **`users` app**: `Profile`
- **`cart` app**: `Cart`, `CartItem`
- **`orders` app**: `Order`, `OrderItem`
- **`wishlist` app**: `Wishlist`
- **`payments` app**: `Payment` (optional)

This modular approach ensures scalability and organizes the project cleanly. Let me know if you'd like further assistance!