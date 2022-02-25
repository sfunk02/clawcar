# Clawcar Project

## Table of Contents
* [Table of Contents](#TableOfContents)
* [Introduction](#Introduction)
* [Planning](#Planning_Stage)
* [CAD](#CAD)
* [Code](#Code)
* [Building the Robot](#Building_the_Robot)
* [Final Product](#Final_Product)

## Introduction
For this project, we were assigned to create something that uses a robot arm. Our constraints consisted of 2 months of time and materials available in the lab or any materials 
that could be easily obtained. We had access to hardware, acrylic, a laser cutter, and 3D printers to create our robot.

## Planning_Stage

[Planning Document](https://docs.google.com/document/d/18APe1ReYu_2JsjmeK-9Reznoc6AoXzXg0CE4DWNOTgk/edit?usp=sharing)

## CAD

[Onshape Document](https://cvilleschools.onshape.com/documents/68aa0f638d08d1c7e2145037/w/4b7c45ff2284ca1a7005927c/e/dc6fd3a74e3c54772968f738)


## Code
I used pulse values defined as arrays at the beginning of my code to trigger if statements to move servo's and motors controlled by an IR remote. The code below can be used with 
wiring found [here](https://learn.adafruit.com/ir-sensor/using-an-ir-sensor) to find pulse values from any IR remote. These pulse values will be key for using a remote to 
control your CircuitPyhton device.
``` python
import board
import pulseio
import adafruit_irremote

IR_PIN = board.D2  # Pin connected to IR receiver.

print('IR listener')
# Fuzzy pulse comparison function:
def fuzzy_pulse_compare(pulse1, pulse2, fuzzyness=0.2):
    if len(pulse1) != len(pulse2):
        return False
    for i in range(len(pulse1)):
        threshold = int(pulse1[i] * fuzzyness)
        if abs(pulse1[i] - pulse2[i]) > threshold:
            return False
    return True

# Create pulse input and IR decoder.
pulses = pulseio.PulseIn(IR_PIN, maxlen=200, idle_state=True)
decoder = adafruit_irremote.GenericDecode()
pulses.clear()
pulses.resume()
# Loop waiting to receive pulses.
while True:
    # Wait for a pulse to be detected.
    detected = decoder.read_pulses(pulses)
    print('got a pulse...')
    # Got a pulse, now compare.
    if fuzzy_pulse_compare(pulses, detected):
        print('Received correct remote control press!')
    else:
        print("Heard", len(detected), "Pulses:", detected)
        print("-")
```
This code should put pulse arrays in your serial monitor that you need to keep and input into your code at the beginning.
Once you have your pulse values, you can put them in an array like this at the beginning of your code:
```pyhton
p1 = [1184, 977, 2239]
p2 = [1173, 1008, 1124, 1034, 1122]
p3 = [1185, 976, 3324]
```
This will make these pulse values identifiable by the following code, which compares pulses from the remote with the pulses you input and can read if they are the same.
``` python
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
```
Now you use if statements and your compare function to set the condtion that if x button is pressed then y will happen. I have ran into issues concerning my metro express's 
storage as well as timers being used up. I fixed these issues by clearing out everything in my Metro except what I needed to use right then, and by adding de initialize 
functions in my buttons. The motors are initialized not at the beginning of the code but in an if statement, because not all of the pwm I used could work at once. Up, left down 
and right all have intialize functions in them with the ok button being a hard stop and deinitialize for all the motors. The servos initialize and deinitialize everytime they 
are given a command. When it all came together it looked like this:

``` pyhton
import pulseio
import board
import adafruit_irremote
import motor
import pwmio
import servo
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


while True:
    detected = decoder.read_pulses(pulses)
    if fuzzy_pulse_compare(pu, detected):
        print('up')
        print("\nForwards slow")
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
        motor1.throttle = 0.5
        print("  throttle:", motor1.throttle)
        motor2.throttle = 0.5
        print("  throttle:", motor2.throttle)
    if fuzzy_pulse_compare(pd, detected):
        print('down')
        print("\nBackwards")
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
        motor1.throttle = -0.5
        print("  throttle:", motor1.throttle)
        motor2.throttle = -0.5
        print("  throttle:", motor2.throttle)
    if fuzzy_pulse_compare(pl, detected):
        print('left')
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
        motor1.throttle = 1
    if fuzzy_pulse_compare(pr, detected):
        print('right')
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
        pwm1 = pulseio.PWMOut(board.D10, frequency=50)
        myServo1 = servo.Servo(pwm1, min_pulse=750, max_pulse=2250)
        pwm2 = pulseio.PWMOut(board.D12, frequency=50)
        myServo2 = servo.Servo(pwm2, min_pulse=750, max_pulse=2250)
        myServo2.angle = 100
        myServo1.angle = 10
        time.sleep(servoDelay)
        pwm1.deinit()
        pwm2.deinit()
    if fuzzy_pulse_compare(p2, detected):
        print('2')
        pwm3 = pulseio.PWMOut(board.D8, frequency=50)
        myServo3 = servo.Servo(pwm3, min_pulse=750, max_pulse=2250)
        myServo3.angle = 100
        time.sleep(servoDelay)
        pwm3.deinit()
    if fuzzy_pulse_compare(p3, detected):
        print('3')
        pwm4 = pulseio.PWMOut(board.D13, frequency=50)
        myServo4 = servo.Servo(pwm4, min_pulse=750, max_pulse=2250)
        myServo4.angle = 165
        time.sleep(servoDelay)
        print(myServo4.angle)
        pwm4.deinit()
    if fuzzy_pulse_compare(p4, detected):
        print('4')
        pwm1 = pulseio.PWMOut(board.D10, frequency=50)
        myServo1 = servo.Servo(pwm1, min_pulse=750, max_pulse=2250)
        pwm2 = pulseio.PWMOut(board.D12, frequency=50)
        myServo2 = servo.Servo(pwm2, min_pulse=750, max_pulse=2250)
        myServo1.angle = 100
        myServo2.angle = 10
        time.sleep(servoDelay)
        pwm1.deinit()
        pwm2.deinit()
    if fuzzy_pulse_compare(p5, detected):
        print('5')
        pwm3 = pulseio.PWMOut(board.D8, frequency=50)
        myServo3 = servo.Servo(pwm3, min_pulse=750, max_pulse=2250)
        myServo3.angle = 0
        time.sleep(servoDelay)
        pwm3.deinit()
    if fuzzy_pulse_compare(p6, detected):
        print('6')
        pwm4 = pulseio.PWMOut(board.D13, frequency=50)
        myServo4 = servo.Servo(pwm4, min_pulse=750, max_pulse=2250)
        print(myServo4.angle)
        myServo4.angle = 110
        time.sleep(servoDelay)
        print(myServo4.angle)
        pwm4.deinit()
```

## Building_the_Robot

## Final_Product
