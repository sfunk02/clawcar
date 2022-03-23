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
For this project, we were assigned to create something that uses a robot arm. Our constraints consisted of 2 months of time and materials available in the lab or any materials that could be easily obtained. We had access to hardware, acrylic, a laser cutter, and 3D printers to create our robot.

## Planning_Stage

[Planning Document](https://docs.google.com/document/d/18APe1ReYu_2JsjmeK-9Reznoc6AoXzXg0CE4DWNOTgk/edit?usp=sharing)

Inital problems we faced in planning our project were deciding whether to control the car via Bluetooth or an infrared universal TV remote. We also didn't know whether we wanted to use a SCARA arm or an articulated arm. We ended up choosing infrared over Bluetooth because Bluetooth seemed overly complicated and unnecessary for what we were trying to achieve, and we chose an articulated arm over a SCARA arm because a SCARA arm didn't seem like it would be strong enough to lift anything vertically while also moving horizontally. 

## CAD

[Onshape Document](https://cvilleschools.onshape.com/documents/68aa0f638d08d1c7e2145037/w/4b7c45ff2284ca1a7005927c/e/dc6fd3a74e3c54772968f738)

#### Rack and Pinion

The first piece of this CAD project was to design a rack and pinion for the claw to open and close with a single 180 micro-servo. In order to create it, I used a spur gear function on Onshape, and then designed a gear rack off of the geometry of the gear. Using a rack and pinion mate allowed the gear to turn while the rack moved back and forth. Lastly, walls to mount the rack onto were designed, with a hole on one side to connect the servo.

<img src="Images/RackandPinion.png" alt="RackandPinion" width="400" height="150"/>



---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#### Claw Fingers
The next piece of the project was designing the claw fingers, which are pieces of gear with curved grab fingers (Shown below). These fingers have gears on the back end, which connect to a cylindrical gear rack on the end of the rack and pinion assembly. This was designed after a wine bottle opener.

<img src="Images/ClawFingers.png" alt="ClawFingers" width="250" height="450"/> <img src="Images/BottleOpener180.png" alt="BottleOpener" width="450" height="450"/>



---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#### Bracket Connector
This bracket was somewhat difficult to design, because it had to be able to hold the three claw fingers in a circular orientation split evenly around a circle. Additionally, the square hole in the center had to be offset to account for the offset of the rack attached to the micro-servo.

<img src="Images/Bracket.png" alt="Bracket" width="400" height="300"/>


---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#### Full Upper Arm
This image shows the upper arm and claw assembly, which includes a gear at the elbow that uses a belt to connect to a servo on the car base. This belt allows for rotation of the upper arm around an axis. The lower arm bends back and forth by two servos working in parallel, in order for extra strength (shown in Car Base).

<img src="Images/Claw_full_arm.png" alt="Claw_full_arm" width="400" height="130"/>


---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#### Car Base
This is the car base rendered in CAD, complete with screw holes, batter holders, motor mounts, servos, and switches.

<img src="Images/Car_Base.png" alt="Car_Base" width="380" height="220"/>


---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#### Completed Assembly
This is the completed car, arm, and claw rendered in CAD. It does not show the motors and belts because we could not find them in the parts folder we have access to.

<img src="Images/Full_car.png" alt="Full_car" width="400" height="300"/>


---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Code

``` python
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
p7 = [1200, 983, 4348]
p8 = [1194, 988, 1145, 3168, 1144]
servoDelay = .25

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
        motor1.throttle = 1
        print("  throttle:", motor1.throttle)
        motor2.throttle = .9
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
        motor2.throttle = -0.45
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
# Write your code here :-)
    if fuzzy_pulse_compare(p1, detected):
        print('1')
        pwm1 = pulseio.PWMOut(board.D10, frequency=50)
        myServo1 = servo.Servo(pwm1, min_pulse=750, max_pulse=2250)
        pwm2 = pulseio.PWMOut(board.D12, frequency=50)
        myServo2 = servo.Servo(pwm2, min_pulse=750, max_pulse=2250)
        myServo2.angle = 100
        myServo1.angle = 10
        time.sleep(servoDelay)
        pwm3 = pulseio.PWMOut(board.D8, frequency=50)
        myServo3 = servo.Servo(pwm3, min_pulse=750, max_pulse=2250)
        myServo3.angle = 160
        time.sleep(servoDelay)
    if fuzzy_pulse_compare(p2, detected):
        print('2')
        myServo1.angle = 90
        myServo2.angle = 20
        time.sleep(servoDelay)
        pwm1.deinit()
        pwm4 = pulseio.PWMOut(board.D13, frequency=50)
        myServo4 = servo.Servo(pwm4, min_pulse=750, max_pulse=2250)
        myServo4.angle = 50
        time.sleep(servoDelay)
        myServo3.angle = 110
    if fuzzy_pulse_compare(p3, detected):
        print('3')
        myServo4.angle = 115
        time.sleep(servoDelay)
        myServo3.angle = 160
        pwm4.deinit()
    if fuzzy_pulse_compare(p4, detected):
        print('4')
        time.sleep(servoDelay)
        pwm1 = pulseio.PWMOut(board.D10, frequency=50)
        myServo1 = servo.Servo(pwm1, min_pulse=750, max_pulse=2250)
        myServo2.angle = 105
        myServo1.angle = 5
        time.sleep(servoDelay)
        pwm1.deinit()
        pwm2.deinit()
        pwm3.deinit()
```

## Building_the_Robot
For the most part, assembling the final product was fairly straightforward. Mostly everything fit where it was supposed to go. We ran into a few problems, one of which was that the middle servo bracket cracked once screwed in, and we had to replace it. The second was that the arms were difficult to put together in the collar holding the claw, but we ended up resolving this by the end. We were able to slide the pieces together and leave one screw out without sacrificing any major durability.

Additionally, we decided to replace the three 180 servos on the car base with stronger servos to better support the weight of the arm, and the microservo was also replaced 3 times, because it kept breaking.

This was due to a struggle with getting the code for the claw microservo to work; the range of motion would always push the rod too far, breaking the servo.
In order to fix this, we tested smaller ranges of motion, so if the code was faulty, it would not damage the mechanics.

## Final_Product
