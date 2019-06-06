from vpython import *
import random

thick = int(input("초기 공기층의 두께는 얼마인가요?"))

layer_num = int(input("층을 몇 개 입력하실 건가요?"))

data = [[1, thick]]

for i in range(layer_num):
    data.append(list(map(int, input(str(i+1)+"번째 층의 굴절률과 두께를 차례대로 입력해주세요.").split())))
    thick +=data[-1][1]


scene = canvas()

back = box(pos = vector(0,0,0), size = vector(100, thick, 5), color = vector(1,1,1))

temp_height = 0

for layer in range(len(data)):
    a = box(pos = vector(0, thick/2 - temp_height - data[layer][1]/2, 5), size = vector(100, data[layer][1], 5), color = vector(random.random(), random.random(), random.random()))
    temp_height += data[layer][1]
