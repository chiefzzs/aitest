import requests

response = requests.post(
     "http://localhost:11434/api/chat",
    json={
        "model": "qwen2.5",
        "messages": [{"role": "user", "content": "你好"}]
    }
)
print(response.text)  
