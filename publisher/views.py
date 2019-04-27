from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render_to_response
from django.shortcuts import render,redirect
from products.models import EBook, Chapter
from products.forms import MyForm, MyChapterForm
from django.http import HttpResponse
from .script import pdf_splitter
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404

from shopping_cart.models import Order
from .models import PublisherProfile
from django.contrib.auth.models import User
import csv
import io
# class HomeView(generic.ListView):
#     template_name = "publisher/home.html"
#     context_object_name = "object_list"
#     def get_queryset(self):
#         return EBook.objects.all()



class ChapterDetailView(generic.ListView):
    template_name = "publisher/chapterDetail.html"
    context_object_name = "ebook"
    def get_queryset(self):
        my_user_profile = PublisherProfile.objects.filter(user=self.request.user).first()
        user = User.objects.filter(username=my_user_profile).first()
        ebooks = EBook.objects.filter(publisher=user)
        return ebooks.get(id=self.kwargs.get('pk'))


class EBookCreate(CreateView):
    form_class = MyForm
    def form_valid(self, form):
        form.instance.publisher = self.request.user
        return super(EBookCreate, self).form_valid(form)
    template_name = "publisher/ebook_form.html"
    success_url = reverse_lazy('publisher:home')

@login_required()
def createChapters(request, pk):
    print(request.POST)
    chapter_form = MyChapterForm()
    if request.method == 'POST':
        print("success")
        chapter_form = MyChapterForm(data=request.POST)
        if chapter_form.is_valid:
            print("hello")
            start_page = request.POST.get('start_page')
            end_page = request.POST.get('end_page')
            chapter_name=request.POST.get('name')
            c_id=pk
            print(c_id,type(c_id))
            book_name=str(EBook.objects.get(id=c_id).bookpdf.name)
            chapter = chapter_form.save(commit=False)
            chapter.ebook = EBook.objects.get(id=c_id)
            chapter.save()
            url_name=EBook.objects.get(id=c_id).bookurl
            print(url_name+'\\'+book_name)
            ebook=url_name+'\\'+book_name
            print('Type:', type(ebook))
            print(ebook)
            pdf_splitter(ebook,start_page,end_page,chapter_name,book_name)

    else:
        chapter_form = MyChapterForm()
    return render(request, 'publisher/createchapters.html', {'form':chapter_form,'pk':pk})

login_required
def createChaptersUsingCSV(request, pk):
    print(pk)
    file_name=request.FILES['fileToUpload']
    print(type(file_name))
    ebook=EBook.objects.get(id=pk)
    my_user_profile = PublisherProfile.objects.filter(user=request.user).first()
    user = User.objects.filter(username=my_user_profile).first()
    ebook = EBook.objects.filter(publisher=user).get(id=pk)
    context = {
        'ebook': ebook
    }
    file_name.seek(0)
    reader = csv.DictReader(io.StringIO(file_name.read().decode('utf-8')))
    for row in reader:
        book_name = str(EBook.objects.get(id=pk).bookpdf.name)
        url_name = EBook.objects.get(id=pk).bookurl
        ebook_url = url_name + '\\' + book_name
        start_page=row['start_page']
        end_page = row['end_page']
        chapter_name=row['name']
        pdf_splitter(ebook_url, start_page, end_page, chapter_name, book_name)
        p = Chapter(ebook=ebook,name=row['name'], description=row['description'],start_page=row['start_page'],end_page=row['end_page'],price=row['price'])
        p.save()
    return render(request,"publisher/chapterDetail.html",context)


@login_required()
def home(request):
    my_user_profile = PublisherProfile.objects.filter(user=request.user).first()
    user=User.objects.filter(username = my_user_profile).first()
    ebooks = EBook.objects.filter(publisher=user)
    context = {
		'ebooks': ebooks
	}
    return render(request, "publisher/home.html", context)


class EBookUpdate(UpdateView):
    model = EBook
    fields = '__all__'


class EBookDelete(DeleteView):
    model = EBook
    success_url = reverse_lazy('publisher:home')



class ChapterDelete(DeleteView):
    model = Chapter
    def get_success_url(self):
        pk=self.kwargs['pk']
        ebook=Chapter.objects.get(id=pk).ebook.title
        ebook_pk = EBook.objects.filter(title=ebook)[0].id
        return reverse_lazy('publisher:chapter-details', kwargs={'pk': ebook_pk})


@login_required()
def search(request):
    if request.method == 'POST':
        book_name =  request.POST.get('search')
        print(book_name)
        try:
            status = EBook.objects.filter(title__icontains=book_name)
            #Add_prod class contains a column called 'bookname'
        except EBook.DoesNotExist:
            status = None
        return render(request,"publisher/search.html",{"ebook_list":status})
    else:
        return render(request,"publisher/search.html")
