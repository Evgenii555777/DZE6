from django.contrib.auth.models import User
from .models import Chat, Message, UserProfile
from .serializers import UserSerializer, ChatSerializer, MessageSerializer, UserProfileSerializer
from django.shortcuts import render
from rest_framework.permissions import BasePermission, IsAuthenticatedOrReadOnly
from rest_framework.decorators import permission_classes
from django.contrib.auth import views as auth_views
from rest_framework import status
from rest_framework.request import Request
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.files.storage import FileSystemStorage


def register_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.POST)
        if serializer.is_valid():
            user = serializer.save()

            try:
                profile = UserProfile.objects.get(user=user)
            except UserProfile.DoesNotExist:
                profile = UserProfile(user=user)
                profile.save()

            return render(request, 'registration_success.html', {'user': user})
        return render(request, 'registration.html', {'serializer': serializer})
    else:
        serializer = UserSerializer()
        return render(request, 'registration.html', {'serializer': serializer})


@api_view(['GET', 'PUT', 'POST'])
def user_profile(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        profile = UserProfile.objects.get_or_create(user=user)[0]

        if request.method == 'POST':
            profile_picture = request.FILES.get('profilePicture')
            if profile_picture:
                profile.avatar = profile_picture
                profile.save()
                return JsonResponse({'status': 'success', 'avatar': profile.avatar.url})

        users = User.objects.all()
        chats = Chat.objects.all()

        context = {
            'user': user,
            'profile': profile,
            'users': users,
            'chats': chats
        }

        return render(request, 'profile.html', context)
    except User.DoesNotExist:
        return render(request, 'error.html', {'message': 'User does not exist'})
    except UserProfile.DoesNotExist:
        return render(request, 'error.html', {'message': 'UserProfile does not exist'})


@api_view(['POST'])
def create_chat_view(request):
    serializer = ChatSerializer(data=request.data)
    if serializer.is_valid():
        chat = serializer.save()
        return Response({'message': 'Group chat created successfully'}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def chat_details(request, chat_id, format=None):
    try:
        chat = Chat.objects.get(id=chat_id)
    except Chat.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = ChatSerializer(chat)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ChatSerializer(chat, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    elif request.method == 'DELETE':
        chat.delete()
        return Response(status=204)


@api_view(['POST'])
def send_message(request):
    serializer = MessageSerializer(data=request.data)
    if serializer.is_valid():
        message = serializer.save(sender=request.user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['GET'])
def get_messages(request, chat_id):
    try:
        chat = Chat.objects.get(id=chat_id)
    except Chat.DoesNotExist:
        return Response(status=404)

    messages = Message.objects.filter(chat=chat).order_by('timestamp')
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)


def chat_page(request):
    chats = Chat.objects.all()
    return render(request, 'chat.html', {'chats': chats})



@api_view(['PUT'])
@permission_classes([IsAuthenticatedOrReadOnly])
def update_profile(request):
    name = request.data.get('name')
    avatar = request.data.get('avatar')
    user = request.user
    user.profile.name = name
    user.profile.avatar = avatar
    user.profile.save()
    data = {
        'name': user.profile.name,
        'avatar': user.profile.avatar.url,
    }
    return Response(data)


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        return obj.user == request.user

def login(request):
    return auth_views.LoginView.as_view(template_name='login.html')(request)

def user_list(request):
    users = User.objects.all()
    chats = Chat.objects.all()
    context = {'users': users, 'chats': chats}
    return render(request, 'user_list.html', context)