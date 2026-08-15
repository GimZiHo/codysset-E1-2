class Quiz:
    """단일 퀴즈 문제를 나타내는 클래스"""
    def __init__(self, question, choices, answer, hint=""):
        if not isinstance(question, str) or not question.strip():
            raise ValueError("문제 내용은 빈 문자열일 수 없습니다.")
        if not isinstance(choices, list) or len(choices) != 4:
            raise ValueError("선택지는 4개여야 합니다.")
        if any(not isinstance(choice, str) or not choice.strip() for choice in choices):
            raise ValueError("선택지 내용은 빈 문자열일 수 없습니다.")
        if isinstance(answer, bool) or not isinstance(answer, int) or not 1 <= answer <= 4:
            raise ValueError("정답은 1부터 4 사이의 정수여야 합니다.")
        if not isinstance(hint, str):
            raise ValueError("힌트는 문자열이어야 합니다.")

        self.question = question.strip()
        self.choices = [choice.strip() for choice in choices]
        self.answer = answer
        self.hint = hint.strip()

    def display(self):
        """문제와 선택지 출력"""
        print(f"Q. {self.question}")
        for number, choice in enumerate(self.choices, start=1):
            print(f"   {number}) {choice}")

    def check_answer(self, user_answer):
        """사용자 정답 확인"""
        return user_answer == self.answer

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
