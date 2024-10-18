from blog_app.models import Post
from django.shortcuts import redirect
from django.utils import timezone
from blog_app.forms import PostForm
from django.views.generic import ListView,DetailView,View,CreateView,UpdateView
from blog_app.models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

class PostListView(ListView):
    model = Post
    template_name = "post_list.html"
    context_object_name = "posts"
    
    def get_queryset(self):
        return Post.objects.filter(published_at__isnull=False).order_by("-published_at")

    
class PostDetailView(DetailView):
    model = Post
    template_name = "post_detail.html"
    context_object_name = "post"
    
    def get_queryset(self):
        queryset = Post.objects.filter(pk=self.kwargs["pk"],published_at__isnull=False)
        return queryset
    

class DraftListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "draft_list.html"
    context_object_name = "posts"
    
    def get_queryset(self):
        queryset = Post.objects.filter( published_at__isnull=True).order_by("-published_at")
        return queryset

class DraftDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = "post_detail.html"
    context_object_name = "post"
    def get_queryset(self):
        queryset =  Post.objects.filter(pk=self.kwargs["pk"],published_at__isnull=True)
        return queryset
    

class DraftPublishView(LoginRequiredMixin,View):
    def get(self,request,pk):
        post=post.objects.get(pk=pk)
        post.published_at= timezone.now()
        post.save()
        return redirect("post-detail",pk=post.pk)


class PostDeleteView(LoginRequiredMixin,View):
    def get(self,request,pk):
        post = Post.objects.get(pk=pk)
        post.delete()
        return redirect("post-list")
    
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "post_create.html"
    form_class = PostForm
    success_url = reverse_lazy("post-list")
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    

class PostUpdateView(LoginRequiredMixin,UpdateView):
    model = Post
    template_name = "post_create.html"
    form_class = PostForm
    
    def get_success_url(self):
        post = self.get_object()
        if post.published_at:
            return reverse_lazy("post-detail",kwargs={"pk":post.pk})
        else:
            return reverse_lazy("draft-detail",kwargs={"pk":post.pk}) 







    