from manager import QuizManager

class QuizGame:
    """전체 게임 진행 및 콘솔 메뉴 처리를 담당하는 클래스"""
    def __init__(self):
        self.manager = QuizManager()

    def run(self):
        """메인 실행 루프"""
        while True:
            print("\n" + "=" * 35)
            print("   🎮 객체지향 파이썬 콘솔 퀴즈 게임")
            print("=" * 35)
            print("1. 퀴즈 풀기")
            print("2. 퀴즈 추가하기")
            print("3. 퀴즈 목록 보기")
            print("4. 최고 점수 확인")
            print("5. 게임 종료")
            print("=" * 35)

            choice = input("원하는 메뉴 번호를 입력하세요: ").strip()

            if choice == "1":
                self.play_quiz()
            elif choice == "2":
                self.add_quiz_ui()
            elif choice == "3":
                self.show_quizzes()
            elif choice == "4":
                self.show_highest_score()
            elif choice == "5":
                print("\n👋 게임을 종료합니다. 이용해 주셔서 감사합니다!")
                break
            else:
                print("\n⚠️ 잘못된 번호입니다. 1~5번 중에서 선택해 주세요.")

    def play_quiz(self):
        if not self.manager.quizzes:
            print("\n⚠️ 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해주세요!")
            return

        print("\n🚀 퀴즈를 시작합니다!")
        current_score = 0

        for q in self.manager.quizzes:
            print("\n------------------------------")
            print(f"Q. {q.question}")
            for opt in q.options:
                print(f"   {opt}")

            user_ans = input("정답 번호를 입력하세요: ").strip()

            if user_ans == q.answer:
                print("✅ 정답입니다!")
                current_score += 10
            else:
                print(f"❌ 틀렸습니다. (정답: {q.answer}번)")

        print("\n🎉 모든 퀴즈가 끝났습니다!")
        total_possible = len(self.manager.quizzes) * 10
        print(f"당신의 최종 점수: {current_score}점 / {total_possible}점")

        if current_score > self.manager.highest_score:
            print("🏆 축하합니다! 최고 점수를 달성했습니다!")
            self.manager.save_score(current_score)

    def add_quiz_ui(self):
        print("\n➕ [새 퀴즈 추가]")
        question = input("문제 내용을 입력하세요: ").strip()
        
        options = []
        for i in range(1, 5):
            opt_text = input(f"선택지 {i}번 입력: ").strip()
            options.append(f"{i}) {opt_text}")
            
        answer = input("정답 번호(1~4)를 입력하세요: ").strip()

        self.manager.add_quiz(question, options, answer)
        print("✅ 새 퀴즈가 저장되었습니다!")

    def show_quizzes(self):
        quizzes = self.manager.quizzes
        print(f"\n📚 현재 총 {len(quizzes)}개의 퀴즈가 등록되어 있습니다.")
        for idx, q in enumerate(quizzes, start=1):
            print(f"{idx}. {q.question}")

    def show_highest_score(self):
        print(f"\n🏆 현재 최고 점수: {self.manager.highest_score}점")


if __name__ == "__main__":
    game = QuizGame()
    game.run()