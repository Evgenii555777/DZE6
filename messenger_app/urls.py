from django.urls import path
from . import views

app_name = 'messenger_app'

urlpatterns = [
    path('registration/', views.register_user, name='register'),
    path('profile/<int:user_id>/', views.user_profile, name='user_profile'),
    path('login/', views.login, name='login'),
    path('chat/create/', views.create_chat_view, name='create_chat'),
    path('chat/<int:chat_id>/', views.chat_details, name='chat_details'),
    path('message/send/', views.send_message, name='send_message'),
    path('message/chat/<int:chat_id>/', views.get_messages, name='get_messages'),
    path('chat/', views.chat_page, name='chat'),
    path('api/register/', views.register_user),
    path('api/profile/', views.update_profile, name='update_profile'),
    path('api/messages/', views.send_message, name='send_message'),
    path('api/chats/', views.create_chat_view, name='create_chat'),
    path('api/group-chats/', views.create_chat_view, name='create_group_chat'),
    path('user-list/', views.user_list, name='user_list'),
    path('create_chat/', views.create_chat_view, name='create_chat'),
]
