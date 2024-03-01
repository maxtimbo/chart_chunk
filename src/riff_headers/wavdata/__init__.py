scott_chunk_dict = {
    'scot': {
        'data_type': '4s',
        'default': b'scot'
    },
    'ckSize': {
        'data_type': 'l',
        'default': 424
    },
    'alter': {
        'data_type': 'b',
        'default': 0
    },
    'attrib': {
        'data_type': 'B',
        'default': int('10000000', 2)
    },
    'artnum': {
        'data_type': 'h',
        'default': 0
    },
    'title': {
        'data_type': '43s',
        'default': ''.ljust(43)[:43]
    },
    'cart': {
        'data_type': '4s',
        'default': ''.ljust(4)[:4]
    },
    'padd': {
        'data_type': 'c',
        'default': ' '
    },
    'asclen': {
        'data_type': '5s',
        'default': ' 0:00'.rjust(5)[:5]
    },
    'start_seconds': {
        'data_type': 'h',
    },
    'start_hundred': {
        'data_type': 'h'
    },
    'end_seconds': {
        'data_type': 'h'
    },
    'end_hundred': {
        'data_type': 'h'
    },
    'start_date': {
        'data_type': '6s'
    },
    'kill_date': {
        'data_type': '6s'
    },
    'start_hour': {
        'data_type': 'b'
    },
    'kill_hour': {
        'data_type': 'b'
    },
    'digital': {
        'data_type': 'c'
    },
    'sampleRate': {
        'data_type': 'h'
    },
    'stereo': {
        'data_type': 'c'
    },
    'compression': {
        'data_type': 'B'
    },
    'eomstart': {
        'data_type': 'l'
    },
    'eomlength': {
        'data_type': 'h'
    },
    'attrib2': {
        'data_type': 'L'
    },
    'future1': {
        'data_type': '12s'
    },
    'cfcolo': {
        'data_type': 'L'
    },
    'ccolo': {
        'data_type': 'L'
    },
    'segeompos': {
        'data_type': 'l'
    },
    'vtstartsec': {
        'data_type': 'h'
    },
    'vtstarthun': {
        'data_type': 'h'
    },
    'pcat': {
        'data_type': '3s'
    },
    'pcopy': {
        'data_type': '4s'
    },
    'ppadd': {
        'data_type': 'c'
    },
    'pocat': {
        'data_type': '3s'
    },
    'pocopy': {
        'data_type': '4s'
    },
    'popadd': {
        'data_type': 'c'
    },
    'hrcanplay': {
        'data_type': '21B'
    },
    'future2': {
        'data_type': '108s'
    },
    'artist': {
        'data_type': '34s'
    },
    'trivia': {
        'data_type': '34s'
    },
    'intro': {
        'data_type': '2s'
    },
    'end': {
        'data_type': 'c'
    },
    'year': {
        'data_type': '4s'
    },
    'obsolete2': {
        'data_type': 'c'
    },
    'record_hour': {
        'data_type': 'b'
    },
    'record_date': {
        'data_type': '6s'
    },
    'mpegrate': {
        'data_type': 'h'
    },
    'pitch': {
        'data_type': 'H'
    },
    'playlevel': {
        'data_type': 'H'
    },
    'lenvalid': {
        'data_type': 'B'
    },
    'filelength': {
        'data_type': 'L'
    },
    'newplaylevel': {
        'data_type': 'H'
    },
    'chopsize': {
        'data_type': 'L'
    },
    'vteomovr': {
        'data_type': 'L'
    },
    'desiredlen': {
        'data_type': 'L'
    },
    'triggers': {
        'data_type': '3L'
    },
    'category': {
        'data_type': '4s'
    },
    'fillout': {
        'data_type': '33s'
    },
}

def generate_scott_format():
    format_string = '<'
    for k, v in scott_chunk_dict.items():
        format_string += v['data_type']

    return format_string
