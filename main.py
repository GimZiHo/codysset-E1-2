while True:
    print("\n--- 퀴즈 게임 메뉴 ---")
    print("1. 퀴즈 풀기")
    print("2. 종료하기")
    
    choice = input("선택하세요: ")
    
    if choice == "1":
        print("퀴즈를 시작합니다!")
    elif choice == "2":
        print("게임을 종료합니다. 안녕히 가세요!")
        break  # while 반복문을 종료함
    else:
        print("잘못 입력하셨습니다. 다시 선택해주세요.")