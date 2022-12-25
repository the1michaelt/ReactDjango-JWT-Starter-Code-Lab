from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from .models import Reply
from .serializers import ReplySerializer

# Create your views here.


@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_replies(request):
    replies = Reply.objects.all()
    serializer = ReplySerializer(replies, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def user_replies(request):
    """_api/replies/new_replies/ POST
    _api/replies/<int:pk>/  GET
    """
    if request.method == 'POST':
        serializer = ReplySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        replies = Reply.objects.filter(user_id=request.user.video_id)
        serializer = ReplySerializer(replies, many=True)
        return Response(serializer.data)
