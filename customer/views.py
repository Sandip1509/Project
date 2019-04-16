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

def home(request):
    my_user_profile = CustomerProfile.objects.filter(user=request.user).first()
    my_orders = Order.objects.filter(is_ordered=False, owner=my_user_profile)
    print(my_orders)
    if(my_orders):
        order=my_orders.get(owner=my_user_profile).items.all()
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

def Buy(request):
    my_user_profile = CustomerProfile.objects.filter(user=request.user).first()
    my_orders = Order.objects.filter(is_ordered=False, owner=my_user_profile)
    orders=my_orders.get(owner=my_user_profile).items.all()
    eBooks = EBook.objects.all()
    chapters = Chapter.objects.all()
    ebooks_url=[]
    introduction_set=[]
    introduction=['Book_Name', 'Chapter_Name', 'Page_No']
    introduction_set.append(introduction)
    count = 1
    intro_url=settings.MEDIA_ROOT + '\\' +'simple_table.pdf'
    ebooks_url.append(intro_url)
    for order in orders:
        introduction = []
        ebook = order.product.ebook
        url=EBook.objects.filter(title=ebook)[0].bookurl
        start_page=Chapter.objects.filter(ebook=ebook)[0].start_page
        end_page = Chapter.objects.filter(ebook=ebook)[0].end_page
        book_name=EBook.objects.filter(title=ebook)[0].bookpdf.name.replace('.pdf','_')
        chapter=order.product.name
        chapter_url=url+'\\'+book_name+chapter+'.pdf'
        introduction.append(ebook.title)
        introduction.append(chapter)
        introduction.append(str(count))
        introduction_set.append(introduction)
        count+=(end_page-start_page+1)
        ebooks_url.append(chapter_url)
    print(introduction_set)
    print(ebooks_url)
    make_Introduction(introduction_set)
    pdf_cat(ebooks_url)
    return HttpResponse('')



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
        try:
            status = EBook.objects.filter(title__icontains=book_name)
            #Add_prod class contains a column called 'bookname'
        except EBook.DoesNotExist:
            status = None
        return render(request,"customer/search.html",{"ebook_list":status})
    else:
        return render(request,"customer/search.html")