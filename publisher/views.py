""" from django.shortcuts import render, get_object_or_404
    from .models import Album,Song

    def index(request):
        all_albums = Album.objects.all()
        context ={'all_albums' : all_albums}
        return render(request, 'music/index.html' ,context)

    def detail(request, album_id):
        album = get_object_or_404(Album, pk=album_id)
        return render(request, 'music/detail.html', {'album' : album})

    def favourite(request, album_id):
        album = get_object_or_404(Album, pk=album_id)
        try:
            selected_song = album.song_set.get(pk=request.POST['song'])
        except (KeyError, Song.DoesNotExist):
            return render(request, 'music/detail.html', {
                'album' : album,
                'error_message' : "You did not select a valid song",
        })
        else:
            selected_song.is_favourite=True
            selected_song.save()
            return render(request, 'music/detail.html', {'album': album})
"""

from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from .models import EBook, Chapter
from .forms import MyForm

class HomeView(generic.ListView):
    template_name = "publisher/home.html"
    context_object_name = "object_list"
    def get_queryset(self):
        return EBook.objects.all()

class DetailView(generic.DetailView):
    model = EBook
    template_name = "publisher/detail.html"


class EBookCreate(CreateView):
    form_class = MyForm
    template_name = "publisher/ebook_form.html"


class EBookUpdate(UpdateView):
    model = EBook
    fields = '__all__'


class EBookDelete(DeleteView):
    model = EBook
    success_url = reverse_lazy('publisher:home')

"""
class UserFormView(View):
    form_class = UserForm
    template_name = "music/registration_form.html"

    #display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})


    #process from data
    def post(self,request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            # cleaned (nnormalized) data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()


            #returns User Objects if credentials are correct
            user = authenticate(username= username, password=password)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect('music:index')

     return render(request, self.template_name, {'form': form})
"""