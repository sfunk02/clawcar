# Write your code here :-)
import board
import pulseio
import adafruit_irremote
from adafruit_motor import motor
from adafruit motor import servo
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


servoDelay = .5

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

pwm1 = pulseio.PWMOut(board.D10, frequency=50)
myServo1 = servo.Servo(pwm1, min_pulse=750, max_pulse=2250)
pwm2 = pulseio.PWMOut(board.D12, frequency=50)
myServo2 = servo.Servo(pwm2, min_pulse=750, max_pulse=2250)
pwm3 = pulseio.PWMOut(board.D8, frequency=50)
myServo3 = servo.Servo(pwm3, min_pulse=750, max_pulse=2250)
pwm4 = pulseio.PWMOut(board.D11, frequency=50)
myServo4 = servo.Servo(pwm4, min_pulse=750, max_pulse=2250)

while True:
    detected = decoder.read_pulses(pulses)
    if fuzzy_pulse_compare(pu, detected):
        print('up')
        print("\nForwards slow")
        motor1.throttle = 0.5
        print("  throttle:", motor1.throttle)
        motor2.throttle = 0.5
        print("  throttle:", motor2.throttle)
    if fuzzy_pulse_compare(pd, detected):
        print('down')
        print("\nBackwards")
        motor1.throttle = -0.5
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
        pwmA1.deinit()
        pwmA2.deinit()
        pwmB1.deinit()
        pwmB2.deinit()
    if fuzzy_pulse_compare(p1, detected):
        print('1')
        myServo2.angle = 100
        myServo1.angle = 10
        time.sleep(servoDelay)
        pwm1.deinit()
        pwm2.deinit()
    if fuzzy_pulse_compare(p2, detected):
        print('2')
        myServo3.angle = 180
        time.sleep(servoDelay)
        pwm3.deinit()
    if fuzzy_pulse_compare(p3, detected):
        print('3')
        myServo4.angle = 0
        time.sleep(servoDelay)
        pwm4.deinit()
    if fuzzy_pulse_compare(p4, detected):
        print('4')
        myServo1.angle = 100
        myServo2.angle = 10
        time.sleep(servoDelay)
        pwm1.deinit()
        pwm2.deinit()
    if fuzzy_pulse_compare(p5, detected):
        print('5')
        myServo3.angle = 0
        time.sleep(servoDelay)
        pwm3.deinit()
    if fuzzy_pulse_compare(p6, detected):
        print('6')
        print(myServo4.angle)
        time.sleep(servoDelay)
        myServo4.angle = 180
        time.sleep(servoDelay)
        print(myServo4.angle)
        pwm4.deinit()
