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

            # 예외 처리: 메뉴 선택 시 숫자 및 범위 검증
            try:
                choice = int(input("원하는 메뉴 번호를 입력하세요 (1-5): ").strip())
            except ValueError:
                print("\n⚠️ 문자가 아닌 [숫자]만 입력해 주세요!")
                continue  # 메뉴를 다시 출력하도록 맨 위로 이동

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
            else:
                print("\n⚠️ 1~5번 사이의 번호를 입력해 주세요.")

    def play_quiz(self):
        if not self.manager.quizzes:
            print("\n⚠️ 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해주세요!")
            return

        print("\n🚀 퀴즈를 시작합니다!")
        current_score = 0

        for q in self.manager.quizzes:
            print("\n------------------------------")
            print(f"Q. {q.question}")
            for number, choice in enumerate(q.choices, start=1):
                print(f"   {number}) {choice}")

            hint_used = False

            # 0을 입력하면 힌트를 보여주고, 1~4 정답을 입력받기
            while True:
                try:
                    user_ans = int(input("정답 번호(1-4), 힌트는 0: ").strip())
                    if user_ans == 0:
                        if hint_used:
                            print("⚠️ 힌트는 한 번만 사용할 수 있습니다.")
                        elif q.hint:
                            hint_used = True
                            print(f"💡 힌트: {q.hint}")
                        else:
                            print("⚠️ 이 문제에는 힌트가 없습니다.")
                        continue
                    if 1 <= user_ans <= len(q.choices):
                        break
                    else:
                        print(f"⚠️ 1번부터 {len(q.choices)}번 사이의 번호를 선택해 주세요.")
                except ValueError:
                    print("⚠️ 숫자로 입력해 주세요!")

            # 정답 검증
            if user_ans == q.answer:
                earned_score = 10 if hint_used else 20
                current_score += earned_score
                print(f"✅ 정답입니다! (+{earned_score}점)")
            else:
                print(f"❌ 틀렸습니다. (정답: {q.answer}번)")

        print("\n🎉 모든 퀴즈가 끝났습니다!")
        total_possible = len(self.manager.quizzes) * 20
        print(f"당신의 최종 점수: {current_score}점 / {total_possible}점")

        if current_score > self.manager.highest_score:
            print("🏆 축하합니다! 최고 점수를 달성했습니다!")
            self.manager.save_score(current_score)

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
            
        # 정답 번호 예외 처리
        while True:
            try:
                answer = int(input("정답 번호(1~4)를 입력하세요: ").strip())
                if 1 <= answer <= 4:
                    break
                else:
                    print("⚠️ 1번에서 4번 사이의 번호를 입력해 주세요.")
            except ValueError:
                print("⚠️ 숫자로 정답 번호를 입력해 주세요.")

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
        print(f"\n🏆 현재 최고 점수: {self.manager.highest_score}점")


if __name__ == "__main__":
    game = QuizGame()
    game.run()
