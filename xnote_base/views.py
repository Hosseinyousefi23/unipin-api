from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from rest_framework import viewsets

from xnote_base.forms import LoginForm
from xnote_base.models import Person, Post
from xnote_base.serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


def main_page(request):
    if request.user.is_authenticated:
        user = request.user
        person = Person.objects.get(user__username=user.username)
        event_list = Post.objects.order_by('-publish_time')
        # suggestions = Person.objects.exclude(
        #     Q(url_name=person.url_name) | Q(followers__url_name=person.url_name))
        if 'platform' in request.GET and request.GET['platform'] == 'android':
            return JsonResponse({
                'user': request.user.first_name + ' ' + request.user.last_name,
                'event_list': serializers.serialize('json', event_list),
                # 'suggestions': serializers.serialize('json', suggestions),
                'author_list': serializers.serialize('json', person.follows.all()),
            })
        else:
            return render(request, 'xnote_base/userindex.html', {
                'user': request.user,
                'event_list': event_list,
                # 'suggestions': suggestions,
            })
    else:
        event_list = Post.objects.order_by('-publish_time')
        if 'platform' in request.GET and request.GET['platform'] == 'android':
            return JsonResponse({'event_list': serializers.serialize('json', event_list)})
        else:
            form = LoginForm()
            return render(request, 'xnote_base/index.html', {'event_list': event_list, 'form': form})


@login_required
def settings(request):
    return None


@login_required
def my_profile(request):
    event_list = Post.objects.filter(author=request.user.person)
    if 'platform' in request.GET and request.GET['platform'] == 'android':
        return JsonResponse({
            'user': request.user.first_name + ' ' + request.user.last_name,
            'event_list': serializers.serialize('json', event_list)
        })
    else:
        return render(request, 'xnote_base/profile.html', {
            'user': request.user,
            'event_list': event_list,
        })


def login_view(request):
    if 'platform' in request.GET and request.GET['platform'] == 'android':
        username = request.GET['username']
        password = request.GET['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponse('ok')
            else:
                return HttpResponse('not_active')
        else:
            return HttpResponse('wrong')
    else:
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(username=login_form.cleaned_data['username'],
                                password=login_form.cleaned_data['password'])

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('xnote_base:main_page'))
                else:
                    return HttpResponse('you cannot login because you are blocked.')
            else:
                return HttpResponse('username or password is wrong. please check your spelling and try again...')
        else:
            event_list = Post.objects.filter(author__is_formal=True, is_public=True).order_by('-publish_time')
            return render(request, 'xnote_base/index.html', {'form': login_form, 'event_list': event_list})


def forgot_password(request):
    return render(request, 'xnote_base/forgot_password.html', {})


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
        if 'platform' in request.GET and request.GET['platform'] == 'android':
            return JsonResponse({
                'message': 'redirect to main page'
            })
        else:
            return HttpResponseRedirect(reverse('xnote_base:main_page'))
    else:
        if 'platform' in request.GET and request.GET['platform'] == 'android':
            return JsonResponse({
                'message': 'sign-up page'
            })
        else:
            return render(request, 'xnote_base/signup.html')


@login_required
def view_page(request, name):
    person = get_object_or_404(Person, url_name=name)
    post_list = Post.objects.filter(author=person).order_by('-publish_time')
    if 'platform' in request.GET and request.GET['platform'] == 'android':
        return JsonResponse({
            'person': serializers.serialize('json', person),
            'post_list': serializers.serialize('json', post_list),
        })
    else:
        return render(request, 'xnote_base/person.html', {
            'person': person,
            'post_list': post_list,

        })


# @login_required
# def followers_page(request):
#     person = request.user.person
#     follower_list = Person.objects.filter(following_follow_obj__followed=person)
#     if 'platform' in request.GET and request.GET['platform'] == 'android':
#         return JsonResponse({
#             'user': request.user.first_name + ' ' + request.user.last_name,
#             'follower_list': serializers.serialize('json', follower_list)
#         })
#     else:
#         return render(request, 'xnote_base/followers_page.html', {
#             'user': request.user,
#             'follower_list': follower_list,
#         })


