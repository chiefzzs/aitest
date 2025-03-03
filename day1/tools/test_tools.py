# 步骤4:发起 function calling
# 请将以下代码粘贴到步骤3 代码后

from openai import OpenAI
import os
from tools import *
from tools_config import *

# 步骤3:创建messages数组
# 请将以下代码粘贴到步骤2 代码后
messages = [
    {
        "role": "system",
        "content": """你是一个很有帮助的助手。如果用户提问关于天气的问题，请调用 ‘get_current_weather’ 函数;
     如果用户提问关于时间的问题，请调用‘get_current_time’函数。
     请以友好的语气回答问题。""",
    },
    {
        "role": "user",
        "content": "上海天气"
    }
]
print("messages 数组创建完成\n")


modelname = "Qwen/Qwen2.5-72B-Instruct"
modelname = "qwen2.5"

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    base_url='http://localhost:11434/v1/',
    api_key='unset', # Model
   
)

def function_calling():
    completion = client.chat.completions.create(
        model=modelname,  # 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        messages=messages,
        tools=tools
    )
    print("返回对象：")
    print(completion.choices[0].message.model_dump_json())
    print("\n")
    return completion

print("正在发起function calling...")
completion = function_calling()

# 步骤5:运行工具函数
# 请将以下代码粘贴到步骤4 代码后
import json

print("正在执行工具函数...")
# 从返回的结果中获取函数名称和入参
function_name = completion.choices[0].message.tool_calls[0].function.name
arguments_string = completion.choices[0].message.tool_calls[0].function.arguments

# 使用json模块解析参数字符串
arguments = json.loads(arguments_string)
# 创建一个函数映射表
function_mapper = {
    "get_current_weather": get_current_weather,
    "get_current_time": get_current_time
}
# 获取函数实体
function = function_mapper[function_name]
# 如果入参为空，则直接调用函数
if arguments == {}:
    function_output = function()
# 否则，传入参数后调用函数
else:
    function_output = function(arguments)
# 打印工具的输出
print(f"工具函数输出：{function_output}\n")


