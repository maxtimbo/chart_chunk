from struct import calcsize

__all__ = [
    'riff_chunk',
    'fmt_chunk',
    'pcm_chunk',
    'mpeg_chunk',
    'new_mpeg_chunk',
    'scott_chunk',
    'fact_chunk',
    'data_chunk',
    'generate_format'
]

def bin_str(s: str) -> str:
    return ''.join(format(ord(char), '08b') for char in s)

riff_chunk = {
    'riff':             {'format': '4s'},
    'size':             {'format': 'l'},
    'type':             {'format': '4s'}
}

fmt_chunk = {
    'fmt':              {'format': '4s'},
    'fmtsize':          {'format': 'l'}
}

pcm_chunk = {
    'tag':              {'format': 'h'},
    'chan':             {'format': 'h'},
    'sampleRate':       {'format': 'l'},
    'transfrate':       {'format': 'l'},
    'align':            {'format': 'h'},
    'bitsPerSample':    {'format': 'h'}
}

mpeg_chunk = pcm_chunk | {
    'extra':            {'format': 'h', 'data': 0},
    'layer':            {'format': 'h', 'data': 0},
    'bitrate':          {'format': 'l', 'data': 0},
    'mode':             {'format': 'h', 'data': 0},
    'extmode':          {'format': 'h', 'data': 0},
    'emphasis':         {'format': 'h', 'data': 0},
    'flags':            {'format': 'h', 'data': 0},
    'PTSlow':           {'format': 'l', 'data': 0},
    'PTShigh':          {'format': 'l', 'data': 0}
}

new_mpeg_chunk = {
    'extra':            {'format': 'h', 'data': 0},
    'layer':            {'format': 'h', 'data': 0},
    'bitrate':          {'format': 'l', 'data': 0},
    'mode':             {'format': 'h', 'data': 0},
    'extmode':          {'format': 'h', 'data': 0},
    'emphasis':         {'format': 'h', 'data': 0},
    'flags':            {'format': 'h', 'data': 0},
    'PTSlow':           {'format': 'l', 'data': 0},
    'PTShigh':          {'format': 'l', 'data': 0}
}

fact_chunk = {
    'fact':             {'format': '4s'},
    'factsize':         {'format': 'l'},
    'numsamples':       {'format': 'l'}
}

data_chunk = {
    'data':             {'format': '4s'},
    'datasize':         {'format': 'l'}
}

scott_chunk = {
    'scot':             {'format': '4s', 'data': b'scot'},
    'ckSize':           {'format': 'l', 'data': 424},
    'alter':            {'format': 'b', 'data': 0},                     # Padding
    'attrib':           {'format': 'B', 'data': 128},                   # ?
    'artnum':           {'format': 'h', 'data': 0},                     # Padding
    'title':            {'format': '43s', 'data': b' ' * 43},           # Title
    'cart':             {'format': '4s', 'data': b' ' * 4},             # Cart
    'padd':             {'format': 'c', 'data': b' '},                  # Padding
    'asclen':           {'format': '5s', 'data': b"99:99"},             # Duration of the audio
    'start_seconds':    {'format': 'h', 'data': 0},                     # INTRO
    'start_hundred':    {'format': 'h', 'data': 0},                     # INTRO
                                                                        # Intro and EOD are related.
                                                                        #
                                                                        #  marker          marker
                                                                        #    \/              \/
                                                                        # | INTRO | ----- | EOD |
                                                                        #             ^
                                                                        #     this length = eod
                                                                        #
    'end_seconds':      {'format': 'h', 'data': 9999},                  # EOD
    'end_hundred':      {'format': 'h', 'data': 9999},                  # EOD
    'start_date':       {'format': '6s', 'data': b"0" * 6},             # Expiry start date MMDDYY
    'kill_date':        {'format': '6s', 'data': b"9" * 6},             # Expiry end date MMDDYY
    'start_hour':       {'format': 'b', 'data': -128},                  # Expiry start hour (only the hour is used)
    'kill_hour':        {'format': 'b', 'data': -128},                  # Expiry end hour (only the hour is used)
    'digital':          {'format': 'c', 'data': b'A'},                  # Always 'A' = Analog
    'sampleRate':       {'format': 'h', 'data': 0},                     # From FMT Header
    'stereo':           {'format': 'c', 'data': b'S'},                  # From FMT Header
    'compression':      {'format': 'B', 'data': 10},                    # From FMT Header
    'eomstart':         {'format': 'l', 'data': 99},                    # SEC
    'eomlength':        {'format': 'h', 'data': 0},                     # SEC
    'attrib2':          {'format': 'L', 'data': 264},                   # ?
    'future1':          {'format': '12s', 'data': bytes([0] * 12)},     # padding..
    'cfcolo':           {'format': 'L', 'data': 0},                     # useless
    'ccolo':            {'format': 'L', 'data': 0},                     # useless
    'segeompos':        {'format': 'l', 'data': 0},                     # what does this do?
    'vtstartsec':       {'format': 'h', 'data': 0},                     # Padding
    'vtstarthun':       {'format': 'h', 'data': 0},                     # Padding
    'pcat':             {'format': '3s', 'data': b" " * 3},             # Padding
    'pcopy':            {'format': '4s', 'data': b" " * 4},             # Padding
    'ppadd':            {'format': 'c', 'data': b' '},                  # Padding
    'pocat':            {'format': '3s', 'data': b" " * 3},             # Padding
    'pocopy':           {'format': '4s', 'data': b" " * 4},             # Padding
    'popadd':           {'format': 'c', 'data': b' '},                  # Padding
    'hrcanplay':        {'format': '21s', 'data': bytes([255] * 21)},   # ?
    'future2':          {'format': '108s', 'data': bytes([0] *108)},    # Padding
    'artist':           {'format': '34s', 'data': b" " * 34},           # ?
    'trivia':           {'format': '34s', 'data': b" " * 34},           # ?
    'intro':            {'format': '2s', 'data': b" " * 2},             # Padding
    'end':              {'format': 'c', 'data': b' '},                  # Padding
    'year':             {'format': '4s', 'data': b" " * 4},             # ?
    'obsolete2':        {'format': 'c', 'data': bytes([0])},            # Padding
    'record_hour':      {'format': 'b', 'data': 0},                     # ?
    'record_date':      {'format': '6s', 'data': b" " * 6},             # ?
    'mpegrate':         {'format': 'h', 'data': 0},                     # Padding
    'pitch':            {'format': 'H', 'data': 32768},                 # Padding
    'playlevel':        {'format': 'H', 'data': 21845},                 # Padding
    'lenvalid':         {'format': 'B', 'data': 0},                     # Padding
    'filelength':       {'format': 'L', 'data': 0},                     # Padding
    'newplaylevel':     {'format': 'H', 'data': 33768},                 # Padding
    'chopsize':         {'format': 'L', 'data': 0},                     # Padding
    'vteomovr':         {'format': 'L', 'data': 0},                     # Padding
    'desiredlen':       {'format': 'L', 'data': 0},                     # Padding
    'triggers1':        {'format': 'L', 'data': 0},                     # Padding
    'triggers2':        {'format': 'L', 'data': 0},                     # Padding
    'triggers3':        {'format': 'L', 'data': 0},                     # Padding
    'category':         {'format': '4s', 'data': bytes([0] * 4)},       # Category
    'fillout':          {'format': '33s', 'data': bytes([0] * 33)},     # Padding
}

def generate_format(chunk: dict) -> str:
    format_string = '<'
    for k, v in chunk.items():
        format_string += v['format']

    size = calcsize(format_string)

    return format_string, size

