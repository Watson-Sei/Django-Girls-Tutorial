from django.contrib import admin
from .models import Post,Like,Question,QuestionLike, Question2
from markdownx.admin import MarkdownxModelAdmin

admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Question,MarkdownxModelAdmin)
admin.site.register(QuestionLike)
admin.site.register(Question2)
