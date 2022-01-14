import board
import pulseio
import adafruit_irremote

IR_PIN = board.D2  # Pin connected to IR receiver.

# Expected pulse, pasted in from previous recording REPL session:
pulseup = [1171, 1009, 3292, 1022, 2206]
pulseright = [1168, 1012, 2205, 2108, 2203]
pusleleft = [1168, 1012, 2205, 2108, 2203]
pulsedown = [1179, 980, 1152, 1028, 1128, 1030, 2211]
pulse1 = [1184, 977, 2239]
pulse2 = [1173, 1008, 1124, 1034, 1122]
pulse3 = [1185, 976, 3324]
pulse4 = [1119, 1039, 1170, 2067, 1142]



def fuzzyness=.2
    if len(pulseup):
        print("up")


















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
    if fuzzy_pulse_compare(pulseup, detected):
        print('Received correct remote control press!')
    else:
        print("Heard", len(detected), "Pulses:", detected)
        print("-")