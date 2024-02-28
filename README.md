## RIFF Header Reader

This is just a quick test script for reading the scott header of a RIFF Wave container. To use, simply clone this repo and execute `scott_header.py {wave_file.wav}` to see the results.

```
$ git clone https://github.com/maxtimbo/riff_headers
$ cd riff_headers
$ python3 scott_headers.py SampleWav.wav
$ python3 scott_headers.py NEW1234.wav
$ python3 scott_headers.py SP1234.wav
```

The audio files are each a little different:

- SampleWav.wav has no scot headers
- NEW1234.wav has scot headers created by Audition v3
- SP1234.wav has processed headers
