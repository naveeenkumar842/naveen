
from django.shortcuts import render , get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User

from django.views.generic import (
    ListView , DetailView, CreateView,
    UpdateView ,DeleteView )


from django.contrib.auth.mixins import \
    LoginRequiredMixin , UserPassesTestMixin


from .models import Post

# posts = [
#     {
#         'author' : 'Srinivas',
#         'title' : 'Blog Post 1',
#         'content' : 'First Post content',
#         'date_posted' : 'August 22, 2019'
#     },
#
#     {
#         'author' : 'Virat',
#         'title' : 'Blog Post 2',
#         'content' : 'Second Post content',
#         'date_posted' : 'August 21, 2019'
#     }
# ]

def home(request):
    context = {
        'posts' : Post.objects.all()
    }
    return render(request,'blog/home.html',context)


def about(request):
    return render(request,'blog/about.html',{'title':'About'})




class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <appName>/<modelName>_<viewType>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']


    paginate_by = 5  # for each page 5 records displa





class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <appName>/<modelName>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5  # for each page 5 records displa


    def get_queryset(self):
        user = get_object_or_404(
            User,
            username=self.kwargs.get('username')
        )

        return Post.objects.filter(author=user).order_by('-date_posted')




class PostDetailView(DetailView):
    model = Post
    # template_name = 'post_detail.html'
    #context_object_name = 'post'  or  'object'



class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title','content']


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)



class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,
                     UpdateView):
    model = Post
    fields = ['title','content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()

        if self.request.user == post.author:
            return True
        return False



class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,
                     DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()

        if self.request.user == post.author:
            return True
        return False





def LatestListView(request):
    latest_posts = Post.objects.all().order_by('-date_posted')[:3]

    return render(request,'blog/latest_posts.html',
                  {'latest_posts':latest_posts})


def top_questions(request):
    return render(request,'blog/top_questions.html')



def blog_python_view(request):
    return render(request,'blog/python.html')



