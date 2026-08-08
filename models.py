class Quiz:
    """단일 퀴즈 문제를 나타내는 클래스"""
    def __init__(self, question, choices, answer, hint=""):
        self.question = question
        self.choices = choices
        self.answer = int(answer)
        self.hint = hint

    def to_dict(self):
        """JSON 파일에 저장하기 위해 객체를 딕셔너리로 변환"""
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
            "hint": self.hint
        }

    @classmethod
    def from_dict(cls, data):
        """JSON 딕셔너리 데이터를 받아 Quiz 객체 생성"""
        return cls(
            data["question"],
            data["choices"],
            data["answer"],
            data.get("hint", "")
        )
