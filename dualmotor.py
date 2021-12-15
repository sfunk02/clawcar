# Uses an H-bridge to connect to two TT motors
import time
import board
import pwmio
import motor

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

print("***DC motor test***")

print("\nForwards slow")
motor1.throttle = 0.5
print("  throttle:", motor1.throttle)
motor2.throttle = 0.5
print("  throttle:", motor2.throttle)
time.sleep(1)

print("\nStop")
motor1.throttle = 0
print("  throttle:", motor1.throttle)
motor2.throttle = 0
print("  throttle:", motor2.throttle)
time.sleep(1)

print("\nForwards")
motor1.throttle = 1.0
print("  throttle:", motor1.throttle)
motor2.throttle = 1.0
print("  throttle:", motor2.throttle)
time.sleep(1)

print("\nStop")
motor1.throttle = 0
print("throttle:", motor1.throttle)
motor2.throttle = 0
print("throttle:", motor2.throttle)
time.sleep(1)

print("\nBackwards")
motor1.throttle = -1.0
print("  throttle:", motor1.throttle)
motor2.throttle = -1.0
print("  throttle:", motor2.throttle)
time.sleep(1)

print("\nStop")
motor1.throttle = 0
print("throttle:", motor1.throttle)
motor2.throttle = 0
print("throttle:", motor2.throttle)
time.sleep(1)

print("\nBackwards slow")
motor1.throttle = -0.5
print("  throttle:", motor1.throttle)
motor2.throttle = -0.5
print("  throttle:", motor2.throttle)
time.sleep(1)

print("\nStop")
motor1.throttle = 0
print("  throttle:", motor1.throttle)
motor2.throttle = 0
print("  throttle:", motor2.throttle)
time.sleep(1)

print("\nSpin freely")
motor1.throttle = None
print("  throttle:", motor1.throttle)
motor2.throttle = None
print("  throttle:", motor2.throttle)

print("\n***Motor test is complete***")
