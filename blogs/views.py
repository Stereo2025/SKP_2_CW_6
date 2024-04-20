from pytils.translit import slugify
from blogs.forms import BlogForm
from blogs.models import Blog
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class ArticleListView(LoginRequiredMixin, ListView):
    """Просмотр всех статей."""
    model = Blog
    template_name = 'blog/blog_list.html'

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset().filter(is_published=True)


class ArticleDetailView(LoginRequiredMixin, DetailView):
    """Просмотр одной статьти"""
    model = Blog
    template_name = 'blog/blog_detail.html'

    def get_object(self, queryset=None, increment=True):
        obj = super().get_object(queryset)
        if increment:
            obj.views_count += 1
            obj.save()
        return obj


class ArticleCreateView(LoginRequiredMixin, CreateView):
    """Создание статьи"""
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('blogs:articles')
    template_name = 'blog/blog_form.html'

    def form_valid(self, form):
        new_article = form.save(commit=False)
        new_article.user = self.request.user
        new_article.slug = slugify(new_article.title)
        new_article.save()
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Изменение статьи"""
    model = Blog
    form_class = BlogForm
    template_name = 'blog/blog_form.html'

    def test_func(self):
        user = self.request.user
        if user == self.get_object().user or user.has_perm('blogs.change_blog'):
            return True
        return self.handle_no_permission()

    def form_valid(self, form):
        new_article = form.save(commit=False)
        new_article.user = self.request.user
        new_article.slug = slugify(new_article.title)
        new_article.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blogs:view', args=[self.kwargs.get('slug')])


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Удаление статьи"""
    model = Blog
    success_url = reverse_lazy('blogs:articles')
    template_name = 'blog/blog_confirm_delete.html'

    def test_func(self):
        user = self.request.user
        if user == self.get_object().user or user.has_perm('blogs.delete_blog'):
            return True
        return self.handle_no_permission()
