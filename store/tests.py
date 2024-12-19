from django.test import TestCase
from django.contrib.auth.models import User
from .models import Category, Product, Cart, CartItem

class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Electronics', slug='electronics')

    def test_category_creation(self):
        self.assertEqual(self.category.name, 'Electronics')
        self.assertEqual(self.category.slug, 'electronics')

class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Books', slug='books')
        self.product = Product.objects.create(
            category=self.category,
            name='Django for Beginners',
            slug='django-for-beginners',
            description='A book on Django.',
            price=29.99,
            stock=50,
            available=True
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, 'Django for Beginners')
        self.assertEqual(self.product.category.name, 'Books')
        self.assertTrue(self.product.available)

class CartTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(name='Clothing', slug='clothing')
        self.product = Product.objects.create(
            category=self.category,
            name='T-Shirt',
            slug='t-shirt',
            description='A cool t-shirt.',
            price=19.99,
            stock=100,
            available=True
        )
        self.client.login(username='testuser', password='testpass')

    def test_add_to_cart(self):
        response = self.client.get(f'/cart/add/{self.product.id}/')
        self.assertRedirects(response, '/cart/')
        cart = Cart.objects.get(user=self.user)
        cart_item = CartItem.objects.get(cart=cart, product=self.product)
        self.assertEqual(cart_item.quantity, 1)

    def test_remove_from_cart(self):
        cart = Cart.objects.create(user=self.user)
        cart_item = CartItem.objects.create(cart=cart, product=self.product, quantity=2)
        response = self.client.get(f'/cart/remove/{cart_item.id}/')
        self.assertRedirects(response, '/cart/')
        self.assertFalse(CartItem.objects.filter(id=cart_item.id).exists())