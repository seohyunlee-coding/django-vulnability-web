from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.template import Template, Context

from .models import Post
from .forms import PostForm

def index(request):
    posts = Post.objects.order_by('-created_at')[:20]
    return render(request, 'board/index.html', {'posts': posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            p = form.save(commit=False)
            p.author = request.user
            p.save()
            return redirect('index')
    else:
        form = PostForm()
    return render(request, 'board/create.html', {'form': form})

def search_raw(request):
    """Deliberately unsafe raw SQL search to demonstrate SQL injection."""
    q = request.GET.get('q', '')
    posts = []
    if q:
        # WARNING: insecure raw SQL concatenation (SQLi demonstration)
        with connection.cursor() as cur:
            cur.execute("SELECT id, title, body FROM board_post WHERE title LIKE '%%" + q + "%%'")
            rows = cur.fetchall()
        for r in rows:
            posts.append({'id': r[0], 'title': r[1], 'body': r[2]})
    return render(request, 'board/search.html', {'posts': posts, 'q': q})

@csrf_exempt
def delete_post(request, post_id):
    """CSRF exempt delete — intentional vulnerability."""
    post = get_object_or_404(Post, pk=post_id)
    # Logical flaw: any authenticated user can delete any post
    if request.user.is_authenticated:
        post.delete()
        return redirect('index')
    return redirect('index')

def ssti_demo(request):
    """Demonstrate a server-side template injection-like behavior by rendering user input as a template."""
    expr = request.GET.get('tpl', '')
    rendered = ''
    if expr:
        # WARNING: intentionally rendering user input as template
        t = Template(expr)
        rendered = t.render(Context({'user': request.user, 'posts': Post.objects.all()}))
    return render(request, 'board/ssti.html', {'rendered': rendered, 'expr': expr})

def home(request):
    query = request.GET.get('query', '')
    if query:
        posts = Post.objects.filter(title__icontains=query)
    else:
        posts = Post.objects.all().order_by('-created_at')[:5]  # 최근 5개 포스트
    return render(request, 'board/home.html', {'posts': posts, 'query': query})
