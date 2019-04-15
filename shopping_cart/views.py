from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from customer.models import CustomerProfile
from products.models import Chapter

from shopping_cart.extras import generate_order_id
from shopping_cart.models import OrderItem, Order, Transaction

import datetime

def get_user_pending_order(request):
    # get order for the correct user
    user_profile = get_object_or_404(CustomerProfile, user=request.user)
    order = Order.objects.filter(owner=user_profile, is_ordered=False)
    if order.exists():
        # get the only order in the list of filtered orders
        return order[0]
    return 0


@login_required()
def add_to_cart(request, **kwargs):
    # get the user profile
    user_profile = get_object_or_404(CustomerProfile, user=request.user)
    # filter products by id
    product = Chapter.objects.filter(id=kwargs.get('item_id')).first()
    print(product)
    # check if the user already owns this product
    if product in request.user.customerprofile.chapters.all():
        messages.info(request, 'You already own this chapter')
        return redirect(reverse('products:product-list'))
        # create orderItem of the selected product
    order_item, status = OrderItem.objects.get_or_create(product=product)
    print(order_item,status)
    # create order associated with the user
    user_order, status = Order.objects.get_or_create(owner=user_profile, is_ordered=False)
    user_order.items.add(order_item)
    print(user_order, status)
    # if status:
        # generate a reference code
    user_order.ref_code = generate_order_id()
    print(user_order.ref_code)
    user_order.save()
    # show confirmation message and redirect back to the same page
    # messages.info(request, "item added to cart")
    return HttpResponse('')


@login_required()
def delete_from_cart(request, item_id):
    item_to_delete = OrderItem.objects.filter(pk=item_id)
    if item_to_delete.exists():
        item_to_delete[0].delete()
        messages.info(request, "Item has been deleted")
    return redirect(reverse('shopping_cart:order_summary'))


@login_required()
def order_details(request, **kwargs):
    existing_order = get_user_pending_order(request)
    context = {
        'order': existing_order
    }
    return render(request, 'shopping_cart/order_summary.html', context)


@login_required()
def update_transaction_records(request, token):
    # get the order being processed
    order_to_purchase = get_user_pending_order(request)

    # update the placed order
    order_to_purchase.is_ordered = True
    order_to_purchase.date_ordered = datetime.datetime.now()
    order_to_purchase.save()

    # get all items in the order - generates a queryset
    order_items = order_to_purchase.items.all()

    # update order items
    order_items.update(is_ordered=True, date_ordered=datetime.datetime.now())

    # Add products to user profile
    user_profile = get_object_or_404(CustomerProfile, user=request.user)
    # get the products from the items
    order_products = [item.product for item in order_items]
    user_profile.chapters.add(*order_products)
    user_profile.save()

    # create a transaction
    transaction = Transaction(profile=request.user.customerprofile,
                              token=token,
                              order_id=order_to_purchase.id,
                              amount=order_to_purchase.get_cart_total(),
                              success=True)
    # save the transcation (otherwise doesn't exist)
    transaction.save()

    # send an email to the customer
    # look at tutorial on how to send emails with sendgrid
    messages.info(request, "Thank you! Your purchase was successful!")
    return redirect(reverse('accounts:my_profile'))


def success(request, **kwargs):
    # a view signifying the transcation was successful
    return render(request, 'shopping_cart/purchase_success.html', {})