# @login_required
# def following_page(request):
#     person = request.user.person
#     followed_list = SuperConductor.objects.filter(followers_follow_obj__follower=person)
#     if 'platform' in request.GET and request.GET['platform'] == 'android':
#         return JsonResponse({
#             'user': request.user.first_name + ' ' + request.user.last_name,
#             'follower_list': serializers.serialize('json', followed_list)
#         })
#     else:
#         return render(request, 'xnote_base/following_page.html', {
#             'user': request.user,
#             'followed_list': followed_list,
#         })


def log_out(request):
    if request.user.is_authenticated:
        logout(request)
    if 'platform' in request.GET and request.GET['platform'] == 'android':
        return JsonResponse({
            'message': 'redirect to main page'
        })
    else:
        return HttpResponseRedirect(reverse('xnote_base:main_page'))


def check_username(request):
    username = request.GET['username']
    if User.objects.filter(username=username).count() == 0:
        return HttpResponse('valid')
    else:
        return HttpResponse('invalid')


# @login_required
# def follow(request):
#     name = request.GET['name']
#     conductor = SuperConductor.objects.get(url_name=name)
#     person = request.user.person
#     follow_obj = Follow.objects.create(follower=person, followed=conductor, follow_time=timezone.now())
#     follow_obj.save()
#     return HttpResponse('ok')


# def unfollow(request):
#     print("unfollow")
#     name = request.GET['name']
#     conductor = SuperConductor.objects.get(url_name=name)
#     person = request.user.person
#     Follow.objects.filter(follower=person, followed=conductor).delete()
#     return HttpResponse('ok')

def single_post(request):
    return render(request, '../templates/xnote_base/single_post.html', {})


@login_required
def new_post(request):
    if request.method == 'GET':
        user = request.user

        # permission_group_list = SuperInstitution.objects.filter(
        #     (Q(membership_obj__person=user.person) & (
        #             Q(membership_obj__is_admin=True) | Q(membership_obj__portfolio__permissions__name='create_post'))))

        '''

            (Q(__class______name__='Person') & Q(url_name=user.person.url_name)) | (
                Q(__class______name__='SuperInstitution') & Q(membership_obj__person=user.person) & (
                    Q(membership_obj__is_admin=True) | Q(membership_obj__portfolio__permissions__name='create_post')))
         '''
        if 'platform' in request.GET and request.GET['platform'] == 'android':
            return JsonResponse({
                'user': request.user.person.real_name,
                # 'permission_group_list': serializers.serialize('json', permission_group_list),
            })
        else:
            return render(request, 'xnote_base/new_post.html', {
                'person': user.person,
                # 'permission_group_list': permission_group_list,
            })
    else:
        author_name = request.POST['as']
        title = request.POST['title']
        context = request.POST['context']
        is_public = True if request.POST['is_public'] == "public" else False
        author = Person.objects.get(url_name=author_name)
        author.post_set.create(title=title, context=context, publish_time=timezone.now(), author=author,
                               is_public=is_public)
        return HttpResponseRedirect(reverse("xnote_base:view_page", kwargs={'name': author_name}))

# def new_group(request):
#     group_form = GroupForm()
#     return render(request, 'xnote_base/create_new_group.html', {'form': group_form})


# def new_group_action(request):
#     group_form = GroupForm(request.POST)
#     group = group_form.save(commit=False)
#     group.real_type = ContentType.objects.get(model='group', app_label='xnote_base')
#     group.is_department_group = False
#     group.is_formal = False
#     group.save()
#     group_form.save_m2m()
#     return HttpResponseRedirect(reverse('xnote_base:view_page', kwargs={'name': group.url_name}))
