import os
from openai import OpenAI
from dataclasses import dataclass
import pytz
from datetime import datetime, timedelta
import tiktoken

@dataclass(frozen=True) # 초기화 메서드 생략, 데이터 변경 불가
class Model: 
    basic: str = "gpt-4o-mini"
    advanced: str = "gpt-4o"
    
model = Model();    
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), timeout=30, max_retries=1) # 타임 아웃 30초, 오류 최대 재시도 횟수 1회

    
# 토큰 수 산출 함수
def gpt_num_tokens(messages, model="gpt-4o"):
    encoding = tiktoken.encoding_for_model(model)
    tokens_per_message = 3 # 참고, 모든 메시지는 다음 형식을 따른다: <|start|>{role/name}\n{content}<|end|>\n   
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message #
        for _, value in message.items():
            num_tokens += len(encoding.encode(value))
    num_tokens += 3  # 참고, 모든 메시지는 다음 형식으로 assistant의 응답을 준비한다: <|start|>assistant<|message|>
    return num_tokens

# 예외 처리
def makeup_response(message, finish_reason="ERROR"):
    return {
        "choices": [
            {
                "finish_reason": finish_reason,
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": message
                }                   
            }
        ],
        "usage": {"total_tokens": 0},
    }
    
def today():
    korea = pytz.timezone('Asia/Seoul')
    now = datetime.now(korea)
    return(now.strftime("%Y%m%d"))

def yesterday():    
    korea = pytz.timezone('Asia/Seoul')
    now = datetime.now(korea)
    one_day = timedelta(days=1)
    yesterday = now - one_day 
    return yesterday.strftime('%Y%m%d') 

def currTime():
    korea = pytz.timezone('Asia/Seoul')
    now = datetime.now(korea)
    formatted_now = now.strftime("%Y.%m.%d %H:%M:%S")
    return(formatted_now)
