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
    'scot':             {'format': '4s', 'data': b'scot'},          # ?
    'ckSize':           {'format': 'l', 'data': 424},               # ?
    'alter':            {'format': 'b', 'data': 0},                 # ?
    'attrib':           {'format': 'B', 'data': 128},               # ?
    'artnum':           {'format': 'h', 'data': 0},                 # ?
    'title':            {'format': '43s', 'data': b' ' * 43},       # ?
    'cart':             {'format': '4s', 'data': b' ' * 4},         # ?
    'padd':             {'format': 'c', 'data': b' '},              # ?
    'asclen':           {'format': '5s', 'data': b"99:99"},         # SEC Tone? MM:SS
    'start_seconds':    {'format': 'h', 'data': 0},                 # ?
    'start_hundred':    {'format': 'h', 'data': 0},                 # ?
    'end_seconds':      {'format': 'h', 'data': 9999},              # ?
    'end_hundred':      {'format': 'h', 'data': 9999},              # ?
    'start_date':       {'format': '6s', 'data': b"0" * 6},         # ?
    'kill_date':        {'format': '6s', 'data': b"9" * 6},         # ?
    'start_hour':       {'format': 'b', 'data': -128},              # ?
    'kill_hour':        {'format': 'b', 'data': -128},              # ?
    'digital':          {'format': 'c', 'data': b'A'},              # ?
    'sampleRate':       {'format': 'h', 'data': 0},                 # ?
    'stereo':           {'format': 'c', 'data': b'S'},              # ?
    'compression':      {'format': 'B', 'data': 10},                # ?
    'eomstart':         {'format': 'l', 'data': 99},                # ?
    'eomlength':        {'format': 'h', 'data': 0},                 # ?
    'attrib2':          {'format': 'L', 'data': 264},               # ? 
    'future1':          {'format': '12s', 'data': bytes([0] * 12)}, # ?
    'cfcolo':           {'format': 'L', 'data': 0},                 # ? 
    'ccolo':            {'format': 'L', 'data': 0},                 # ?
    'segeompos':        {'format': 'l', 'data': 0},                 # ?
    'vtstartsec':       {'format': 'h', 'data': 0},
    'vtstarthun':       {'format': 'h', 'data': 0},
    'pcat':             {'format': '3s', 'data': b" " * 3},
    'pcopy':            {'format': '4s', 'data': b" " * 4},
    'ppadd':            {'format': 'c', 'data': b' '},
    'pocat':            {'format': '3s', 'data': b" " * 3},
    'pocopy':           {'format': '4s', 'data': b" " * 4},
    'popadd':           {'format': 'c', 'data': b' '},
    'hrcanplay':        {'format': '21s', 'data': bytes([255] * 21)},
    'future2':          {'format': '108s', 'data': bytes([0] *108)},
    'artist':           {'format': '34s', 'data': b" " * 34},
    'trivia':           {'format': '34s', 'data': b" " * 34},
    'intro':            {'format': '2s', 'data': b" " * 2},
    'end':              {'format': 'c', 'data': b' '},
    'year':             {'format': '4s', 'data': b" " * 4},
    'obsolete2':        {'format': 'c', 'data': bytes([0])},
    'record_hour':      {'format': 'b', 'data': 0},
    'record_date':      {'format': '6s', 'data': b" " * 6},
    'mpegrate':         {'format': 'h', 'data': 0},
    'pitch':            {'format': 'H', 'data': 32768},
    'playlevel':        {'format': 'H', 'data': 21845},
    'lenvalid':         {'format': 'B', 'data': 0},
    'filelength':       {'format': 'L', 'data': 0},
    'newplaylevel':     {'format': 'H', 'data': 33768},
    'chopsize':         {'format': 'L', 'data': 0},
    'vteomovr':         {'format': 'L', 'data': 0},
    'desiredlen':       {'format': 'L', 'data': 0},
    'triggers1':        {'format': 'L', 'data': 0},
    'triggers2':        {'format': 'L', 'data': 0},
    'triggers3':        {'format': 'L', 'data': 0},
    'category':         {'format': '4s', 'data': b" " * 4},
    'fillout':          {'format': '33s', 'data': bytes([0] * 33)},
}

def generate_format(chunk: dict) -> str:
    format_string = '<'
    for k, v in chunk.items():
        format_string += v['format']

    size = calcsize(format_string)

    return format_string, size

