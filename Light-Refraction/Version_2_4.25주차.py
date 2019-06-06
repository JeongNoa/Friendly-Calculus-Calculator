from vpython import *
import random
import math

length = int(input("각 층의 가로 길이는 얼마인가요?"))

thick = int(input("초기 공기층의 두께는 얼마인가요?"))

layer_num = int(input("층을 몇 개 입력하실 건가요?"))

data = [[1, thick]]

color_layer = {1 : vector(1,1,1)}

for i in range(layer_num):
    data.append(list(map(int, input(str(i+1)+"번째 층의 굴절률과 두께를 차례대로 입력해주세요.").split())))
    thick += data[-1][1]
    if data[-1][0] not in color_layer.keys():
        color_layer[data[-1][0]] = vector(random.random(), random.random(), random.random())

ang = int(input("빛의 첫 입사각은 몇 도인가요?")) * math.pi / 180

speed = int(input("대략 몇 초 안에 실행시키고 싶으신가요?"))


def angle_ref(st_ang, st_vel, n1, n2):
    if n1 * math.sin(st_ang) / n2 >= 1:   #전반사
        fi_vel = vector(st_vel.x, st_vel.y * (-1), 0)
        fi_ang = st_ang
        return fi_vel, fi_ang
    fi_ang = math.asin(n1 * math.sin(st_ang) / n2)
    fi_vel_mag = n1 * st_vel.mag / n2
    fi_vel = vector(fi_vel_mag * math.sin(fi_ang), (-1) * fi_vel_mag * math.cos(fi_ang), 0)
    return fi_vel, fi_ang

c = 10

vel = vector(c * math.sin(ang), (-1) * c * math.cos(ang), 0)

border_pos = []
border_temp = 0
for i in range(len(data)-1):
    border_pos.append(thick/2 - border_temp - data[i][1])
    border_temp += data[i][1]
    
scene = canvas()

vel2 = vel
ang2 = ang

data_box = []

back = box(pos = vector(0,0,0), size = vector(length, thick, 5), color = vector(1,1,1))

temp_height = 0

for layer in range(len(data)):
    a = box(pos = vector(0, thick/2 - temp_height - data[layer][1]/2, 5), size = vector(100, data[layer][1], 5), 
            opacity = 0.3, color = color_layer[data[layer][0]])
    temp_height += data[layer][1]
    
light = sphere(pos = vector((-1) * length/2, thick /2, 5), size = vector(1,1,1), color = vector(1,1,0), make_trail=True)

dt = 1/200
float_value_adj = None
while light.pos.y < thick/2 + 1 and light.pos.y > thick/2 * (-1) - 1 and light.pos.x < length / 2 + 1 and \
        light.pos.x > 0 - length / 2 - 1:
    rate(200)
    light.pos += vel2 * dt
    temp = 0
    for i in border_pos:
        if light.pos.y < i + 0.1 and light.pos.y > i - 0.1:
            temp = i
            break
    if temp and float_value_adj != temp:
        print(border_pos.index(temp))
        vel2, ang2 = angle_ref(ang2, vel2, data[border_pos.index(temp)][0], data[border_pos.index(temp)+1][0])
        float_value_adj = temp
