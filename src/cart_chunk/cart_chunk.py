import io
import struct
import pathlib
import wave

from datetime import datetime, timedelta

from .defines import *


class CartChunk:
    def __init__(self, filename: pathlib.Path) -> None:
        self.filename = filename
        self.wave_data: dict    = {}
        self.header = self.get_header()

        self.riff_data: dict    = {}
        self.fmt_data: dict     = {}
        self.data_meta: dict    = {}
        self.scott_data: dict   = {}
        self.data_end: int      = 0

        self.is_scott: bool     = False

    def get_header(self) -> io.BytesIO:
        with open(self.filename, 'rb') as fh:
            header = io.BytesIO(fh.read(512))

        with wave.open(str(self.filename), 'rb') as fh:
            self.wave_data['channels']      = fh.getnchannels()
            self.wave_data['sampleWidth']   = fh.getsampwidth()
            self.wave_data['framerate']     = fh.getframerate()
            self.wave_data['frames']        = fh.getnframes()
            self.wave_data['compression']   = fh.getcomptype()
            self.wave_data['compName']      = fh.getcompname()

        self.wave_data['duration'] = float("{:.2f}".format(self.wave_data['frames'] / self.wave_data['framerate']))

        return header

    def get_riff_data(self) -> None:
        f, s = generate_format(riff_chunk)
        d = struct.unpack(f, self.header.read(s))
        for field, data in zip(riff_chunk, d):
            self.riff_data[field] = data

        f, s = generate_format(fmt_chunk)
        d = struct.unpack(f, self.header.read(s))
        for field, data in zip(fmt_chunk, d):
            self.fmt_data[field] = data

        if self.fmt_data['fmtsize'] == 40:
            chunk = mpeg_chunk
        else:
            chunk = pcm_chunk

        f, s = generate_format(chunk)
        d = struct.unpack(f, self.header.read(s))
        for field, data in zip(chunk, d):
            self.fmt_data[field] = data

    def get_scott_data(self) -> None:
        self.header.seek(0)
        index = self.header.read().find(b'scot')
        if index != -1:
            self.is_scott = True
            f, s = generate_format(scott_chunk)
            self.header.seek(index)

            scott_data = struct.unpack(f, self.header.read(s))

            skip_fields = []
            #skip_fields.extend(range(9, 17, 1))

            for i, field, data in zip(range(len(scott_data)), scott_chunk, scott_data):
                if 'attrib' in field:
                    self.scott_data[field] = bin(data)
                elif i == 36:
                    self.scott_data['hrcanplay'] = [bin(x) for x in struct.unpack('@21B', data)]
                elif i in skip_fields:
                    pass
                elif 'future' in field:
                    pass
                elif i in [51, 52, 47, 48]:
                    self.scott_data[field] = bin(data)
                else:
                    self.scott_data[field] = data

        else:
            self.is_scott = False

    def get_data_size(self) -> None:
        self.header.seek(0)
        index = self.header.read().find(b'data')
        try:
            if index != -1:
                self.header.seek(index)
                f, s = generate_format(data_chunk)
                d = struct.unpack(f, self.header.read(s))
                for field, data in zip(data_chunk, d):
                    self.data_meta[field] = data

                with open(self.filename, 'rb') as fh:
                    fh.seek(self.header.tell())
                    self.audio = fh.read()
        except:
            raise

    def write_copy(self, artist, title):
        f, s = generate_format(riff_chunk)

        self.riff_data['size'] = self.data_meta['datasize'] + 470
        riff = struct.pack(f, *self.riff_data.values())
        f, s = generate_format(fmt_chunk | pcm_chunk)
        f += 'xx'
        self.fmt_data['fmtsize'] = 18
        #for k, v in new_mpeg_chunk.items():
        #    self.fmt_data[k] = 0

        fmt = struct.pack(f, *self.fmt_data.values())

        f, s = generate_format(data_chunk)
        data = struct.pack(f, *self.data_meta.values())

        for k, v in scott_chunk.items():
            self.scott_data[k] = v['data']

        self.scott_data['artist'] = artist.ljust(34).encode()
        self.scott_data['title'] = title.ljust(43).encode()
        if self.fmt_data['chan'] == 1:
            self.scott_data['stereo'] = b'M'
        elif self.fmt_data['chan'] == 2:
            self.scott_data['stereo'] = b'S'

        sec = datetime.strftime(datetime.strptime(f'{self.wave_data["duration"]:.2f}', '%S.%f'), '%M:%S')

        self.scott_data['asclen'] = sec.rjust(5).encode()
        self.scott_data['end_seconds'] = int(self.wave_data['duration'])
        self.scott_data['end_hundred'] = int((self.wave_data['duration'] % 1) * 100)
        self.scott_data['eomstart'] = int(self.wave_data['duration'] * 10)
        self.scott_data['eomlength'] = int(((self.wave_data['duration'] * 10) % 1) * 100)

        record_date = datetime.fromtimestamp(self.filename.stat().st_ctime)
        self.scott_data['record_date'] = datetime.strftime(record_date, "%y%m%d").encode()
        self.scott_data['record_hour'] = int(datetime.strftime(record_date, "%H")) - 128

        self.scott_data['sampleRate'] = int(self.fmt_data['sampleRate'] / 100)

        f, s = generate_format(scott_chunk)
        scott = struct.pack(f, *self.scott_data.values())

        with open('testNew.wav', 'wb') as fh:
            fh.write(riff)
            fh.write(fmt)
            fh.write(scott)
            fh.write(data)
            fh.write(self.audio)



    @staticmethod
    def convert_timestamp(date: str, hour_value: int) -> datetime:
        hour = hour_value + 128
        hours = f'{hour:02d}{0:02d}{0:02d}'
        date = date.decode('ascii')
        if int(date) == 0:
            timestamp = datetime.today() + timedelta(days = -99999)
        elif int(date) == 999999:
            timestamp = datetime.today() + timedelta(days = 99999)
        else:
            timestamp = datetime.strptime(f'{date}{hours}', '%m%d%y%H%M%S')
        return timestamp


