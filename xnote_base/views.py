from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http.response import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from xnote_base.models import Person, Post, SuperConductor, Follow
from django.db.models import Q


def main_page(request):
    if request.user.is_authenticated():
        user = request.user
        person = Person.objects.get(user__username=user.username)
        post_list = Post.objects.filter(author__in=person.follows.all()).order_by('-publish_time')
        suggestions = SuperConductor.objects.exclude(
            Q(url_name=person.url_name) | Q(followers__url_name=person.url_name))
        return render(request, 'xnote_base/userindex.html', {
            'user': request.user,
            'post_list': post_list,
            'suggestions': suggestions,
        })
    else:
        post_list = Post.objects.filter(author__is_formal=True, is_public=True).order_by('-publish_time')
        return render(request, 'xnote_base/index.html', {'post_list': post_list})


@login_required
def settings(request):
    return None


@login_required
def my_profile(request):
    post_list = Post.objects.filter(author=request.user.person)
    return render(request, 'xnote_base/profile.html', {
        'user': request.user,
        'post_list': post_list,
    })


def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect(reverse('xnote_base:main_page'))
        else:
            return HttpResponse('you cannot login because you are blocked.')
    else:
        return HttpResponse('username or password is wrong. please check your spelling and try again...')


def signup(request):
    if request.method == 'POST':
        post = request.POST
        user = User.objects.create_user(post['username'], post['username'], post['password'])
        user.first_name = post['first_name']
        user.last_name = post['last_name']
        person = Person()
        person.user = user
        user.save()
        person.save()
        user = authenticate(username=post['username'], password=post['password'])
        login(request, user)
        return HttpResponseRedirect(reverse('xnote_base:main_page'))
    else:
        return render(request, 'xnote_base/signup.html')


@login_required
def view_page(request, name):
    super_conductor = get_object_or_404(SuperConductor, url_name=name)
    post_list = Post.objects.filter(author=super_conductor).order_by('-publish_time')
    return render(request, 'xnote_base/person.html', {
        'super_conductor': super_conductor,
        'post_list': post_list,

    })


@login_required
def followers_page(request):
    person = request.user.person
    follower_list = Person.objects.filter(following_follow_obj__followed=person)
    return render(request, 'xnote_base/followers_page.html', {
        'user': request.user,
        'follower_list': follower_list,
    })


@login_required
def following_page(request):
    person = request.user.person
    followed_list = SuperConductor.objects.filter(followers_follow_obj__follower=person)
    return render(request, 'xnote_base/following_page.html', {
        'user': request.user,
        'followed_list': followed_list,
    })


def log_out(request):
    if request.user.is_authenticated():
        logout(request)
    return HttpResponseRedirect(reverse('xnote_base:main_page'))


def check_username(request):
    username = request.GET['username']
    if User.objects.filter(username=username).count() == 0:
        return HttpResponse('valid')
    else:
        return HttpResponse('invalid')


@login_required
def follow(request):
    name = request.GET['name']
    conductor = SuperConductor.objects.get(url_name=name)
    person = request.user.person
    follow_obj = Follow.objects.create(follower=person, followed=conductor, follow_time=timezone.now())
    follow_obj.save()
    return HttpResponse('ok')


@login_required
def new_post(request):
    if request.method == 'GET':
        user = request.user
        permission_group_list = SuperConductor.objects.all()
        return render(request, 'xnote_base/new_post.html', {
            'user': user,
            'permission_group_list': permission_group_list,
        })
    else:
        # return HttpResponse()
        pass