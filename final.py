import board
import pulseio
import adafruit_irremote
import motor
import pwmio
import servo
pwm = pulseio.PWMOut(board.D8, frequency=50)
myServo = servo.Servo(pwm, min_pulse=750, max_pulse=2250)
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
    if fuzzy_pulse_compare(p1, detected):
        print('1')
        myServo.angle = 0
    if fuzzy_pulse_compare(p2, detected):
        print('2')
    if fuzzy_pulse_compare(p3, detected):
        print('3')
    if fuzzy_pulse_compare(p4, detected):
        print('4')
    if fuzzy_pulse_compare(p5, detected):
        print('5')
    if fuzzy_pulse_compare(p6, detected):
        print('6')
