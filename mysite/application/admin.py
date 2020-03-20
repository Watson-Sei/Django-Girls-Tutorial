from django.contrib import admin
from .models import Post,Like,Question,QuestionLike
from markdownx.admin import MarkdownxModelAdmin

admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Question,MarkdownxModelAdmin)
admin.site.register(QuestionLike)