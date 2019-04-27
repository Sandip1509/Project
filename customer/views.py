from django.http import HttpResponse
from django.views import generic
from .models import CustomerProfile
from products.models  import EBook,Chapter
from django.shortcuts import render, get_object_or_404
from shopping_cart.models import Order
from publisher.script import pdf_cat, make_Introduction
from django.shortcuts import render, redirect
from django.urls import reverse
import requests
from shopping_cart.models import OrderItem
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.conf import settings
from django.db import transaction
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
import json

@login_required()
def home(request):
    my_user_profile = CustomerProfile.objects.filter(user=request.user).first()
    my_orders = Order.objects.filter(is_ordered=False, owner=my_user_profile)
    print(my_orders)
    if(my_orders):
        order=my_orders.get(owner=my_user_profile).items.all()
        print(order)
        sum=0
        for items in order:
            sum+=items.product.price
        context = {
            'my_orders': my_orders,
            'sum': sum,
        }
        return render(request, "customer/home.html", context)
    else:
        return render(request, "customer/home.html")

@login_required()
def Buy(request):
    ref_no=request.GET.get('ref_no')
    print(ref_no)
    return render(request, "customer/payment.html",{'ref_no':ref_no})

@login_required()
def PayConfirm(request):
    return render(request, "customer/Payment_confirm.html")


def insertOrUpdate(model):
    try:
        with transaction.atomic():
            model.save()
    except IntegrityError as e:
        return HttpResponse('')


@login_required()
def orderHistory(request):
    my_user_profile = CustomerProfile.objects.filter(user=request.user).first()
    my_orders = Order.objects.filter(is_ordered=True, owner=my_user_profile)
    print(my_orders)
    return render(request, "customer/Order_history.html",{'my_orders':my_orders})

@login_required()
def Pay(request):
    name_book=request.POST.get('book_name')
    print('book_name: ',name_book)
    product_ids=json.loads(request.POST.get('id'))
    print('productIds: ',product_ids)
    my_user_profile = CustomerProfile.objects.filter(user=request.user).first()
    my_orders = Order.objects.filter(is_ordered=False, owner=my_user_profile)
    ref_no=0
    for order in my_orders:
        print("My order: ", order)
        ref_no=order.ref_code
        order.is_ordered=True
        order.save()
        insertOrUpdate(order)
    my_orders = Order.objects.filter(is_ordered=False, owner=my_user_profile)
    print("2nd My order: ", my_orders)
    # eBooks = EBook.objects.all()
    # chapters = Chapter.objects.all()
    ebooks_url=[]
    introduction_set=[]
    introduction=['Book_Name', 'Chapter_Name', 'Page_No']
    introduction_set.append(introduction)
    count = 2
    intro_url=settings.MEDIA_ROOT + '\\' +'simple_table.pdf'
    ebooks_url.append(intro_url)
    for id in product_ids:
        print(id)
        introduction = []
        ebook=Chapter.objects.get(id=id).ebook
        chapter = Chapter.objects.get(id=id)
        url=ebook.bookurl
        start_page=chapter.start_page
        end_page = chapter.end_page
        book_name=ebook.bookpdf.name.replace('.pdf','_')
        chapter_name=chapter.name
        chapter_url=url+'\\'+book_name+chapter_name+'.pdf'
        introduction.append(ebook.title)
        introduction.append(chapter_name)
        introduction.append(str(count))
        introduction_set.append(introduction)
        count+=(end_page-start_page+1)
        ebooks_url.append(chapter_url)
    print(introduction_set)
    print(ebooks_url)
    make_Introduction(name_book,introduction_set)
    pdf_cat(ref_no,ebooks_url)
    return HttpResponse(ref_no)



class OrderItemDelete(DeleteView):
    model = OrderItem
    success_url = reverse_lazy('customer:home')


class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('customer:home')



def search(request):
    if request.method == 'POST':
        book_name =  request.POST.get('search')
        print(book_name)
        status = EBook.objects.none()
        try:
            title = EBook.objects.filter(title__icontains=book_name)
            if (not (status)):
                genre = EBook.objects.filter(genre__icontains=book_name)
                print(genre)
            else:
                genre = EBook.objects.filter(genre__icontains=book_name)

            if(not (status)):
                keyword = EBook.objects.filter(keyword__icontains=book_name)
                print(keyword)
            else:
                keyword = EBook.objects.filter(keyword__icontains=book_name)
            status= title|genre|keyword
            print(status)
            # if(not(status)):
            #     status = EBook.objects.filter(genre__icontains=book_name)
            # if (not(status)):
            #     status = EBook.objects.filter(keyword__icontains=book_name)
            #Add_prod class contains a column called 'bookname'
        except EBook.DoesNotExist:
            status = None
        return render(request,"customer/search.html",{"ebook_list":status})
    else:
        return render(request,"customer/search.html")