from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailPostForm, CommentForm, PostForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
# from django.http import Http404
# Create your views here.

def home(request):
    sent = False
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            sent = True
    else:
        form = PostForm()
    return render(request, 'home.html', {'form':form, 'sent':sent})


def post_list(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'list.html', {'posts':posts})


# def post_detail(request, id):
#     try:
#         post = Post.published.all(id=id)
#     except Post.DoesNotExist:
#         raise Http404('Post not found.')
#     return render(request, 'detail.html', {'post':post})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    comments = post.comments.filter(active=True)
    form = CommentForm()
    return render(request, 'detail.html', {'post':post, 'form':form, 'comments':comments})


def post_share(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} requests you to read {post.title}"
            message = f"Read {post.title} at {post_url}.\n\n" \
                      f"{cd['name']} \'s comments : {cd['comments']}"
            send_mail(subject, message, cd['email'], [cd['to']])
            sent = True

    else:
        form = EmailPostForm()
    return render(request, 'share.html', {'post':post, 'form':form, 'sent':sent})


#@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comment = None
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
    else:
        form = CommentForm()
    return render(request, 'comment.html', {'post':post, 'form':form, 'comment':comment})

