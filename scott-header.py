import struct
import io
from io import BytesIO
from datetime import datetime, timedelta
import click

def print_hex(data):
    hex_data = ' '.join(f'{byte:02X}' for byte in data)
    return f'Raw Data:\n{data}\nHex Data:\n{hex_data}\n'

def convert_timestamp(date, byte_value):
    date = date.decode('ascii')

    if byte_value >= 128:
        hour = byte_value - 128
    else:
        hour = byte_value

    minute = 0
    second = 0
    total_time = f'{hour:02d}:{minute:02d}:{second:02d}'

    if int(date) == 0:
        timestamp = datetime.today() + timedelta(days = -99999)
    elif int(date) == 999999:
        timestamp = datetime.today() + timedelta(days = 99999)
    else:
        timestamp = datetime.strptime(f'{date}{total_time}', '%m%d%y%H:%M:%S')
    return timestamp


class HeaderReader:
    def __init__(self, filename):
        self.filename = filename
        self.current_pos: int

    def get_scott(self, header):
        index = header.find(b'scot')
        if index != -1:
            print(f'{index + self.current_pos = }')
            return index + self.current_pos, True
        else:
            return '', False

    def get_scott_header(self):
        scott_data = {}
        print(self.current_pos)
        with io.open(self.filename, 'rb+') as fh:
            fh.seek(self.current_pos)
            title = struct.unpack('<43p', fh.read(43))[0]
            scott_data['title'] = title.decode('utf-8', 'ignore')

            cart, asclen  = struct.unpack('<xxx4sx5s', fh.read(13))
            scott_data['cart'] = cart.decode('ascii')
            scott_data['asclen'] = asclen.decode('ascii')

            start_s, start_h, end_s, end_h = struct.unpack('<hhhh', fh.read(8))
            scott_data['start_seconds'] = f'{start_s}.{start_h}'
            scott_data['end_seconds'] = f'{end_s}.{end_h}'

            kill_dates = struct.unpack('<6s6sBB', fh.read(14))
            try:
                scott_data['start_time'] = convert_timestamp(kill_dates[0], kill_dates[2])
            except:
                scott_data['start_time'] = kill_dates[0], kill_dates[2]
            try:
                scott_data['end_time'] = convert_timestamp(kill_dates[1], kill_dates[3])
            except:
                scott_data['end_time'] = kill_dates[1], kill_dates[3]

            digital, sampleRate, stereo, compression = struct.unpack('<chcB', fh.read(5))
            scott_data['digital'] = digital.decode('ascii')
            scott_data['sampleRate'] = sampleRate
            scott_data['stereo'] = stereo.decode('ascii')
            scott_data['compression'] = compression

            eomstart, eomlength = struct.unpack('<lH', fh.read(6))
            scott_data['eomstart'] = eomstart
            scott_data['eomlength'] = eomlength
            ##extra_data = print_hex(fh.read(6))

            attrs = fh.read(32)
            #attr_flags = struct.unpack('<I', attrs)
            #header_data['attr_flags'] = attr_flags
            chuck = fh.read(145)
            artist, trivia = struct.unpack('<34s34s', fh.read(68))
            scott_data['artist'] = artist.decode('utf-8')
            scott_data['trivia'] = trivia.decode('utf-8')

            #fh.write(b'00')
            intro, end = struct.unpack('<2ps', fh.read(3))
            scott_data['intro'] = intro.decode('ascii')
            scott_data['end_type'] = end.decode('ascii')

        return scott_data



    def read_header(self):
        header_data = {}
        extra_data = ""

        with io.open(self.filename, 'rb') as fh:
            # Read the RIFF chunk
            riff, size, wave = struct.unpack('<4sI4s', fh.read(12))
            header_data['riff'] = riff.decode('ascii')
            header_data['size'] = f'{size / (1024*1024):.2f}M'
            header_data['wave'] = wave.decode('ascii')

            # Read the fmt chunk
            fmt, fmtsize = struct.unpack('<4sI', fh.read(8))
            header_data['fmt'] = fmt.decode('ascii')
            header_data['fmtsize'] = fmtsize

            # Read the fmtdata for PCM
            pcm_data = struct.unpack('<hhLLhh', fh.read(16))
            header_data['tag'] = pcm_data[0]
            header_data['chan'] = pcm_data[1]
            header_data['samplerate'] = pcm_data[2]
            header_data['transfrate'] = pcm_data[3]
            header_data['align'] = pcm_data[4]
            header_data['bitspersamp'] = pcm_data[5]
            self.current_pos = fh.tell()
            next_400 = fh.read(400)
            seek_scott, is_scott = self.get_scott(next_400)

        if is_scott:
            with io.open(self.filename, 'rb') as fh:
                fh.seek(seek_scott)
                # Read the scot chunk
                scott_header, ckSize = struct.unpack('<4slx', fh.read(9))
                header_data['scott'] = scott_header.decode('ascii')
                header_data['ckSize'] = ckSize
                if ckSize != 424:
                    is_scott = False
                else:
                    self.current_pos = fh.tell()

        return header_data, is_scott

@click.command()
@click.argument('audio', type=click.Path(exists=True))
def cli(audio):
    header_reader = HeaderReader(audio)
    header_data, is_scott = header_reader.read_header()
    for k, v in header_data.items():
        print(f'{k:<20}: {v}')

    if is_scott:
        scott_header = header_reader.get_scott_header()
        print(f'{"Scott Header":^30}')
        for k, v in scott_header.items():
            print(f'{k:<20}: {v}')

if __name__ == '__main__':
    cli()
