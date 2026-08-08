import json
import os
from models import Quiz


DEFAULT_QUIZ_DATA = [
    {
        "question": "파이썬에서 화면에 문자를 출력하는 함수는?",
        "choices": ["input", "print", "len", "type"],
        "answer": 2,
        "hint": "출력을 뜻하는 영어 단어입니다."
    },
    {
        "question": "다음 중 참/거짓을 나타내는 자료형은?",
        "choices": ["Int", "String", "Boolean", "Float"],
        "answer": 3,
        "hint": "True와 False 두 가지 값을 가집니다."
    },
    {
        "question": "한국의 수도는?",
        "choices": ["서울", "대전", "광주", "부산"],
        "answer": 1,
        "hint": "대한민국의 특별시입니다."
    },
    {
        "question": "지금 개발중인 프로그래밍 언어는?",
        "choices": ["Java", "C", "JS", "Python"],
        "answer": 4,
        "hint": "이 프로젝트 파일의 확장자는 .py입니다."
    },
    {
        "question": "내 근무지는?",
        "choices": ["강남", "마곡", "여의도", "판교"],
        "answer": 3,
        "hint": "국회의사당이 있는 지역입니다."
    }
]


class QuizManager:
    """퀴즈 목록 관리 및 JSON 파일 입출력을 담당하는 클래스"""
    def __init__(self, state_filename="state.json"):
        self.state_filename = state_filename
        self.quizzes = []
        self.highest_score = 0
        self.has_played = False
        
        # 프로그램 시작 시 데이터 불러오기
        self.load_state()

    def load_state(self):
        """state.json에서 퀴즈와 최고 점수를 불러오기"""
        try:
            if os.path.exists(self.state_filename):
                with open(self.state_filename, "r", encoding="utf-8") as f:
                    data = json.load(f)

                quiz_data = data["quizzes"]
                best_score = data["best_score"]
                has_played = data.get("has_played", best_score > 0)
                if not isinstance(quiz_data, list):
                    raise ValueError("quizzes는 리스트여야 합니다.")
                if not isinstance(best_score, int) or best_score < 0:
                    raise ValueError("best_score는 0 이상의 정수여야 합니다.")
                if not isinstance(has_played, bool):
                    raise ValueError("has_played는 참/거짓 값이어야 합니다.")

                self.quizzes = [Quiz.from_dict(item) for item in quiz_data]
                self.highest_score = best_score
                self.has_played = has_played
                return
        except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as e:
            print(f"⚠️ state.json을 불러오지 못했습니다: {e}")
            print("🛠️ 기본 퀴즈 데이터로 복구합니다.")
        else:
            print("📂 state.json이 없어 기본 퀴즈 데이터를 생성합니다.")

        self.quizzes = [Quiz.from_dict(item) for item in DEFAULT_QUIZ_DATA]
        self.highest_score = 0
        self.has_played = False
        self.save_state()

    def save_state(self):
        """현재 퀴즈와 최고 점수를 state.json에 저장"""
        data = {
            "quizzes": [q.to_dict() for q in self.quizzes],
            "best_score": self.highest_score,
            "has_played": self.has_played
        }
        try:
            with open(self.state_filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            return True
        except OSError as e:
            print(f"⚠️ state.json을 저장하지 못했습니다: {e}")
            return False

    def save_score(self, score):
        """새 최고 점수를 state.json에 저장"""
        self.highest_score = score
        self.has_played = True
        self.save_state()

    def add_quiz(self, question, choices, answer, hint):
        """새 퀴즈 추가 후 JSON 저장"""
        new_quiz = Quiz(question, choices, answer, hint)
        self.quizzes.append(new_quiz)
        self.save_state()

    def delete_quiz(self, quiz_index):
        """선택한 퀴즈를 삭제하고 JSON에 반영"""
        deleted_quiz = self.quizzes.pop(quiz_index)
        if self.save_state():
            return deleted_quiz

        self.quizzes.insert(quiz_index, deleted_quiz)
        return None
