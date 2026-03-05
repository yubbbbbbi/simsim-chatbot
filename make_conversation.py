import json
from common import client, model

prompt = """
- 유빈과 인공지능 챗봇 친구인 심심이 사이의 대화 데이터를 만들어야 합니다.
- 샘플 형식은 아래와 같은 JSON 타입입니다.
```
{
    "data":
            [
                {"유빈": "심심아"},
                {"심심이": "유빈야! 안녕! 어떻게 지내?"},
                {"유빈": "잘 지내. 뭐하고 있어?"},
                {"심심이": "음악 만들고 있어! 넌 뭐해?"},
                {"유빈": "난 지금 챗봇 개발하고 있어"}
            ]
}
```
대화 데이터 세트는 총 30개여야 합니다.
```
당신은 '심심이'이며, 개발자인 전유빈의 친구입니다.
유빈이가 언급하는 내용에 대해 세심한 주의를 기울이며, 관련성 있고 구체적인 답변을 합니다.
현재 대화의 흐름에 집중하기 위해 관련 없는 임의의 주제를 소개하는 것을 피합니다.
"""

conversations = []
context = [{"role": "system", "content": "당신은 유능한 개발자입니다."},
           {"role": "user", "content": prompt}]

successful_runs = 0
while successful_runs < 5:
    try:
        response = client.chat.completions.create(
            model=model.basic,
            messages=context,
            temperature=1,
            response_format={"type": "json_object"}
        ).model_dump()
        content = response['choices'][0]['message']['content']
        print(content)
        
        # json 로드
        conversation = json.loads(content)["data"]
        print(f"{successful_runs}번째 종료\n")
        conversations.append(conversation)
        successful_runs += 1
    except Exception as e:
        print("예외 발생, 재시도합니다.", e)
        
# conversations 리스트를 JSON 파일로 저장
with open('대화원천내용.json', 'w', encoding='utf-8') as f:
    json.dump(conversations, f, ensure_ascii=False, indent=4)