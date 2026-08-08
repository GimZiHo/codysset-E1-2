import json
import os
from models import Quiz

class QuizManager:
    """퀴즈 목록 관리 및 JSON 파일 입출력을 담당하는 클래스"""
    def __init__(self, state_filename="state.json"):
        self.state_filename = state_filename
        self.quizzes = []
        self.highest_score = 0
        
        # 프로그램 시작 시 데이터 불러오기
        self.load_state()

    def load_state(self):
        """state.json에서 퀴즈와 최고 점수를 불러오기"""
        if os.path.exists(self.state_filename):
            try:
                with open(self.state_filename, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.quizzes = [Quiz.from_dict(item) for item in data.get("quizzes", [])]
                self.highest_score = data.get("best_score", 0)
                return
            except Exception as e:
                print(f"⚠️ JSON 데이터 로드 실패(파일 손상 가능성): {e}")

        self.quizzes = []
        self.highest_score = 0

    def save_state(self):
        """현재 퀴즈와 최고 점수를 state.json에 저장"""
        data = {
            "quizzes": [q.to_dict() for q in self.quizzes],
            "best_score": self.highest_score
        }
        with open(self.state_filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def save_score(self, score):
        """새 최고 점수를 state.json에 저장"""
        self.highest_score = score
        self.save_state()

    def add_quiz(self, question, options, answer):
        """새 퀴즈 추가 후 JSON 저장"""
        new_quiz = Quiz(question, options, answer)
        self.quizzes.append(new_quiz)
        self.save_state()
