import os
import sys
import time
import threading
import subprocess
import numpy as np

start_time = time.time() #시작시간 체크

#실행파일 위치
exePath = ".\dist\exefile.exe" #C:/Users/woojh/Desktop/exetest

#파라미터 정의
min_para = 0.6 # 최소값
max_para = 1.5 # 최대값
step = 0.1 # 어느정도 단위로 탐색할 것인지
amount = 2 # 전체 파라미터 개수

result_min = {} #가장 작은 결과를 저장하는 변수


thread_limit = 5 #동시에 동작하는 최대 스레드의 개수 지정
cur_thread = 0 #현재 스레드 개수
th_num_count = 1 # 스레드 번호

# exe파일 실행 함수
def run_exe(exe_list_paras, th_num):
    global cur_thread
    global result_min
    global result_min_para

    cur_thread += 1 #현재 스레드 수 증가
    str_para = list(map(str, exe_list_paras))
    str_para.insert(0, exePath)
    aResult = subprocess.check_output(str_para, shell=True, encoding='utf-8')
    aResult = float(aResult)

    #진행과정 출력 (스레드 번호, 현재 스레드 개수, 파라미터값, 함수실행 결과)
    print('[', th_num, cur_thread,']', str_para[1:], '-->', aResult)

    result_min[aResult] = str_para[1:]

    cur_thread -= 1 #현재 스레드 수 감소

# 파라미터를 step 만큼 증가시키는 함수
def increase(list_paras, index):
    para = list_paras[index] + step
    para = round(para, 1)
    if para > max_para:
        list_paras[index] = min_para
        increase_index = index - 1
        if increase_index < 0: # index가 맨 앞자리를 넘어가면 종료
            return 0
        else:
            return increase(list_paras, increase_index)
    else:
        list_paras[index] = para
        return list_paras
    

if __name__ == "__main__":
    #amout의 길이만큼 min_para로 파라미터 초기화
    # ex) [0.6, 0.6, 0.6, ~ , 0.6]
    parameter_list = list(np.full(amount, min_para))
    
    while(True):
        if parameter_list == 0:
            break
        else:
            if cur_thread < thread_limit: #스레드를 thread_limit만큼 제한
                t = threading.Thread(target=run_exe, 
                                    args=(parameter_list, th_num_count))
                t.start()
                th_num_count += 1
                parameter_list = increase(parameter_list, amount - 1)

    while (True): 
        if cur_thread <= 0:
            break
        else:
            time.sleep(0.1)
    take_time = time.time() - start_time

    temp = result_min.keys()
    min_value = min(temp)
    
    print('가장 작은 결과 : ', min_value)
    print('그 때에 파라미터 값 : ', result_min[min_value])
    print('실행시간(초): ', take_time % 60)
        