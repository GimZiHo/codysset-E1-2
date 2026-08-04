import json
import os
from models import Quiz

class QuizManager:
    """퀴즈 목록 관리 및 JSON 파일 입출력을 담당하는 클래스"""
    def __init__(self, quiz_filename="quizzes.json", score_filename="score.json"):
        self.quiz_filename = quiz_filename
        self.score_filename = score_filename
        self.quizzes = []
        self.highest_score = 0
        
        # 프로그램 시작 시 데이터 불러오기
        self.load_quizzes()
        self.load_score()

    def load_quizzes(self):
        """quizzes.json 파일에서 퀴즈 목록 불러오기"""
        if not os.path.exists(self.quiz_filename):
            # 파일이 없으면 기본 퀴즈 생성 후 저장
            self.quizzes = [
                Quiz("파이썬에서 화면에 문자를 출력하는 함수는?", ["1) input", "2) print", "3) len", "4) type"], "2"),
                Quiz("다음 중 참/거짓을 나타내는 자료형은?", ["1) Int", "2) String", "3) Boolean", "4) Float"], "3")
            ]
            self.save_quizzes()
        else:
            try:
                with open(self.quiz_filename, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.quizzes = [Quiz.from_dict(item) for item in data]
            except Exception as e:
                print(f"⚠️ 퀴즈 데이터 로드 실패: {e}")
                self.quizzes = []

    def save_quizzes(self):
        """현재 퀴즈 목록을 quizzes.json 파일로 저장"""
        with open(self.quiz_filename, "w", encoding="utf-8") as f:
            data = [q.to_dict() for q in self.quizzes]
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load_score(self):
        """score.json 파일에서 최고 점수 불러오기"""
        if os.path.exists(self.score_filename):
            try:
                with open(self.score_filename, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.highest_score = data.get("highest_score", 0)
            except Exception:
                self.highest_score = 0

    def save_score(self, score):
        """새 최고 점수를 score.json 파일로 저장"""
        self.highest_score = score
        with open(self.score_filename, "w", encoding="utf-8") as f:
            json.dump({"highest_score": self.highest_score}, f, ensure_ascii=False, indent=4)

    def add_quiz(self, question, options, answer):
        """새 퀴즈 추가 후 JSON 저장"""
        new_quiz = Quiz(question, options, answer)
        self.quizzes.append(new_quiz)
        self.save_quizzes()