## Microphone voice changer program

This soft allows you to change your voice during voice calls or for recording directly from your micro.

### Requirements
Soft requirements are in `requirements.txt` file, its only 4 libs:
- librosa (for basic audio processing)
- numpy (technical requirement)
- PyAudio (for audio streaming)
- pysndfx (for complex effects)

Also you need to install a virtual audio cable (VAC), more about this technology you can read [here](https://vac.muzychenko.net/en/).

Good choice of VAC for Windows is [VoiceMeeter](https://voicemeeter.com)\
For Linux in can be [JACK Audio Connection Kit](https://alternativeto.net/software/jack-audio-connection-kit/about/)

If you want complex audio effects you need to install `sox` toolkit:
`conda install -c conda-forge sox`

### How to run
Best choice of soft installation is creation of virtual env from requirements:
```
git clone https://github.com/hivaze/voice_changer/
cd voice_changer/
pip install virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```
After this you can use program CLI to deterine audio devices\
 `python voice_changer.py -r devices` 

Then you can run `python voice_changer.py --help` , and see this help message:
```
usage: voice_changer.py [-h] -regime {run,devices} [-microphone_device MICROPHONE_DEVICE] [-virtual_device VIRTUAL_DEVICE] [-chunk_size {6,8,10,12,14,16}] [-volume_mult VOLUME_MULT]
                        [-pitch_shift PITCH_SHIFT] [-reverse]

Voice changer program

optional arguments:
  -h, --help            show this help message and exit
  -regime {run,devices}, -r {run,devices}
                        Regime of program launch
  -microphone_device MICROPHONE_DEVICE, -md MICROPHONE_DEVICE
                        Device ID of microphone (input channels)
  -virtual_device VIRTUAL_DEVICE, -vd VIRTUAL_DEVICE
                        Virtual device ID (output channels)
  -chunk_size {6,8,10,12,14,16}, -cs {6,8,10,12,14,16}
                        Chunk size for microphone device
  -volume_mult VOLUME_MULT, -vm VOLUME_MULT
                        Volume adjust multiplier (8-17 is a good value)
  -pitch_shift PITCH_SHIFT, -ps PITCH_SHIFT
                        Pitch shift, values in (-5, +5) are okey
  -reverse              Use reverse effect
```

To hear the results you need to change your micro to VAC output in target program (e.g. Discord). You can easily test this soft in VoiceMeeter on Windows.