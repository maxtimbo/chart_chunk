from struct import calcsize

__all__ = [
    'riff_chunk',
    'fmt_chunk',
    'pcm_chunk',
    'mpeg_chunk',
    'scott_chunk',
    'fact_chunk',
    'data_chunk',
    'generate_format'
]

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
    'extra':            {'format': 'h'},
    'layer':            {'format': 'h'},
    'bitrate':          {'format': 'l'},
    'mode':             {'format': 'h'},
    'extmode':          {'format': 'h'},
    'emphasis':         {'format': 'h'},
    'flags':            {'format': 'h'},
    'PTSlow':           {'format': 'l'},
    'PTShigh':          {'format': 'l'}
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
    'scot':             {'format': '4s'},
    'ckSize':           {'format': 'l'},
    'alter':            {'format': 'b'},
    'attrib':           {'format': 'B'},
    'artnum':           {'format': 'h'},
    'title':            {'format': '43s'},
    'cart':             {'format': '4s'},
    'padd':             {'format': 'c'},
    'asclen':           {'format': '5s'},
    'start_seconds':    {'format': 'h',},
    'start_hundred':    {'format': 'h'},
    'end_seconds':      {'format': 'h'},
    'end_hundred':      {'format': 'h'},
    'start_date':       {'format': '6s'},
    'kill_date':        {'format': '6s'},
    'start_hour':       {'format': 'b'},
    'kill_hour':        {'format': 'b'},
    'digital':          {'format': 'c'},
    'sampleRate':       {'format': 'h'},
    'stereo':           {'format': 'c'},
    'compression':      {'format': 'B'},
    'eomstart':         {'format': 'l'},
    'eomlength':        {'format': 'h'},
    'attrib2':          {'format': 'L'},
    'future1':          {'format': '12s'},
    'cfcolo':           {'format': 'L'},
    'ccolo':            {'format': 'L'},
    'segeompos':        {'format': 'l'},
    'vtstartsec':       {'format': 'h'},
    'vtstarthun':       {'format': 'h'},
    'pcat':             {'format': '3s'},
    'pcopy':            {'format': '4s'},
    'ppadd':            {'format': 'c'},
    'pocat':            {'format': '3s'},
    'pocopy':           {'format': '4s'},
    'popadd':           {'format': 'c'},
    'hrcanplay':        {'format': '21s'},
    'future2':          {'format': '108s'},
    'artist':           {'format': '34s'},
    'trivia':           {'format': '34s'},
    'intro':            {'format': '2s'},
    'end':              {'format': 'c'},
    'year':             {'format': '4s'},
    'obsolete2':        {'format': 'c'},
    'record_hour':      {'format': 'b'},
    'record_date':      {'format': '6s'},
    'mpegrate':         {'format': 'h'},
    'pitch':            {'format': 'H'},
    'playlevel':        {'format': 'H'},
    'lenvalid':         {'format': 'B'},
    'filelength':       {'format': 'L'},
    'newplaylevel':     {'format': 'H'},
    'chopsize':         {'format': 'L'},
    'vteomovr':         {'format': 'L'},
    'desiredlen':       {'format': 'L'},
    'triggers1':        {'format': 'L'},
    'triggers2':        {'format': 'L'},
    'triggers3':        {'format': 'L'},
    'category':         {'format': '4s'},
    'fillout':          {'format': '33s'},
}

def generate_format(chunk: dict) -> str:
    format_string = '<'
    for k, v in chunk.items():
        format_string += v['format']

    size = calcsize(format_string)

    return format_string, size
