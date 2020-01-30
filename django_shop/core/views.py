from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.utils import timezone
from .models import Item, OrderItem, Order 

class HomeView(ListView):
	model = Item
	template_name = "home.html"
	context_object_name = 'items'


def checkout(request):
	return render(request, "checkout.html")

class ItemDetailView(DetailView):
	model = Item
	template_name = "product.html"

def add_to_cart(request, slug): #Добавление товаров в корзину	
	item = get_object_or_404(Item, slug=slug) #ПРоверям есть ли страница с товаром на сайте, если нет, то получаем страницу 404, если да. то добавляем ее
	order_item, created = OrderItem.objects.get_or_create(  #Добавляем в модель OrderItem объект Item, create нужен что бы принять булевый объект фунции get_or_create
		item=item,
		user=request.user,
		ordered=False
	)
	order_qs = Order.objects.filter(user=request.user, ordered=False) #Фильтруем Order по юзеру и ordered 
	if order_qs.exists(): # exists() возвращает тру если в наборе есть записи
		order = order_qs[0] # Проверяем находиться ли позиция заказа в заказе (OrderItem в Item)
		if order.items.filter(item__slug=item.slug).exists(): # отбираем из набора записей, только те, которые соотвествует slug`у item, если они есть, то выдаем тру
			order_item.quantity += 1 #Добавляем в корзину плюс один товар
			order_item.save()
			messages.info(request, "Количество товаров в корзине изменено")
		else:
			messages.info(request, "Данная позиция добавлена в корзину")
			order.items.add(order_item)
			return redirect("core:product", slug=slug)
	else:
		ordered_date = timezone.now()
		order = Order.objects.create(
			user=request.user, ordered_date=ordered_date)
		order.items.add(order_item) # add связывыет текущую запись первичной модели с записью вторичной модели. переданную в параметре
		messages.info(request, "Данная позиция добавлена в корзину")
	return redirect("core:product", slug=slug)

def remove_from_cart(request, slug): # Удаляет из корзины
	item = get_object_or_404(Item, slug=slug)
	order_item = OrderItem.objects.filter(
		item=item,
		user=request.user,
		ordered=False
	).first()
	order = Order.objects.filter( #Фильтруем Order по юзеру и ordered ы
		user=request.user, 
		ordered=False
	).first()
	if order: # exists() возвращает тру если в наборе есть записи
		if order.items.filter(item__slug=item.slug).exists(): # отбираем из набора записей, только те, которые соотвествует slug`у item, если они есть, то выдаем тру
			if order_item.quantity > 1:
				order_item.quantity -= 1
				order_item.save()
			else:
				OrderItem.objects.filter(item=item, user=request.user, ordered=False).delete() # удаляет указанные записи мз списка с текущей записью
			messages.info(request, "Данная позиция удалена из корзины")
			return redirect("core:product", slug=slug)
		else:
			messages.info(request, "Этого товара нет в вашей корзине")
			return redirect("core:product", slug=slug)
	else:
		messages.info(request, "У вас нет актвного заказа")
		return redirect("core:product", slug=slug)
	