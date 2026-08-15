import json
import os
from datetime import datetime

from quiz.quiz import Quiz


DEFAULT_QUIZ_DATA = [
    {
        "question": "세상에서 가장 큰 동물은?",
        "choices": ["코끼리", "대왕고래", "기린", "하마"],
        "answer": 2,
        "hint": "바다에 사는 아주 큰 포유류입니다."
    },
    {
        "question": "다음 중 날지 못하는 새는?",
        "choices": ["참새", "독수리", "펭귄", "까치"],
        "answer": 3,
        "hint": "추운 남극에서 자주 볼 수 있습니다."
    },
    {
        "question": "판다가 주로 먹는 음식은?",
        "choices": ["대나무", "사과", "물고기", "고기"],
        "answer": 1,
        "hint": "길고 푸른 식물입니다."
    },
    {
        "question": "캥거루가 새끼를 키우는 곳은?",
        "choices": ["등 위", "배의 주머니", "꼬리 위", "땅속"],
        "answer": 2,
        "hint": "어미의 배 쪽에 있습니다."
    },
    {
        "question": "다음 중 바다에 사는 동물은?",
        "choices": ["호랑이", "토끼", "돌고래", "기린"],
        "answer": 3,
        "hint": "똑똑한 해양 포유류로 유명합니다."
    }
]


class QuizManager:
    """퀴즈 목록 관리 및 JSON 파일 입출력을 담당하는 클래스"""
    def __init__(self, state_filename="../data/state.json"):
        self.state_filename = state_filename
        self.quizzes = []
        self.highest_score = 0
        self.has_played = False
        self.score_history = []
        
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
                score_history = data.get("score_history", [])
                if not isinstance(quiz_data, list):
                    raise ValueError("quizzes는 리스트여야 합니다.")
                if not isinstance(best_score, int) or best_score < 0:
                    raise ValueError("best_score는 0 이상의 정수여야 합니다.")
                if not isinstance(has_played, bool):
                    raise ValueError("has_played는 참/거짓 값이어야 합니다.")
                if not isinstance(score_history, list):
                    raise ValueError("score_history는 리스트여야 합니다.")
                for record in score_history:
                    if not isinstance(record, dict):
                        raise ValueError("점수 기록은 객체 형식이어야 합니다.")
                    if not isinstance(record.get("played_at"), str):
                        raise ValueError("점수 기록의 날짜가 잘못되었습니다.")
                    if not isinstance(record.get("quiz_count"), int):
                        raise ValueError("점수 기록의 문제 수가 잘못되었습니다.")
                    if not isinstance(record.get("score"), int):
                        raise ValueError("점수 기록의 점수가 잘못되었습니다.")
                    if not isinstance(record.get("max_score"), int):
                        raise ValueError("점수 기록의 만점이 잘못되었습니다.")

                self.quizzes = [Quiz.from_dict(item) for item in quiz_data]
                self.highest_score = best_score
                self.has_played = has_played
                self.score_history = score_history
                return
        except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as e:
            print(f"⚠️ state.json을 불러오지 못했습니다: {e}")
            print("🛠️ 기본 퀴즈 데이터로 복구합니다.")
        else:
            print("📂 state.json이 없어 기본 퀴즈 데이터를 생성합니다.")

        self.quizzes = [Quiz.from_dict(item) for item in DEFAULT_QUIZ_DATA]
        self.highest_score = 0
        self.has_played = False
        self.score_history = []
        self.save_state()

    def save_state(self):
        """현재 퀴즈와 최고 점수를 state.json에 저장"""
        data = {
            "quizzes": [q.to_dict() for q in self.quizzes],
            "best_score": self.highest_score,
            "has_played": self.has_played,
            "score_history": self.score_history
        }
        try:
            with open(self.state_filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            return True
        except OSError as e:
            print(f"⚠️ state.json을 저장하지 못했습니다: {e}")
            return False

    def record_game(self, score, quiz_count, max_score):
        """게임 결과를 기록하고 최고 점수 갱신"""
        previous_highest_score = self.highest_score
        previous_has_played = self.has_played
        is_new_highest = not self.has_played or score > self.highest_score

        self.score_history.append({
            "played_at": datetime.now().astimezone().isoformat(timespec="seconds"),
            "quiz_count": quiz_count,
            "score": score,
            "max_score": max_score
        })
        if is_new_highest:
            self.highest_score = score
        self.has_played = True

        if self.save_state():
            return is_new_highest

        self.score_history.pop()
        self.highest_score = previous_highest_score
        self.has_played = previous_has_played
        return None

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
