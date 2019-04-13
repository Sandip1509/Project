from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render_to_response
from django.shortcuts import render,redirect
from .models import EBook, Chapter
from .forms import MyForm, MyChapterForm
from django.http import HttpResponse
from .script import pdf_splitter
from django.contrib import messages


class HomeView(generic.ListView):
    template_name = "publisher/home.html"
    context_object_name = "object_list"
    def get_queryset(self):
        return EBook.objects.all()

class ChapterDetailView(generic.ListView):
    template_name = "publisher/chapterDetail.html"
    context_object_name = "ebook"
    def get_queryset(self):
        return EBook.objects.get(id=self.kwargs.get('pk'))


class EBookCreate(CreateView):
    form_class = MyForm
    template_name = "publisher/ebook_form.html"


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
            book_name=str(EBook.objects.get(id=c_id))
            chapter = chapter_form.save(commit=False)
            chapter.ebook = EBook.objects.get(id=c_id)
            chapter.save()
            messages.success(request, f' Chapter created for!',book_name)
            url_name=EBook.objects.get(id=c_id).bookurl

            print(url_name+'\\'+book_name)
            ebook=url_name+'\\'+book_name
            print('Type:', type(ebook))
            print(ebook)
            pdf_splitter(ebook,start_page,end_page,chapter_name,book_name)
    else:
        chapter_form = MyChapterForm()
    return render(request, 'publisher/createchapters.html', {'form':chapter_form})


class EBookUpdate(UpdateView):
    model = EBook
    fields = '__all__'


class EBookDelete(DeleteView):
    model = EBook
    success_url = reverse_lazy('publisher:home')



class ChapterDelete(DeleteView):
    model = Chapter
    success_url = reverse_lazy('publisher:home')
