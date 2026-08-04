class Quiz:
    """단일 퀴즈 문제를 나타내는 클래스"""
    def __init__(self, question, options, answer):
        self.question = question
        self.options = options
        self.answer = str(answer)

    def to_dict(self):
        """JSON 파일에 저장하기 위해 객체를 딕셔너리로 변환"""
        return {
            "question": self.question,
            "options": self.options,
            "answer": self.answer
        }

    @classmethod
    def from_dict(cls, data):
        """JSON 딕셔너리 데이터를 받아 Quiz 객체 생성"""
        return cls(data["question"], data["options"], data["answer"])