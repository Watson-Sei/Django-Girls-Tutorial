from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField
from django.utils.safestring import mark_safe
from markdownx.utils import markdownify


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    like_num = models.IntegerField(default=0)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Like(models.Model):
    """ Like """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='like_user')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments'
    )
    author = models.CharField(max_length=50)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']

    def approve(self):
        self.approved = True
        self.save()

    def __str__(self):
        return self.text


class Reply(models.Model):
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name='replies'
    )
    author = models.CharField(max_length=50)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def approve(self):
        self.approved = True
        self.save()

    def __str__(self):
        return self.text


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='question_user')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    title = models.CharField(verbose_name='title', max_length=200)
    text = MarkdownxField(verbose_name='text')
    created_at = models.DateTimeField(default=timezone.now)
    like_num = models.IntegerField(default=0)
    """ カスタムメソッド """

    def get_text_markdownx(self):
        return mark_safe(markdownify(self.text))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Question'


class QuestionLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='question_like_user')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)


from mdeditor.fields import MDTextField


class Question2(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='question2_user')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    title = models.CharField(verbose_name='title', max_length=200)
    content = MDTextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Question2'
        verbose_name_plural = 'Question2'
