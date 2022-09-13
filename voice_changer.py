import signal
import time
import argparse

import librosa
import numpy as np
import pyaudio
from pysndfx import AudioEffectsChain

audio = pyaudio.PyAudio()

parser = argparse.ArgumentParser(description='Microphone voice changer program (by hivaze)')

parser.add_argument('-regime', '-r', type=str, required=True,
                    action='store',
                    help='Regime of program launch', choices=['run', 'devices'])
parser.add_argument('-microphone_device', '-md', type=int,
                    action='store',
                    help='Device ID of microphone (input channels)')
parser.add_argument('-virtual_device', '-vd', type=int,
                    action='store',
                    help='Virtual device ID (output channels)')
parser.add_argument('-chunk_size', '-cs', type=int, default=12,
                    action='store',
                    choices=[6, 8, 10, 12, 14, 16], help='Chunk size for microphone device')
parser.add_argument('-volume_mult', '-vm', type=float, default=12.0,
                    action='store',
                    help='Volume adjust multiplier (8-17 is a good value)')
parser.add_argument('-pitch_shift', '-ps', type=float, default=-3.0,
                    action='store',
                    help='Pitch shift, values in (-5, +5) are okey')
parser.add_argument('-reverse', action='store_true',
                    help='Use reverse effect')

params = parser.parse_args()

if params.regime == 'devices':
    print('All found sound devices:')
    for i in range(0, audio.get_device_count()):
        info = audio.get_device_info_by_index(i)
        print(info, '\n')
    exit(0)

microphone_device = audio.get_device_info_by_index(params.microphone_device)
virtual_device = audio.get_device_info_by_index(params.virtual_device)

print('Selected micro device:', str(microphone_device['index']) + ' | ' + microphone_device['name'], '|',
      'SR:', microphone_device['defaultSampleRate'])
print('Selected virtual device:', str(virtual_device['index']) + ' | ' + virtual_device['name'], '|',
      'SR:', virtual_device['defaultSampleRate'])

FORMAT = pyaudio.paFloat32

CHUNK_SIZE = params.chunk_size * 1024

VOLUME_ADJUST = params.volume_mult
PITCH_STEPS = params.pitch_shift

fx = (
    AudioEffectsChain()
    # .echo()
    # .highshelf()
    .reverb(reverberance=100, hf_damping=100, pre_delay=20)
    # .echo()
    # .pitch(shift=+100)
    # .phaser()
    # .equalizer(70, db=+10)
    # .delay()
    # .lowshelf()
)


def close_streams(signum, frame):
    print('Cancellation signal', signum, '...')
    microphone_stream.stop_stream()
    virtual_stream.stop_stream()


def microphone_callback(in_data, frame_count, time_info, status):
    if microphone_stream.is_active() or status == 0:
        array = np.frombuffer(in_data, np.float32)
        sr = virtual_device['defaultSampleRate']

        y = librosa.resample(array, microphone_device['defaultSampleRate'], sr, res_type='kaiser_best', fix=False)
        y *= VOLUME_ADJUST

        # sox effects
        # y = fx(y)

        # librosa effects
        y = librosa.effects.pitch_shift(y, sr, n_steps=PITCH_STEPS, res_type='kaiser_best')

        if params.reverse:
            y = np.flip(y, axis=None)

        virtual_stream.write(y.tobytes())

        return None, pyaudio.paNoError
    else:
        return None, pyaudio.paAbort


virtual_stream = audio.open(format=FORMAT,
                            channels=int(virtual_device['maxOutputChannels']),
                            rate=int(virtual_device['defaultSampleRate']),
                            output=True,
                            output_device_index=int(virtual_device['index']),
                            frames_per_buffer=CHUNK_SIZE)

microphone_stream = audio.open(format=FORMAT,
                               channels=int(microphone_device['maxInputChannels']),
                               rate=int(microphone_device['defaultSampleRate']),
                               input=True,
                               input_device_index=int(microphone_device['index']),
                               frames_per_buffer=CHUNK_SIZE,
                               stream_callback=microphone_callback)

print('Start of streaming...')

if __name__ == '__main__':
    signal.signal(signal.SIGINT, close_streams)
    signal.signal(signal.SIGTERM, close_streams)
    while microphone_stream.is_active():
        time.sleep(0.1)
