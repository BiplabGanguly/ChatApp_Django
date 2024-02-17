from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.http import HttpResponse
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
import openai

openai.api_key = "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"

@api_view(['POST'])
def signin(req):
    if req.method == 'POST':
        email = req.data.get('email')
        username = req.data.get('username')
        password = req.data.get('password')

        if User.objects.filter(username=username).exists():
            data = {'status':100,'payload':'already signin'}
            return Response(data)
        
        else:
             User.objects.create_user(username=username, email=email, password=password)
             data = {'status':200, 'payload':'user is created'}
             return Response(data)
        

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            data = {'status': 200, 'payload': True, 'username': user.username, 'token': token.key}
            return Response(data)
        else:
            data = {'status': 200, 'payload': False}
            return Response(data)
        


@api_view(['POST'])
def chat_view(req):
    if req.method == "POST":
        user_input = req.data.get('user_input') 

        if user_input:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": user_input},
                ]
            )
            data = completion['choices'][0]['message']['content'].strip()
            return Response(data)

    
        
