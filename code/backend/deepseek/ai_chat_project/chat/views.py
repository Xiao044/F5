import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def chat_with_deepseek(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_input = data.get("message", "")
            if not user_input:
                return JsonResponse({"reply": "消息不能为空"}, status=400)

            url = "https://api.deepseek.com/v1/chat/completions"
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer YOUR_API_KEY"  # 替换为你的DeepSeek API Key
            }
            payload = {
                "model": "deepseek-chat",
                "messages": [{"role": "user", "content": user_input}]
            }

            response = requests.post(url, headers=headers, json=payload, timeout=15)
            reply = response.json()['choices'][0]['message']['content']
            return JsonResponse({"reply": reply})
        except Exception as e:
            return JsonResponse({"reply": f"出错：{str(e)}"}, status=500)

    return JsonResponse({"reply": "只支持 POST 请求"}, status=405)
