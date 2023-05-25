from django.shortcuts import render
import openai
# 추가된거
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.models import UserChatResult
from django.utils import timezone

openai.api_key = ""

def chatGPT(prompt):
    completion = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo',
        messages = [{'role' : 'user', 'content' : prompt}]
    )
    print(completion)
    result = completion.choices[0].message.content
    return result

def imageGPT(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="256x256"
    )
    result = response['data'][0]['url']
    return result

def index(request):
    return render(request, 'selfgpt/index.html')

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
        
        context = {
            'question': prompt,
            'result': result
        }

    return render(request, 'selfgpt/result.html', context) 

