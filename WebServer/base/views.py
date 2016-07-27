# -*- coding: utf-8 -*-
import string
import random

from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import View

from .models import ChatRoom


def getRoomID(size=8, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class IndexView(View):
    def get(self, request):
        return render(request, 'base/main.html')


class CreateChatView(View):
    def get(self, request):
        return render(request, 'test/create_chat.html')

    def post(self, request):
        room_id = getRoomID()
        chat_room = ChatRoom(room_id=room_id)
        chat_room.save()

        context = {
            'room_id': room_id
        }
        return render(request, 'test/join_room.html', context)


class JoinChatView(View):
    def get(self, request):
        return render(request, 'test/join_room.html')

    def post(self, request):
        if request.POST['room_id']:
            if ChatRoom.objects.filter(room_id=request.POST['room_id']).exists():
                context = {
                    'room_id': request.POST['room_id']
                }
                return render(request, 'test/chat.html', context)
            else:
                return HttpResponse("Chat room does not exist.")
        return HttpResponse("Please enter a valid chat room ID.")

