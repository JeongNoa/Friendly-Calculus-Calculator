from vpython import *
import random
import math


class refract:
    
    def angle_ref(self, st_ang, st_vel, n1, n2):
        if n1 * math.sin(st_ang) / n2 >= 1:   #전반사
            fi_vel = vector(st_vel.x, st_vel.y * (-1), 0)
            fi_ang = st_ang
            return fi_vel, fi_ang
        
        fi_ang = math.asin(n1 * math.sin(st_ang) / n2)
        fi_vel_mag = n1 * st_vel.mag / n2
        fi_vel = vector(fi_vel_mag * math.sin(fi_ang), (-1) * fi_vel_mag * math.cos(fi_ang), 0)
        return fi_vel, fi_ang
    
    
    def time_ref(self, st_ang, st_vel, n1, n2):
        if n1 * math.sin(st_ang) / n2 >= 1:   #전반사
            return st_ang, -1
        return math.asin(n1 * math.sin(st_ang) / n2), 1
    
    
    def border(self):
        border_pos = []
        border_temp = 0
        for i in range(len(self.data)-1):
            border_pos.append(self.thick/2 - border_temp - self.data[i][1])
            border_temp += self.data[i][1]
        
        return border_pos
            
    
    def speed_check(self, speed):
        time_check = 0
        timer = 0
        xpos = 0
        ang = self.ang
        direc = 1
        while time_check >= 0 and time_check < len(self.data):
            timer += self.data[time_check][1] * self.data[time_check][0] / math.cos(ang)
            xpos += math.tan(ang) * self.data[time_check][1]
            if time_check == len(self.data) - 1:
                break
            ang, direc = self.time_ref(ang, vector(0,0,0), self.data[time_check][0], self.data[time_check + direc][0])
            time_check += int((direc + 1) // 2)

            if xpos > self.length - math.tan(ang) * self.data[time_check][1]:
                timer += (self.length - xpos) * self.data[time_check][0] / math.sin(ang)
                break

        c = timer / speed

        return vector(c * math.sin(self.ang), (-1) * c * math.cos(self.ang), 0)
    
    
    def base(self, color_layer):
        scene = canvas()

        back = box(pos = vector(0,0,0), size = vector(self.length, self.thick, 5), color = vector(1,1,1))

        temp_height = 0
        for layer in range(len(self.data)):
            a = box(pos = vector(0, self.thick/2 - temp_height - self.data[layer][1]/2, 5), 
                    size = vector(self.length, self.data[layer][1], 5), opacity = 0.3, color = color_layer[self.data[layer][0]])
            temp_height += self.data[layer][1]

        self.light = sphere(pos = vector((-1) * self.length/2, self.thick /2, 5), 
                    size = vector(1,1,1), color = vector(1,1,0), make_trail=True)
        
        
    def move(self, vel, border_pos):
        vel /= self.data[0][0]
        ang = self.ang
        
        dt = 1/200
        float_value_adj = None
        while self.light.pos.y < self.thick/2 + 1 and self.light.pos.y > self.thick/2 * (-1) - 1 and \
            self.light.pos.x < self.length / 2 + 1 and self.light.pos.x > 0 - self.length / 2 - 1:
            
            rate(200)
            self.light.pos += vel * dt
            temp = 'None'
            
            for i in border_pos:
                if self.light.pos.y < i + 0.1 and self.light.pos.y > i - 0.1:
                    temp = i
                    break
                    
            if temp != 'None' and float_value_adj != temp:
                vel, ang = self.angle_ref(ang, vel, self.data[border_pos.index(temp)][0], self.data[border_pos.index(temp)+1][0])
                float_value_adj = temp
    
    
    def activate(self):
        self.length = float(input("각 층의 가로 길이는 얼마인가요? 100 이상의 값을 입력해주세요."))
        
        layer_num = int(input("층을 몇 개 입력하실 건가요?"))
        
        self.data = []   #각 층의[굴절률, 두께]가 들어가 있는 리스트.
        
        color_layer = {1 : vector(1,1,1)}   #각 층의 색깔에 대한 데이터가 들어가 있는 리스트. 같은 굴절률의 데이터는 같은 색이다.

        self.thick = 0
        for i in range(layer_num):
    
            self.data.append(list(map(float, input(str(i+1)+"번째 층의 굴절률과 두께를 차례대로 입력해주세요.").split())))
            self.thick += self.data[-1][1]
            
            if self.data[-1][0] not in color_layer.keys():
                color_layer[self.data[-1][0]] = vector(random.random(), random.random(), random.random())
                
        self.ang = float(input("빛의 첫 입사각은 몇 도인가요?")) * math.pi / 180

        speed = float(input("몇 초 안에 실행시키고 싶으신가요?"))
        
        vel = self.speed_check(speed)
        
        self.base(color_layer)
        self.move(vel, self.border())
  
        
a = refract()
a.activate()
