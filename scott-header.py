import click
import io
import struct

from datetime import datetime, timedelta

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
        self.file_size = 508

    def update_size(self, byte):
        self.file_size = self.file_size - byte
        return byte

    def get_data(self, data):
        index = data.find(b'data')
        if index != -1:
            return index + self.current_pos
        else:
            print('data not found')

    def get_data_meta(self):
        with io.open(self.filename, 'rb') as fh:
            fh.seek(self.data_index)
            data_tag, audio_length = struct.unpack('<4sl', fh.read(8))
            data_tag = data_tag.decode('ascii')
            self.audio_data = fh.read(audio_length)

        print(self.data_index)

        return data_tag, audio_length

    def create_copy(self):

        with io.open(self.filename, 'rb') as fh:
            header = fh.read(36)
            data = fh.read(8)

        with io.open('new.wav', 'wb') as fh:
            fh.write(header)
            fh.write(data)
            fh.write(self.audio_data)


    def get_scott(self, header):
        index = header.find(b'scot')
        if index != -1:
            return index + self.current_pos, True
        else:
            return '', False

    def get_scott_header(self):
        scott_data = {}
        with io.open(self.filename, 'rb+') as fh:
            fh.seek(self.current_pos)
            title = struct.unpack('<43p', fh.read(self.update_size(43)))[0]
            scott_data['title'] = title.decode('utf-8', 'ignore')

            cart, asclen  = struct.unpack('<xxx4sx5s', fh.read(self.update_size(13)))
            scott_data['cart'] = cart.decode('ascii')
            scott_data['asclen'] = asclen.decode('ascii')

            start_s, start_h, end_s, end_h = struct.unpack('<hhhh', fh.read(self.update_size(8)))
            scott_data['start_seconds'] = f'{start_s}.{start_h}'
            scott_data['end_seconds'] = f'{end_s}.{end_h}'

            kill_dates = struct.unpack('<6s6sBB', fh.read(self.update_size(14)))
            try:
                scott_data['start_time'] = convert_timestamp(kill_dates[0], kill_dates[2])
            except:
                scott_data['start_time'] = kill_dates[0], kill_dates[2]
            try:
                scott_data['end_time'] = convert_timestamp(kill_dates[1], kill_dates[3])
            except:
                scott_data['end_time'] = kill_dates[1], kill_dates[3]

            digital, sampleRate, stereo, compression = struct.unpack('<chcB', fh.read(self.update_size(5)))
            scott_data['digital'] = digital.decode('ascii')
            scott_data['sampleRate'] = sampleRate
            scott_data['stereo'] = stereo.decode('ascii')
            scott_data['compression'] = compression

            eomstart, eomlength = struct.unpack('<lH', fh.read(self.update_size(6)))
            scott_data['eomstart'] = eomstart
            scott_data['eomlength'] = eomlength

            self.attrs = print_hex(fh.read(self.update_size(32)))
            self.chuck = print_hex(fh.read(self.update_size(145)))
            artist, trivia = struct.unpack('<34s34s', fh.read(self.update_size(68)))
            scott_data['artist'] = artist.decode('utf-8')
            scott_data['trivia'] = trivia.decode('utf-8')

            #fh.write(b'00')
            intro, end = struct.unpack('<2ps', fh.read(self.update_size(3)))
            scott_data['intro'] = intro.decode('ascii')
            scott_data['end_type'] = end.decode('ascii')
            #print(self.file_size)
            self.eof = print_hex(fh.read(self.file_size - 4))

        return scott_data



    def read_header(self):
        header_data = {}
        extra_data = ""

        #with io.open(self.filename, 'rb') as fh:
        #    find_data = fh.read(550)
        #    self.data_index = self.get_data(find_data)

        with io.open(self.filename, 'rb') as fh:
            # Read the RIFF and fmt chunk
            riff_data = struct.unpack('<4sI4s4sIhhLLhh', fh.read(36))
            header_data['riff']         = riff_data[0].decode('ascii')
            header_data['size']         = riff_data[1]
            header_data['wave']         = riff_data[2].decode('ascii')
            header_data['fmt']          = riff_data[3].decode('ascii')
            header_data['fmtsize']      = riff_data[4]
            header_data['tag']          = riff_data[5]
            header_data['chan']         = riff_data[6]
            header_data['samplerate']   = riff_data[7]
            header_data['transfrate']   = riff_data[8]
            header_data['align']        = riff_data[9]
            header_data['bitspersamp']  = riff_data[10]
            self.current_pos = fh.tell()
            next_400 = fh.read(550)
            seek_scott, is_scott = self.get_scott(next_400)
            self.data_index = self.get_data(next_400)

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
@click.option('--create_copy', is_flag=True)
def cli(audio, create_copy):
    header_reader = HeaderReader(audio)
    header_data, is_scott = header_reader.read_header()
    for k, v in header_data.items():
        print(f'{k:<20}: {v}')

    data_tag, audio_length = header_reader.get_data_meta()
    print(f'{data_tag = }')
    print(f'{audio_length = }')
    if create_copy:
        header_reader.create_copy()

    if is_scott:
        scott_header = header_reader.get_scott_header()
        print(f'{"Scott Header":^30}')
        for k, v in scott_header.items():
            print(f'{k:<20}: {v}')

        #print(header_reader.attrs)
        #print(header_reader.chuck)
        print(header_reader.eof)

if __name__ == '__main__':
    cli()
