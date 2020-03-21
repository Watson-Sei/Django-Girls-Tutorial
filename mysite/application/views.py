from django.shortcuts import render, get_object_or_404, redirect
from django.http.response import JsonResponse
from django.utils import timezone
from .models import Post, Like, Question, QuestionLike, Question2
from .forms import PostForm, QuestionForm
from django.contrib.auth.models import User
from django.views.generic import View, TemplateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'application/post_list.html', {'posts': posts})


@login_required
def post_detail(request, pk, **kwargs):
    post = get_object_or_404(Post, pk=pk)
    print(type(post))
    question = Question.objects.filter(post=post)
    question_is_like = Like.objects.filter(user=request.user).filter(post=post).count()
    question2 = Question2.objects.filter(post=post)
    return render(request, 'application/post_detail.html',
                  {'post': post, 'question_is_like': question_is_like, 'question': question, 'question2': question2})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('application:post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'application/post_edit.html', {'form': form})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('application:post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'application/post_edit.html', {'form': form})


# Like Function View

class Like_Detail(View):
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(id=pk)
        is_like = Like.objects.filter(user=self.request.user).filter(post=post).count()
        # unlike
        if is_like > 0:
            liking = Like.objects.get(post__id=pk, user=self.request.user)
            liking.delete()
            post.like_num -= 1
            post.save()
            post = get_object_or_404(Post, pk=pk)
            json = {'like_value': post.like_num}
            return JsonResponse(json)
        # like
        post.like_num += 1
        post.save()
        like = Like()
        like.user = self.request.user
        like.post = post
        like.save()
        post = get_object_or_404(Post, pk=pk)
        json = {'like_value': post.like_num}
        return JsonResponse(json)


""" コメントView """
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from .models import Comment, Reply
from .forms import CommentForm, ReplyForm


class CommentFormView(CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        comment = form.save(commit=False)
        post_pk = self.kwargs['pk']
        comment.post = get_object_or_404(Post, pk=post_pk)
        comment.save()
        return redirect('application:post_detail', pk=post_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_pk = self.kwargs['pk']
        context['post'] = get_object_or_404(Post, pk=post_pk)
        return context


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('application:post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('application:post_detail', pk=comment.post.pk)


class ReplyFormView(CreateView):
    model = Reply
    form_class = ReplyForm

    def form_valid(self, form):
        reply = form.save(commit=False)
        comment_pk = self.kwargs['pk']
        reply.comment = get_object_or_404(Comment, pk=comment_pk)
        reply.save()
        return redirect('application:post_detail', pk=reply.comment.post.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment_pk = self.kwargs['pk']
        context['comment'] = get_object_or_404(Comment, pk=comment_pk)
        return context


@login_required
def reply_approve(request, pk):
    reply = get_object_or_404(Reply, pk=pk)
    reply.approve()
    return redirect('application:post_detail', pk=reply.comment.post.pk)


@login_required
def reply_remove(request, pk):
    reply = get_object_or_404(Reply, pk=pk)
    reply.delete()
    return redirect('application:post_detail', pk=reply.comment.post.pk)


# Question function View

class QuestionDetail(TemplateView):
    template_name = 'application/question.html'

    def get(self, request, **kwargs):
        url_path = request.get_full_path()
        if '/question/' in url_path:
            question_id = self.kwargs['question_id']
            print(question_id)
            question = get_object_or_404(Question, pk=question_id)
            question_is_like = QuestionLike.objects.filter(user=self.request.user).filter(question=question)
            context = {
                'question': question,
                'question_is_like': question_is_like,
                'post_pk': self.kwargs['pk']
            }
            return self.render_to_response(context)

        elif '/question2/' in url_path:
            question_id = self.kwargs['question_id']
            print(question_id)
            question2 = get_object_or_404(Question2, pk=question_id)
            context = {
                'question':question2,
                'question_is_like':0,
                'post_pk': self.kwargs['pk']
            }
            return self.render_to_response(context)


class QeustionEdit(View):

    def get(self, request, **kwargs):
        self.question = self.kwargs['pk']
        form = QuestionForm()
        return render(request, 'application/question_edit.html', {'form': form, 'post_id': self.question})

    def post(self, request, **kwargs):
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = self.request.user
            question.post = Post.objects.get(pk=self.kwargs['pk'])
            form.save()
            return redirect('application:post_detail', pk=self.kwargs['pk'])
        return render(request, 'application/question_edit.html', {'form': QuestionForm()})


class QeustionEdit2(View):

    def get(self, request, **kwargs):
        self.question = self.kwargs['pk']
        form = QuestionForm()
        return render(request, 'application/question_edit2.html', {'form': form, 'post_id': self.question})

    def post(self, request, **kwargs):
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = self.request.user
            question.post = Post.objects.get(pk=self.kwargs['pk'])
            form.save()
            return redirect('application:post_detail', pk=self.kwargs['pk'])
        return render(request, 'application/question_edit2.html', {'form': QuestionForm()})


class QuestionLikeDetail(View):
    def get(self, request, *args, **kwargs):
        question = Question.objects.get(id=self.kwargs['question_id'])
        question_is_like = QuestionLike.objects.filter(user=self.request.user).filter(question=question).count()
        # unlike
        if question_is_like > 0:
            liking = QuestionLike.objects.get(question__id=self.kwargs['question_id'], user=self.request.user)
            liking.delete()
            question.like_num -= 1
            question.save()
            question = get_object_or_404(Question, pk=self.kwargs['question_id'])
            json = {'question_value': question.like_num}
            return JsonResponse(json)

        # like
        question.like_num += 1
        question.save()
        like = QuestionLike()
        like.user = self.request.user
        like.question = question
        like.save()
        question = get_object_or_404(Question, pk=self.kwargs['question_id'])
        json = {'question_value': question.like_num}
        return JsonResponse(json)
