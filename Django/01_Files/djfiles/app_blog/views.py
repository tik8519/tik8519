from _csv import reader

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.views import generic, View
from .models import *
from .forms import RegisterForm, BlogForm, UploadBlog, ImageForms


class BlogListView(generic.ListView):
    """Выводит список блогов"""
    model = Blog
    template_name = 'blog_list.html'  # Явно указывает на путь к шаблону
    context_object_name = 'blog_list'  # Явно указывает на имя объекта передаваемого в шаблон

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['descript'] = context['blog_list']
        return context  # разобраться для ограничения кол-ва символов

    def get_ordering(self, **kwargs):
        ordering = self.request.GET.get('author')
        return ordering
        # return super(BlogListView, self).get_queryset(**kwargs).order_by('-created_at')


class BlogDetailView(generic.DetailView):
    """Выводит детальную информацию о блоге"""
    model = Blog
    template_name = 'blog_detail.html'
    context_object_name = 'blog'

    def get_context_data(self, *args, **kwargs):
        """Позволяет загружать изображения"""
        request = super().get_context_data(*args, **kwargs)
        blog_id = self.kwargs['pk']
        form = ImageForms(initial={'blog': blog_id})
        request['form'] = form
        images = File.objects.filter(blog=blog_id)
        request['images'] = images
        return request

    def post(self, request, **kwargs):
        form = ImageForms(request.POST, request.FILES)
        blog_id = self.kwargs['pk']

        if form.is_valid():
            # здесь можно прописать бизнес логику
            files = self.request.FILES.getlist('file')
            for f in files:
                instace = File(file=f, blog_id=blog_id)
                instace.save()
            return HttpResponseRedirect('/' + str(blog_id))  # указывается адрес перенаправления после проверки
        return render(request, 'blog_detail.html', {'form': form})


class BlogFormView(View):
    """Позволяет добавлять новую новость в БД из отдельной страницы"""

    def get(self, request):
        blog_form = BlogForm(initial={'author': self.request.user},)
        # Передает значение 'author' в форму. В форме это поле скрыто.
        return render(request, 'blog_form.html', context={'blog_form': blog_form})

    def post(self, request):
        # if not request.user.has_perm('app_news.change_news'):
        #     raise PermissionDenied()

        blog_form = BlogForm(request.POST)

        if blog_form.is_valid():
            # здесь можно прописать бизнес логику
            Blog.objects.create(**blog_form.cleaned_data)
            return HttpResponseRedirect('/')
        return render(request, 'blog_form.html', context={'blog_form': blog_form})


class Login(LoginView):
    template_name = 'users/login.html'


class UserEditFormView(View):
    """Позволяет редактировать информацию о пользователе в отдельной странице"""

    def get(self, request):
        # if not request.user.has_perm('app_blog.change_user'):
        #     raise PermissionDenied()
        # вызывает ошибку если недостаточно прав на действие
        if str(self.request.user) != 'AnonymousUser':
            user = User.objects.get(id=request.user.id)
            user_form = RegisterForm(instance=user)
            return render(request, 'users/edit.html', context={'user_form': user_form})
        else:
            return HttpResponseRedirect('/register/')

    def post(self, request):
        user = User.objects.get(id=request.user.id)
        user_form = RegisterForm(request.POST, instance=user)

        if user_form.is_valid():
            # здесь можно прописать бизнес логику
            user.save()
        return render(request, 'users/edit.html', context={'user_form': user_form})


def register_view(request):
    """Функция регистрации"""
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})


def logout_view(request):
    logout(request)
    response = redirect('/')  # перенаправляет на главную страницу
    return response


def upload_blog(request):
    """Загружает записи блога из файла"""
    if request.method == 'POST':
        upload_file_form = UploadBlog(request.POST, request.FILES)
        if upload_file_form.is_valid():
            blog_file = upload_file_form.cleaned_data['file'].read()
            blog_str = blog_file.decode('utf-8').split('\n')
            csv_reader = reader(blog_str, delimiter=";", quotechar='"')
            for row in csv_reader:
                if len(row) > 0:
                    record = Blog(author=request.user, title=row[0], description=row[1], created_at=row[2])
                    record.save()
            return HttpResponseRedirect('/')
    else:
        upload_file_form = UploadBlog()

    context = {
        'form': upload_file_form
    }
    return render(request, 'upload_blog.html', context=context)
