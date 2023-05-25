from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import UserChatResult
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import openai
from django.contrib import messages
# Create your views here.
from django.utils import timezone

openai.api_key = ""

def signup(request):
    if request.method == "POST":
        if request.POST['password1'] == request.POST['password2']:
            user = User.objects.create_user(
                                            username=request.POST['username'],
                                            password=request.POST['password1'],
                                            email=request.POST['email'],)
            username = request.POST['username']
            raw_password = password=request.POST['password1']
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        return render(request, 'account/signup.html')
    return render(request, 'account/signup.html')


@login_required(login_url='account:login')
def chat_list(request):
    ans_list = UserChatResult.objects.filter(user=request.user)
    
    if len(ans_list) > 9:
        ans_list = ans_list[len(ans_list)-5:]
    elif len(ans_list) > 5:
        ans_list = ans_list[len(ans_list)-5:len(ans_list)]

    return render(request, 'account/answer_list.html', {'ans_list': ans_list})



#chatGPT에게 채팅 요청 API
def chatGPT(prompt):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    print(completion)
    result = completion.choices[0].message.content
    return result

@login_required(login_url='account:login')
def chat(request):
    #post로 받은 question
    if request.method == 'POST':
        ans = UserChatResult()
        prompt = request.POST.get('question')
        #type가 text면 chatGPT에게 채팅 요청 , type가 image면 imageGPT에게 채팅 요청
        result = chatGPT(prompt)
        ans.user = request.user
        ans.question = prompt
        ans.answer = result
        ans.pub_date = timezone.datetime.now()
        ans.save()

    return redirect('/accounts/answer')
