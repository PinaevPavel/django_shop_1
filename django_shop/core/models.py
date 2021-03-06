from django.conf import settings
from django.db import models
from django.shortcuts import reverse

CATEGORY_CHOICES = (
	('К', 'Комплект ключей'),
	('Ш', 'Поштучно'),
)


class Item(models.Model):
	title = models.CharField(max_length=100)
	price = models.FloatField()
	discount_price = models.FloatField(blank=True, null=True) #Если blanc true, то поле может быть пустым
	category = models.CharField(choices=CATEGORY_CHOICES, max_length=30)
	slug = models.SlugField()
	description = models.TextField()
	quantity = models.IntegerField(default=1)

	def __str__(self):
		return self.title

	def get_absolute_url(self): # метод, определяющий каким образом будет формироваться URL адрес, при переходе на страницу товара 
		return reverse("core:product", kwargs={
				'slug': self.slug
			})

	def get_add_to_cart_url(self): # метод формирующий URL адрес при добавлении товара в корзину
		return reverse("core:add-to-cart", kwargs={
				'slug': self.slug
			})

	def get_remove_from_cart_url(self): # метод формирующий URL адрес при добавлении товара в корзину
		return reverse("core:remove-from-cart", kwargs={
			'slug': self.slug
		})



class OrderItem(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	ordered = models.BooleanField(default=False)
	item = models.ForeignKey(Item, on_delete=models.CASCADE)
	quantity = models.IntegerField(default=1)

	def __str__(self):
		return f"{self.quantity} of {self.item.title}"

class Order(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	items = models.ManyToManyField(OrderItem)
	start_date = models.DateTimeField(auto_now_add=True)
	ordered_date = models.DateTimeField()
	ordered = models.BooleanField(default=False)

	def __str__(self):
		return self.user.username
