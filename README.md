# 2023년도 AI 개발 실무[AI0115-01] 기말고사

<img src="https://img.shields.io/badge/python-3776AB?style=flat&logo=python&logoColor=white"/>

## 레벤슈타인 거리를 기반으로 한 챗봇

<hr>

### * 레벤슈타인 거리 계산 함수

```python
def cal_levenshtein_distance(self, t1, t2):

    if t1 == t2:
        return 0

    t1_len = len(t1)
    t2_len = len(t2)

    if t1 == "": return t2_len
    if t2 == "": return t1_len

    _mat = [[] for i in range(t1_len + 1)]
    for i in range(t1_len + 1):
        _mat[i] = [0 for j in range(t2_len + 1)]
    for x in range(t1_len + 1):
        _mat[x][0] = x
    for y in range(t2_len + 1):
        _mat[0][y] = y

    for x in range(1, t1_len + 1):
        _t1_char = t1[x - 1]
        for y in range(1, t2_len + 1):
            _t2_char = t2[y - 1]
            _cost = 0 if (_t1_char == _t2_char) else 1
            _mat[x][y] = min(_mat[x - 1][y] + 1, _mat[x][y - 1] + 1, _mat[x - 1][y - 1] + _cost)

    return _mat[t1_len][t2_len]
        
```

<hr>

### * 레벤슈타인 거리 계산 함수를 이용하여 입력 텍스트(input_text)와 계산한 결과 중 최소값 반환 함수

```python
def get_levenshtein_answer(self, input_text):
    _cal_result = []
    for question_text in self.questions:
        _cost = self.cal_levenshtein_distance(input_text, question_text)
        _cal_result.append(_cost)
    # 가장 코스트가 낮은 값의 인덱스 구하기
    best_match_index = _cal_result.index(min(_cal_result))
    # 가장 유사한 질문에 해당하는 답변을 반환
    return self.answers[best_match_index]
```

<hr>

### * 챗봇 실행부에 적용

```python
while True:
    input_sentence = input('You: ')
    if input_sentence.lower() == '종료':
        break
    response = chatbot.get_levenshtein_answer(input_sentence)
    print('Chatbot:', response)
```
