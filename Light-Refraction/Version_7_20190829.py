from vpython import *
import random
import math

class refract:
    
    def angle_ref(self, st_ang, st_vel, n1, n2):   
        '''
        빛의 전반사 및 굴절에서 각도 & 속도를 계산하는 함수
        n1 * sin(θ1) = n2 * sin(θ2)의 스넬의 법칙에 의해
            n1 / n2 * sin(θ1)이 0.9999 이상이면 전반사, 미만이면 굴절
        (부동 소수점에 의해 1이어야 함에도 0.9999...이 나와
            전반사하지 않는 경우가 존재 -> 1이 아닌 0.9999)
             
        입력 변수:
        st_ang : 입사각, float
        st_vel : 입사 속도, vector
        n1 : 입사 굴절률, float
        n2 : 굴절 굴절률, float
        
        내장 변수:
        i : 원래 빛이 진행하던 방향 -> -1 : 아래, 1 : 위
        
        리턴 변수:
        fi_vel : 굴절 속도, vector
        fi_ang : 굴절각, float
        i : 빛이 진행하는 방향, int -> -1 : 위, 1 : 아래
        '''
        
        i = -1 if st_vel.y < 0 else 1
        
        if n1 * math.sin(st_ang) / n2 >= 0.9999:
            #전반사가 일어났는지 확인
            fi_vel = vector(st_vel.x, st_vel.y * (-1), 0)
            fi_ang = st_ang
            
            return fi_vel, fi_ang, i
        
        fi_ang = math.asin(n1 * math.sin(st_ang) / n2)
        fi_vel_mag = n1 * st_vel.mag / n2
        fi_vel = vector(fi_vel_mag * math.sin(fi_ang), i * fi_vel_mag * math.cos(fi_ang), 0)
        
        return fi_vel, fi_ang, i * (-1)
    
    
    def time_ref(self, st_ang, n1, n2, direc):
        '''
        angle_ref의 축약본 함수로, 시간을 계산하는 speed_check 함수에 적용
        속도 계산 등의 과정 없이, 각도, 방향, 진행 정도만을 리턴
        
        입력변수:
        st_ang : 입사각, float
        n1 : 입사 굴절률, float
        n2 : 굴절 굴절률, float
        direc : 진행 방향, float -> 1 : 아래, -1 : 위
        
        리턴 변수:
        첫번째 값 : 굴절각, float
        direc : 진행 방향, int
        세번째 값 : 진행 정도, int -> 전반사 : 그 층에 머무르므로 0, 
            굴절 : 다음 층으로 넘어가므로 1
        '''
        
        if n1 * math.sin(st_ang) / n2 >= 0.9999:
            #전반사가 일어났는지 확인
            
            return st_ang, direc * (-1), 0
        
        return math.asin(n1 * math.sin(st_ang) / n2), direc, 1
    
    
    def border(self):
        '''
        각 층의 경계면의 y좌표를 얻어내는 함수
        
        내장 변수:
        border_temp : 전에 계산한 층들의 총 두께, float
        
        리턴 변수:
        border_pos : 경계면의 y좌표, list
        '''
        
        border_pos = []
        border_temp = 0
        
        for i in range(len(self.data)-1):
            border_pos.append(self.thick/2 - border_temp - self.data[i][1])
            border_temp += self.data[i][1]
        
        return border_pos
            
    
    def speed_check(self, speed):
        '''
        입력한 정도의 시간 speed 내에 프로그램을 끝내기 위해 
            굴절률 1에서 진행해야 하는 속도를 계산하는 함수
            
        이는 굴절률 1에서의 속도가 1임을 가정하여 걸리는 시간 timer를 구한 다음,
            속도를 timer / speed로 지정
            
                    
        입력 변수:
        speed : 프로그램이 진행할 총 시간, float
            
        내장 변수:
        time_check : 현재 있는 층의 번호, int
        timer : 진행한 시간의 총합, float
        xpos : 맨 왼쪽에서부터 x방향으로 진행한 길이, float
        ang : 입사각, float
        direc : 현재 진행 방향, int -> -1 : 위, 1 : 아래
        
        리턴 변수:
        굴절률 1에서의 속도, vector
        '''
        time_check = 0
        timer = 0
        xpos = 0
        ang = self.ang
        direc = 1
        
        while time_check >= 0 and time_check < len(self.data):
            #빛이 구현되는 층 내에 존재하는 동안
            timer += self.data[time_check][1] * self.data[time_check][0] / math.cos(ang)
            xpos += math.tan(ang) * self.data[time_check][1]
            if time_check == len(self.data) - 1 or (time_check == 0 and direc == -1):
                #양쪽 끝에 도달하였는지 확인
                break
                
            #각도 변형
            ang, direc, change = self.time_ref(ang, self.data[time_check][0], 
                                               self.data[time_check + direc][0], direc)
            
            time_check += change * direc

            if xpos > self.length - math.tan(ang) * self.data[time_check][1]:
                #빛이 구현하는 x방향 범위를 벗어나는지 확인
                timer += (self.length - xpos) * self.data[time_check][0] / math.sin(ang)
                break

        c = timer / speed

        return vector(c * math.sin(self.ang), (-1) * c * math.cos(self.ang), 0)
    
    
    def base(self, color_layer):
        '''
        층들을 생성하는 함수
        
        입력 변수:
        color_layer : 각 굴절률에 따른 색깔을 주는 딕셔너리, dict
        
        내장 변수:
        back : 빛이 진행하는 모든 층의 뒷판, box
        a : 빛이 진행하는 층, box
        self.light : 빛, sphere
        
        '''
        
        scene = canvas()

        back = box(pos = vector(0,0,0), size = vector(self.length, self.thick, 5), color = vector(1,1,1))

        temp_height = 0
        for layer in range(len(self.data)):
            a = box(pos = vector(0, self.thick/2 - temp_height - self.data[layer][1]/2, 5), 
                    size = vector(self.length, self.data[layer][1], 5), opacity = 0.3, color = color_layer[self.data[layer][0]])
            temp_height += self.data[layer][1]

        self.light = sphere(pos = vector((-1) * self.length/2, self.thick /2, 5), 
                    size = vector(1,1,1), color = vector(1,1,0), make_trail=True)
        
        
        n_green = vector(53/255*2, 83/255*2, 10/255*2)
        body = cylinder(pos = vector(0-self.length/2,10.5+self.thick/2,5), axis = vector(0, -10, 0), color = n_green)
        head = sphere(pos = vector(0-self.length/2,0.5+self.thick/2,5), radius = 1, color = n_green)
        wing = box(pos = vector(0-self.length/2,3.5+self.thick/2,5), size = vector(12,1,1), color = n_green)
        tripath = [vec(0,0,4.5), vec(0,0,5.5)]
        lwing = [ [0+self.length/2,4+self.thick/2],[0+self.length/2,7.5+self.thick/2],[6+self.length/2,4+self.thick/2],\
                 [0+self.length/2,4+self.thick/2] ]
        rwing = [ [0+self.length/2,4+self.thick/2],[0+self.length/2,7.5+self.thick/2],[-6+self.length/2,4+self.thick/2],\
                 [0+self.length/2,4+self.thick/2] ]
        backprop = cylinder(pos = vector(-3-self.length/2,10+self.thick/2,5), axis = vector(6,0,0), radius = 0.5, color = n_green)
        lwing2 = extrusion(path = tripath, shape = lwing, color = n_green)
        rwing2 = extrusion(path = tripath, shape = rwing, color = n_green)
        
        self.target_pos = random.randint(self.length/(-20)+1,self.length/20)*10
        target = cylinder(pos = vector(self.target_pos,self.thick/(-2)-0.5,0), axis = vector(0, -1, 0), radius = 10)
        
    def move(self, vel, border_pos):
        '''
        빛의 구를 움직이는 함수
        3초간의 딜레이 후, 층의 경계가 나올 때까지 빛을 이동
        층의 경계가 나오면, angle_ref 실행
        
        입력 변수:
        vel : 굴절률 1에서의 속도, vector
        border_pos : 경계면의 y좌표, list
        
        내장 변수:
        ang : 입사각, float
        timing : 딜레이한 시간(초) * 200, int
        dt : 촘촘히 실행하는 정도, float
        direc : 현재 진행 방향, int -> -1 : 위, 1 : 아래
        temp : 빛이 경계면에 있는지에 대한 판단, str/int
        float_value_adj : 똑같은 경계면에서 연속적으로 angle_ref가 실행되지
            않도록 하는 변수, bool / int
        '''
        
        vel /= self.data[0][0]
        ang = self.ang
        
        timing = 0
        while timing <= 600:
            #3초간의 딜레이
            rate(200)
            timing += 1
            
        dt = 1/500
        direc = 1
        float_value_adj = None

        while self.light.pos.y < self.thick/2 + 1 and self.light.pos.y > self.thick/2 * (-1) - 1 and \
            self.light.pos.x < self.length / 2 + 1 and self.light.pos.x > 0 - self.length / 2 - 1:
            #빛이 구현되는 층 내에 존재하는 동안
            
            rate(500)
            self.light.pos += vel * dt
            temp = 'None'
            
            for i in range(len(border_pos)):
                if self.light.pos.y < border_pos[i] + 0.1 and self.light.pos.y > border_pos[i] - 0.1:
                    #빛이 경계면에 도달하였는지 확인
                    temp = i
                    break
                    
            if temp != 'None' and float_value_adj != temp:
                vel, ang, direc = self.angle_ref(ang, vel, self.data[int(temp +(1-direc)/2)][0], self.data[int(temp+(direc+1)//2)][0])
                
                float_value_adj = temp
    
    
    def activate(self):
        '''
        프로그램 자체를 실행하는 함수
        
        내장 변수:
        self.length : 층의 가로 길이, float
        layer_num : 층의 개수, int
        self.data : 각 층의[굴절률, 두께]에 대한 데이터, list
        color_layer : 굴절률에 따른 층의 색깔에 대한 데이터, dict
        self.thick : 모든 층의 두께의 합, float
        self.ang : 입사각, float
        speed : 프로그램이 진행할 총 시간, float
        '''
        
        self.length = random.randint(1,5) * 100
        layer_num = random.randint(1, 5)
        self.data = []
        color_layer = {1 : vector(1,1,1)}
        self.thick = 0
        
        for i in range(layer_num):
            #각 층에 대한 데이터 입력
            self.data.append([random.randint(1, 10)/3, random.randint(1, 3)*50])
            self.thick += self.data[-1][1]
            
            if self.data[-1][0] not in color_layer.keys():
                color_layer[self.data[-1][0]] = vector(random.random(), random.random(), random.random())
                
        self.base(color_layer)
                
        print("총 층의 개수는", layer_num, "입니다.")
        for i in range(len(self.data)):
            print(i+1, "번째 층의 굴절률은", self.data[i][0], "이며, 그 층의 두께는", self.data[i][1], "입니다.")
            
        self.ang = float(input("총을 쏠 각도는 얼마인가요?")) * math.pi / 180
        speed = 5.0
        
        vel = self.speed_check(speed)
        

        
        self.move(vel, self.border())
        
        return self.evaluate()

  
    def evaluate(self):
        if self.light.pos.x >= self.target_pos - 10 and self.light.pos.x <= self.target_pos + 10 :
            return True
        else:
            return False
a = refract()

t = False
time = 1
while not t:
    t = a.activate()
    if t:
        print("Congratulations! You managed to beat the game in", time, "times!")
    else:
        T = True
        print("Bad luck! ")
        while T:
            t = input("Would you like to play again? ")
            if t == 'yes' or t == 'YES':
                T = False
                t = False
            elif t == 'no' or t == 'NO':
                T = False
                t = True
            else:
                print("Invalid Input.")
    time += 1
