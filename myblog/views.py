from django.contrib.auth.models import User

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from django.views.generic import ListView, DetailView, UpdateView

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.utils import timezone

from django.urls import reverse_lazy

from .forms import NewTopicForm, PostForm

from . models import Board, Topic, Post

# Create your views here.

class HomeView(ListView):
    template_name = 'myblog/index.html'
    model = Board

# Board HTML with list of topics
class BoardView(ListView):
    template_name = 'myblog/board.html'
    model = Topic
    context_object_name = 'topics'
    paginate_by = 10


    def get_context_data(self, **kwargs):
        kwargs['board'] = self.board
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.board = get_object_or_404(Board, pk=self.kwargs.get('pk'))
        queryset = self.board.topics.order_by('-last_updated')
        return queryset

# Topic HTML with list of posts
class TopicView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'myblog/topic.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        session_key = 'viewed_topic_{}'.format(self.topic.pk)  # <-- here
        if not self.request.session.get(session_key, False):
            self.topic.views += 1
            self.topic.save()
            self.request.session[session_key] = True

        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get('board_pk'), pk=self.kwargs.get('pk'))
        queryset = self.topic.posts.order_by('created_at')
        return queryset

# Form to create a new TOPIC with the first POST inside of that topic
@login_required
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.last_updated = timezone.now()
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            return HttpResponseRedirect(reverse('myblog:topic', args=[topic.board.pk, topic.pk]))
    else:
        form = NewTopicForm()
    return render(request, 'myblog/new_topic.html', {'board': board, 'form': form})


# View to reply (write a POST) within a TOPIC thread
@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()

            topic.last_updated = timezone.now()
            topic.save()

            return HttpResponseRedirect(reverse('myblog:topic', args=[pk, topic_pk]))
    else:
        form = PostForm()
    return render(request, 'myblog/reply_topic.html', {'topic': topic, 'form': form})

# Updating/editing your own POST
@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = ('message', )
    template_name = 'myblog/edit_post.html'
    # pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.topic.last_updated = timezone.now()
        post.topic.save()
        post.save()
        return HttpResponseRedirect(reverse('myblog:topic', args=[post.topic.board.pk, post.topic.pk]))


@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email', )
    template_name = 'myblog/my_account.html'
    success_url = reverse_lazy('myblog:my_account')

    def get_object(self):
        return self.request.user
