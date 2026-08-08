from manager import QuizManager

class QuizGame:
    """전체 게임 진행 및 콘솔 메뉴 처리를 담당하는 클래스"""
    def __init__(self):
        self.manager = QuizManager()

    def run(self):
        """입력 중단 예외를 처리하며 게임 실행"""
        try:
            self.run_menu()
        except (KeyboardInterrupt, EOFError):
            print("\n\n⚠️ 입력이 중단되어 게임을 종료합니다.")
            if self.manager.save_state():
                print("💾 현재 상태를 안전하게 저장했습니다.")
            print("👋 이용해 주셔서 감사합니다!")

    def run_menu(self):
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

            choice = self.get_number(
                "원하는 메뉴 번호를 입력하세요 (1-5): ", 1, 5
            )

            if choice == 1:
                self.play_quiz()
            elif choice == 2:
                self.add_quiz_ui()
            elif choice == 3:
                self.show_quizzes()
            elif choice == 4:
                self.show_highest_score()
            elif choice == 5:
                print("\n👋 게임을 종료합니다. 이용해 주셔서 감사합니다!")
                break

    def get_number(self, prompt, minimum, maximum):
        """공통 숫자 입력 및 범위 검증"""
        while True:
            raw_value = input(prompt).strip()
            if not raw_value:
                print("⚠️ 값을 입력해 주세요.")
                continue

            try:
                value = int(raw_value)
            except ValueError:
                print("⚠️ 숫자로 입력해 주세요.")
                continue

            if minimum <= value <= maximum:
                return value

            print(f"⚠️ {minimum}부터 {maximum} 사이의 숫자를 입력해 주세요.")

    def play_quiz(self):
        if not self.manager.quizzes:
            print("\n⚠️ 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해주세요!")
            return

        quiz_count = self.get_number(
            f"몇 문제를 풀지 입력하세요 (1-{len(self.manager.quizzes)}): ",
            1,
            len(self.manager.quizzes)
        )
        selected_quizzes = self.manager.quizzes[:quiz_count]

        print(f"\n🚀 퀴즈를 시작합니다! (총 {quiz_count}문제)")
        earned_score = 0
        hint_penalty = 0

        for q in selected_quizzes:
            print("\n------------------------------")
            q.display()

            hint_used = False

            # 0을 입력하면 힌트를 보여주고, 1~4 정답을 입력받기
            while True:
                user_ans = self.get_number(
                    "정답 번호(1-4), 힌트는 0: ", 0, len(q.choices)
                )
                if user_ans == 0:
                    if hint_used:
                        print("⚠️ 힌트는 한 번만 사용할 수 있습니다.")
                    elif q.hint:
                        hint_used = True
                        hint_penalty += 10
                        print(f"💡 힌트: {q.hint} (-10점)")
                    else:
                        print("⚠️ 이 문제에는 힌트가 없습니다.")
                    continue
                break

            # 정답 검증
            if q.check_answer(user_ans):
                earned_score += 20
                print("✅ 정답입니다! (+20점)")
            else:
                print(f"❌ 틀렸습니다. (정답: {q.answer}번)")

        print("\n🎉 모든 퀴즈가 끝났습니다!")
        total_possible = quiz_count * 20
        final_score = max(0, earned_score - hint_penalty)
        penalty_text = f"-{hint_penalty}점" if hint_penalty else "0점"
        print(f"획득 점수: {earned_score}점")
        print(f"힌트 감점: {penalty_text}")
        print(f"당신의 최종 점수: {final_score}점 / {total_possible}점")

        if not self.manager.has_played:
            self.manager.save_score(final_score)
            print("📝 첫 점수가 기록되었습니다.")
        elif final_score > self.manager.highest_score:
            print("🏆 축하합니다! 최고 점수를 달성했습니다!")
            self.manager.save_score(final_score)

    def add_quiz_ui(self):
        print("\n➕ [새 퀴즈 추가]")
        
        # 빈 문자열 입력 방지
        while True:
            question = input("문제 내용을 입력하세요: ").strip()
            if question:
                break
            print("⚠️ 문제 내용은 비워둘 수 없습니다.")
        
        choices = []
        for i in range(1, 5):
            while True:
                opt_text = input(f"선택지 {i}번 입력: ").strip()
                if opt_text:
                    choices.append(opt_text)
                    break
                print("⚠️ 선택지 내용은 비워둘 수 없습니다.")
            
        answer = self.get_number("정답 번호(1~4)를 입력하세요: ", 1, 4)

        while True:
            hint = input("힌트를 입력하세요: ").strip()
            if hint:
                break
            print("⚠️ 힌트 내용은 비워둘 수 없습니다.")

        self.manager.add_quiz(question, choices, answer, hint)
        print("✅ 새 퀴즈가 안전하게 저장되었습니다!")

    def show_quizzes(self):
        quizzes = self.manager.quizzes
        print(f"\n📚 현재 총 {len(quizzes)}개의 퀴즈가 등록되어 있습니다.")
        for idx, q in enumerate(quizzes, start=1):
            print(f"{idx}. {q.question}")

    def show_highest_score(self):
        if not self.manager.has_played:
            print("\n🏆 아직 기록된 점수가 없습니다.")
        else:
            print(f"\n🏆 현재 최고 점수: {self.manager.highest_score}점")


if __name__ == "__main__":
    game = QuizGame()
    game.run()
