from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from .models import Post
from .forms import EmailPostField
from site_blog.settings import EMAIL_HOST_USER


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_share(request, post_id):
    post = get_object_or_404(Post,
                             id=post_id,
                             status=Post.Status.PUBLISHED)

    sent_flag = False

    if request.method == 'POST':
        form = EmailPostField(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f'{cd["name"]} recommends you read {post.title}'
            message = f'{cd["name"]}\u0027s comments: {cd["comments"]}'
            send_mail(subject, message, EMAIL_HOST_USER, [cd['to']])
            sent_flag = True
    else:
        form = EmailPostField()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent_flag})


def post_detail(request, year, month, day, post_slug):
    post = get_object_or_404(Post, slug=post_slug, publish__year=year, 
                             publish__month=month, publish__day=day, 
                             status=Post.Status.PUBLISHED)
    return render(request, 'blog/post/detail.html', {'post': post})
