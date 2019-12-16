from pynput import keyboard
import time
import pyaudio
import wave
import sched
import sys

CHUNK = 8192
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000
dev_index = 1
RECORD_SECONDS = 60
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()
frames = []

def callback(in_data, frame_count, time_info, status):
    frames.append(in_data)
    return (in_data, pyaudio.paContinue)

class MyListener(keyboard.Listener):
    def __init__(self):
        super(MyListener, self).__init__(self.on_press, self.on_release)
        self.key_pressed = None
        self.wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        self.wf.setnchannels(CHANNELS)
        self.wf.setsampwidth(p.get_sample_size(FORMAT))
        self.wf.setframerate(RATE)
    def on_press(self, key):
        if key.char == 'r':
            self.key_pressed = True
        return True

    def on_release(self, key):
        if key.char == 'r':
            self.key_pressed = False
        return True


listener = MyListener()
listener.start()
started = False
stream = None

def recorder():
    global started, p, stream, frames

    if listener.key_pressed and not started:
        # Start the recording
        try:
            stream = p.open(format=FORMAT,
                             rate=RATE,
                             channels=CHANNELS,
                             input_device_index = dev_index,
                             input=True,
                             frames_per_buffer=CHUNK,
                             stream_callback = callback)
            print("Stream active:", stream.is_active())
            started = True
            print("start Stream")
        except:
            raise

    elif not listener.key_pressed and started:
        print("Stop recording")
        stream.stop_stream()
        stream.close()
        p.terminate()
        listener.wf.writeframes(b''.join(frames))
        listener.wf.close()
        print ("You should have a wav file in the current directory")
        sys.exit()
    # Reschedule the recorder function in 100 ms.
    task.enter(0.1, 1, recorder, ())


print ("Press and hold the 'r' key to begin recording")
print ("Release the 'r' key to end recording")
task = sched.scheduler(time.time, time.sleep)
task.enter(0.1, 1, recorder, ())
task.run()