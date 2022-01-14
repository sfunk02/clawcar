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
