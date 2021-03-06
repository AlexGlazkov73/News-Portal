from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post, Comment
from .filters import PostFilter


class PostList(ListView):
    model = Post
    ordering = '-time_create'
    template_name = 'news.html'
    context_object_name = 'posts'
    paginate_by = 1

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class CommentList(ListView):
    model = Comment
    template_name = 'post.html'
    context_object_name = 'comments'
