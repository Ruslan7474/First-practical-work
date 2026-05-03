from collections import defaultdict

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import NewsCommentForm
from .models import News, NewsComment


def news_page(request):
    events = News.objects.all()
    return render(request, 'news/news_page.html', {'events': events})


def news_detail(request, news_id):
    event = get_object_or_404(News, pk=news_id)
    other_news = News.objects.exclude(pk=event.pk).order_by("-published_at")[:12]

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect(f"/accounts/login/?next=/news/{event.pk}/")

        form = NewsCommentForm(request.POST)
        if form.is_valid():
            parent = None
            parent_id = request.POST.get("parent_id")
            if parent_id:
                parent = NewsComment.objects.filter(pk=parent_id, news=event).first()

            NewsComment.objects.create(
                news=event,
                user=request.user,
                parent=parent,
                text=form.cleaned_data["text"].strip(),
            )
            return redirect(f"/news/{event.pk}/#comments")
        messages.error(request, "Не удалось отправить комментарий.")
    else:
        form = NewsCommentForm()

    flat_comments = list(
        NewsComment.objects.filter(news=event).select_related("user").order_by("created_at")
    )
    children_map = defaultdict(list)
    for comment in flat_comments:
        children_map[comment.parent_id].append(comment)

    def attach_tree(node):
        node.tree_children = children_map.get(node.id, [])
        for child in node.tree_children:
            attach_tree(child)

    comment_roots = children_map.get(None, [])
    for root in comment_roots:
        attach_tree(root)

    return render(
        request,
        "news/news_detail.html",
        {
            "event": event,
            "other_news": other_news,
            "comment_roots": comment_roots,
        },
    )
