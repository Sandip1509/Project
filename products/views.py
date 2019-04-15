# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views import generic
from shopping_cart.models import Order
from .models import EBook,Chapter
from django.contrib.auth.decorators import login_required

@login_required()
def product_list(request):
    object_list = EBook.objects.all()
    context = {
        'ebook_list': object_list,
    }
    return render(request, "products/product_list.html", context)

@login_required()
def chapter_details(request, pk):
    ebook = EBook.objects.get(id=pk)
    chapters = Chapter.objects.filter(ebook=ebook)
    filtered_orders = Order.objects.filter(owner=request.user.customerprofile, is_ordered=False)
    current_order_products = []
    if filtered_orders.exists():
    	user_order = filtered_orders[0]
    	user_order_items = user_order.items.all()
    	current_order_products = [product.product for product in user_order_items]

    context = {
        'ebook': ebook,
        'object_list': chapters,
        'current_order_products': current_order_products,
    }

    return render(request, "products/product_details.html", context)


