## RIFF Header Reader

This is just a quick test script for reading the scott header of a RIFF Wave container. To use, simply clone this repo and execute `scott-header.py {wave_file.wav}` to see the results.

```
$ git clone https://github.com/maxtimbo/riff_headers
$ cd riff_headers
$ python3 scott-header.py SampleWav.wav
$ python3 scott-header.py NEW1234.wav
$ python3 scott-header.py SP1234.wav
```

The audio files are each a little different:

- SampleWav.wav has no scot headers
- NEW1234.wav has scot headers created by Audition v3
- SP1234.wav has processed headers

Here's how I think this will go from here:

Add ffmpeg to analyse the wav file for length. This is necessary for the asclen parameter.  
There will need a mechanism for adding the 424 + 9 bytes after the RIFF and FMT structs. 9 bytes tells interpreting software that scot header is present. the 424 bytes defines the scot header metadata. The main things that should be added are the `artist` and `title` fields. But other fields must be either spaces or null characters for the header to be valid. Other fields can be added later, such as `kill_dates`, `eomstart` and `eomlength`, `start_seconds` and `end_seconds`, as well as `cart` and 
