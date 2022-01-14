import board
import pulseio
import adafruit_irremote
IR_PIN = board.D2
pu = [1171, 1009, 3292, 1022, 2206]
pl = [1185, 975, 1157, 3185, 2211]
pr = [1168, 1012, 2205, 2108, 2203]
pd = [1179, 980, 1152, 1028, 1128, 1030, 2211]
p1 = [1184, 977, 2239]
p2 = [1173, 1008, 1124, 1034, 1122]
p3 = [1185, 976, 3324]
p4 = [1119, 1039, 1170, 2067, 1142]

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
    if fuzzy_pulse_compare(pd, detected):
        print('down')
    if fuzzy_pulse_compare(pl, detected):
        print('left')
    if fuzzy_pulse_compare(pr, detected):
        print('right')
    if fuzzy_pulse_compare(p1, detected):
        print('1')
    if fuzzy_pulse_compare(p2, detected):
        print('2')
    if fuzzy_pulse_compare(p3, detected):
        print('3')
    if fuzzy_pulse_compare(p4, detected):
        print('4')