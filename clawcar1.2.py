import board
import pulseio
import adafruit_irremote
from adafruit_motor import motor
from adafruit_motor import servo
import pwmio
import time


IR_PIN = board.D2
pu = [1171, 1009, 3292, 1022, 2206]
pl = [1185, 975, 1157, 3185, 2211]
pr = [1168, 1012, 2205, 2108, 2203]
pd = [1179, 980, 1152, 1028, 1128, 1030, 2211]
pok = [1146, 1011, 2207, 1030, 3288]
p1 = [1184, 977, 2239]
p2 = [1173, 1008, 1124, 1034, 1122]
p3 = [1185, 976, 3324]
p4 = [1119, 1039, 1170, 2067, 1142]
p5 = [1212, 970, 2227, 1011, 1140]
p6 = [1089, 1096, 1056, 1103, 2163]
p7 = [1191, 980, 4321]
p8 = [1191, 982, 1140, 3149, 1139]
p9 = [1192, 980, 2217, 2073, 1137]

print('IR listener')
def fuzzy_pulse_compare(pulse1, pulse2, fuzzyness=0.2):
    if len(pulse1) != len(pulse2):
        return False
    for i in range(len(pulse1)):
        threshold = int(pulse1[i] * fuzzyness)
        if abs(pulse1[i] - pulse2[i]) > threshold:
            return False
    return True

pulses = pulseio.PulseIn(IR_PIN, maxlen=200, idle_state=True)
decoder = adafruit_irremote.GenericDecode()
pulses.clear()
pulses.resume()

A1 = board.D4
A2 = board.D5
pwmA1 = pwmio.PWMOut(A1, frequency=50)
pwmA2 = pwmio.PWMOut(A2, frequency=50)
motor1 = motor.DCMotor(pwmA1, pwmA2)
B1 = board.D7
B2 = board.D6
pwmB1 = pwmio.PWMOut(B1, frequency=50)
pwmB2 = pwmio.PWMOut(B2, frequency=50)
motor2 = motor.DCMotor(pwmB1, pwmB2)

pwm1 = pwmio.PWMOut(board.D10, frequency=50)
myServo1 = servo.Servo(pwm1, min_pulse=750, max_pulse=2250)

pwm2 = pwmio.PWMOut(board.D12, frequency=50)
myServo2 = servo.Servo(pwm2, min_pulse=750, max_pulse=2250)

pwm3 = pwmio.PWMOut(board.D8, frequency=50)
myServo3 = servo.Servo(pwm3, min_pulse=750, max_pulse=2250)

pwm4 = pwmio.PWMOut(board.D11, frequency=50)
myServo4 = servo.Servo(pwm4, min_pulse=750, max_pulse=2250)

myServo1.angle = 90
myServo2.angle = 90
myServo3.angle = 50
myServo4.angle = 120


while True:
    detected = decoder.read_pulses(pulses)
    if fuzzy_pulse_compare(pu, detected):
        print('up')
        motor1.throttle = 1
        print("  throttle:", motor1.throttle)
        motor2.throttle = 0.5
        print("  throttle:", motor2.throttle)
    if fuzzy_pulse_compare(pd, detected):
        print('down')
        motor1.throttle = -1
        print("  throttle:", motor1.throttle)
        motor2.throttle = -0.5
        print("  throttle:", motor2.throttle)
    if fuzzy_pulse_compare(pl, detected):
        print('left')
        motor1.throttle = 1
    if fuzzy_pulse_compare(pr, detected):
        print('right')
        motor2.throttle = 1
    if fuzzy_pulse_compare(pok, detected):
        print('ok')
        print("\nStop")
        motor1.throttle = 0
        print("  throttle:", motor1.throttle)
        motor2.throttle = 0
        print("  throttle:", motor2.throttle)

    if fuzzy_pulse_compare(p1, detected):
        print('1')
        print(myServo1.angle)
        servo1angle = myServo1.angle
        servo2angle = myServo2.angle
        for i in range(1, 9):
            myServo1.angle = servo1angle + i
            myServo2.angle = servo2angle - i
            time.sleep(.02)
            print(myServo1.angle)
    if fuzzy_pulse_compare(p4, detected):       #Resets lower arms
        button1toggle = False
        print('4')
        myServo2.angle = 80
        myServo1.angle = 100

    if fuzzy_pulse_compare(p2, detected) and myServo3.angle < 90:
        print('2')
        servo3angle = myServo3.angle
        for i in range(1, 6):
            myServo3.angle = servo3angle - i
            time.sleep(.02)
            print(myServo3.angle)
    if fuzzy_pulse_compare(p5, detected):       #Resets upper arm
        print('5')
        myServo3.angle = 60
        print(myServo3.angle)

    if fuzzy_pulse_compare(p3, detected) and myServo4:       #Opens claw
        print('3')
        servo4angle = myServo4.angle
        for i in range(int(servo4angle), 160):
            myServo4.angle = i
            time.sleep(.01)
        print(myServo4.angle)
    if fuzzy_pulse_compare(p6, detected):       #Closes claw
        print('6')
        servo6angle = myServo4.angle
        for i in range(int(servo6angle), 100, -1):
            myServo4.angle = i
            time.sleep(.01)
        print(myServo4.angle)

    if fuzzy_pulse_compare(p9, detected):       #Resets arms
        print('9')
        myServo3.angle = 60
        myServo1.angle = 40
        myServo2.angle = 140
