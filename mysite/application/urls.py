from django.urls import path
from . import views
from .views import Like_Detail
from .views import (CommentFormView,comment_approve,comment_remove,ReplyFormView,reply_approve,reply_remove,QuestionDetail,QeustionEdit,QuestionLikeDetail)

app_name = 'application'
urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/like/',Like_Detail.as_view(), name='get'),
    path('post/<int:pk>/comment/',CommentFormView.as_view(), name='comment_form'),
    path('post/<int:pk>/comment/approve/', comment_approve, name='comment_approve'),
    path('post/<int:pk>/comment/remove/', comment_remove, name='comment_remove'),
    path('post/<int:pk>/reply/', ReplyFormView.as_view(), name='reply_form'),
    path('post/<int:pk>/reply/approve/', reply_approve, name='reply_approve'),
    path('post/<int:pk>/reply/remove/', reply_remove, name='reply_remove'),
    path('post/<int:pk>/question/<int:question_id>/',QuestionDetail.as_view(),name='get'),
    path('post/<int:pk>/question/edit/',QeustionEdit.as_view(),name='get'),
    path('post/<int:pk>/question/edit/',QeustionEdit.as_view(),name='post'),
    path('post/<int:pk>/question/<int:question_id>/like/',QuestionLikeDetail.as_view(),name='get'),
]