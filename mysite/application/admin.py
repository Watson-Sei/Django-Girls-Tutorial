from django.contrib import admin
from .models import Post,Like,Question
from markdownx.admin import MarkdownxModelAdmin

admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Question,MarkdownxModelAdmin)