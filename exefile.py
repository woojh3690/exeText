import sys
import random

if __name__ == "__main__":
    para = sys.argv #파라미터 받은값

    #임시 return 값으로 무작위 수를 생성
    random_number = random.random()
    print(random_number, end='')
    sys.exit(0)