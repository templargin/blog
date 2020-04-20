from django.urls import path

from . import views

app_name = 'myblog'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('boards/<int:pk>/', views.BoardView.as_view(), name='board'),
    path('boards/<int:board_pk>/topics/<int:pk>/', views.TopicView.as_view(), name='topic'),
    path('boards/<int:pk>/new', views.new_topic, name='new_topic'),
    path('boards/<int:pk>/topics/<int:topic_pk>/reply', views.reply_topic, name='reply_topic'),

    path('boards/<int:board_pk>/topics/<int:topic_pk>/posts/<int:pk>/edit', views.PostUpdateView.as_view(), name='edit_post'),
    path('settings/about/', views.UserUpdateView.as_view(), name='my_account'),


    # path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # path('<int:question_id>/vote/', views.vote, name='vote'),
]
