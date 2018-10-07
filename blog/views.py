from django.shortcuts import render

from django.urls import reverse

from django.http import HttpResponse
from django.http import HttpResponseRedirect

from django.core.paginator import Paginator

from django.views import View
from .models import Post, App, PublicUsers, Comment

from django.db.models import Q

from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUser, LoginUser, UserComments

# Create your views here.

def home_page(request):
    all_posts = Post.objects.all()
    posts = all_posts[1:3]
    act_post = all_posts[0]

    # Getting Apps
    all_games = App.objects.filter(app_type='game')
    games = all_games[0:2]
    games_2 = all_games[2:4]

    all_apps = App.objects.filter(app_type='app')
    apps = all_apps[0:2]
    apps_2 = all_apps[2:4]

    context = {
        'posts': posts,
        'act_post': act_post,
        'games': games,
        'games_2': games_2,
        'apps': apps,
        'apps_2': apps_2
    }

    return render(request, 'blog/home_page.html', context)

def posts_list(request):
    posts = Post.objects.all()

    paginator = Paginator(posts, 4)

    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url = ''

    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''

    context = {
        'page_object': page,
        'prev_url': prev_url,
        'next_url': next_url
    }
    return render(request, 'blog/posts_list.html', context)

class PostDetail(View):
    def get(self, request, slug):
        post = Post.objects.get(slug__iexact=slug)
        comments = Comment.objects.filter(post_slug=post.slug)[:5]

        comm_form = UserComments()

        context = {
            'post': post,
            'comments': comments,
            'form': comm_form
        }
        return render(request, 'blog/post_detail.html', context)

    def post(self, request, slug):
        bound_form = UserComments(request.POST)
        author_name = request.session.get('name')
        author = PublicUsers.objects.get(username=author_name)

        if bound_form.is_valid():
            new_comm = bound_form.save(author, slug)
            return HttpResponseRedirect(reverse('post_detail_url', kwargs={'slug': slug}))
        return HttpResponseRedirect(reverse('post_detail_url', kwargs={'slug':slug}))

def search_que(request):
    blank = False
    search_query = request.GET.get('search')
    if search_query == '':
        blank = True
        context = {
            'blank': blank,
        }
        return render(request, 'blog/search_res.html', context)
    else:
        all_posts = Post.objects.filter(Q(title__icontains=search_query) | Q(body__icontains=search_query))
        context = {
            'blank': blank,
            'posts': all_posts
        }
        return render(request, 'blog/search_res.html', context)

def mods_view(request):
    mods = App.objects.filter(app_type='mod')
    context = {
        'mods': mods
    }

    return render(request, 'blog/mods_template.html', context)


class Registration(View):
    def get(self, request):
        form = CreateUser()
        context = {
            'form':form
        }
        return render(request, 'blog/reg.html', context)

    def post(self, request):
        bound_form = CreateUser(request.POST)

        if bound_form.is_valid():
            new_user = bound_form.save()
            request.session['name'] = request.POST['username']
            request.session['auth'] = 'true'
            return HttpResponseRedirect(reverse('home_page'))
        return render(request, 'blog/reg.html', context={'form': bound_form})

class Login(View):
    def get(self, request):
        form = LoginUser()
        context = {
            'form': form
        }
        return render(request, 'blog/login.html', context)

    def post(self, request):
        bound_form = LoginUser(request.POST)
        if PublicUsers.objects.filter(username=request.POST['username']).count() == 0:
            return HttpResponse("Пользователь с таким именем не существует")
        else:
            user = PublicUsers.objects.get(username=request.POST['username'])
            if request.POST['password1'] == user.password1:
                request.session['name'] = user.username
                request.session['auth'] = 'true'
                return HttpResponseRedirect(reverse('home_page'))
        return render(request, 'blog/login.html', context={'form': bound_form})

def session_del(request):
    del request.session['auth']
    return HttpResponseRedirect(reverse('home_page'))