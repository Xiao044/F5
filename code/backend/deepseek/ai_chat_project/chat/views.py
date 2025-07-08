import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


DEEPSEEK_API_KEY = "sk-66b880349a554e48a001825d425410ac"

@csrf_exempt
def chat_with_deepseek(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_input = data.get("message", "").strip()

            if not user_input:
                return JsonResponse({"reply": "请输入有效的消息"}, status=400)

            # DeepSeek API 请求
            url = "https://api.deepseek.com/v1/chat/completions"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
            }
            payload = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": "你是一个善于时间管理和任务规划的助手，请根据用户请求进行清晰回复。"},
                    {"role": "user", "content": user_input}
                ]
            }

            response = requests.post(url, headers=headers, json=payload, timeout=15)
            response.raise_for_status()
            reply = response.json()['choices'][0]['message']['content']
            return JsonResponse({"reply": reply})

        except requests.exceptions.RequestException as e:
            return JsonResponse({"reply": f"请求失败：{str(e)}"}, status=500)
        except Exception as e:
            return JsonResponse({"reply": f"处理出错：{str(e)}"}, status=500)

    return JsonResponse({"reply": "仅支持 POST 请求"}, status=405)

@csrf_exempt
def chat_with_deepseek(request):
    print("🔵 收到请求：", request.method)
