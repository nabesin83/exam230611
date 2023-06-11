import pandas as pd 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 챗봇 클래스를 정의
class SimpleChatBot:
    # 챗봇 객체를 초기화하는 메서드, 초기화 시에는 입력된 데이터 파일을 로드하고, TfidfVectorizer를 사용해 질문 데이터를 벡터화함
    def __init__(self, filepath):
        self.questions, self.answers = self.load_data(filepath)
        self.vectorizer = TfidfVectorizer()
        self.question_vectors = self.vectorizer.fit_transform(self.questions)

    # CSV 파일로부터 질문과 답변 데이터를 불러오는 메서드
    def load_data(self, filepath):
        data = pd.read_csv(filepath)
        questions = data['Q'].tolist()
        answers = data['A'].tolist()
        return questions, answers

    # 입력 문장에 가장 잘 맞는 답변을 찾는 메서드, 입력 문장을 벡터화하고, 이를 기존 질문 벡터들과 비교하여 가장 높은 유사도를 가진 질문의 답변을 반환함
    def find_best_answer(self, input_sentence):
        # 사용자 입력 문장을 벡터화
        input_vector = self.vectorizer.transform([input_sentence])
        # 사용자 입력 벡터와 기존 질문 벡터들 간의 코사인 유사도를 계산
        similarities = cosine_similarity(input_vector, self.question_vectors)
        # 가장 유사도가 높은 질문의 인덱스를 찾음
        best_match_index = similarities.argmax()
        # 가장 유사한 질문에 해당하는 답변을 반환
        return self.answers[best_match_index]

    # 레벤슈타인 거리 계산 함수
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

    # 입력값에 대해 question 전체와 비교하여 최소의 레벤슈타인 cost를 반환하는 함수
    def get_levenshtein_answer(self, input_text):
        _cal_result = []
        for question_text in self.questions:
            _cost = self.cal_levenshtein_distance(input_text, question_text)
            _cal_result.append(_cost)
        # 가장 코스트가 낮은 값의 인덱스 구하기
        best_match_index = _cal_result.index(min(_cal_result))
        # 가장 유사한 질문에 해당하는 답변을 반환
        return self.answers[best_match_index]


# 데이터 파일의 경로를 지정합니다.
filepath = 'ChatbotData.csv'

# 챗봇 객체를 생성합니다.
chatbot = SimpleChatBot(filepath)

# '종료'라는 입력이 나올 때까지 사용자의 입력에 따라 챗봇의 응답을 출력하는 무한 루프를 실행합니다.
while True:
    input_sentence = input('You: ')
    if input_sentence.lower() == '종료':
        break
    response = chatbot.get_levenshtein_answer(input_sentence)
    print('Chatbot:', response)
