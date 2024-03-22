import io
import struct
import pathlib
import wave

import numpy as np

from dataclasses import dataclass, field
from datetime import datetime, timedelta

try:
    from defines import *
except:
    from .defines import *


@dataclass
class NewCart:
    filename: pathlib.Path
    artist: str                 = None
    title: str                  = None
    trivia: str                 = None
    year: int                   = None
    category: str               = None
    cart: str                   = None
    intro: float                = None
    sec: float                  = None
    eom: float                  = None
    start_timestamp: tuple      = None
    end_timestamp: tuple        = None
    hrcanplay: list[list[int]]  = field(default_factory = lambda: [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ])


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
        self.is_bext: bool      = False
        self.get_riff_data()
        self.get_bext_data()
        self.get_scott_data()
        self.get_data_size()

    def get_header(self, header_size: int = 512) -> io.BytesIO:
        with open(self.filename, 'rb') as fh:
            header = io.BytesIO(fh.read(header_size))

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

    def get_bext_data(self) -> None:
        self.header.seek(0)
        index = self.header.read().find(b'bext')
        if index != -1:
            self.is_bext = True
            self.header.seek(index)
            fstring = '<4sl'
            bext_meta = struct.unpack(fstring, self.header.read(struct.calcsize(fstring)))
            self.header = self.get_header(512 + bext_meta[1])

    def get_scott_data(self) -> None:
        self.header.seek(0)
        index = self.header.read().find(b'scot')
        if index != -1:
            self.is_scott = True
            f, s = generate_format(scott_chunk)
            self.header.seek(index)

            scott_data = struct.unpack(f, self.header.read(s))

            for i, field, data in zip(range(len(scott_data)), scott_chunk, scott_data):
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

    def write_copy(self, new_file: NewCart) -> pathlib.Path:
        f, s = generate_format(riff_chunk)

        self.riff_data['size'] = self.data_meta['datasize'] + 470
        riff = struct.pack(f, *self.riff_data.values())
        f, s = generate_format(fmt_chunk | pcm_chunk)
        f += 'xx'
        self.fmt_data['fmtsize'] = 18

        fmt = struct.pack(f, *self.fmt_data.values())

        f, s = generate_format(data_chunk)
        data = struct.pack(f, *self.data_meta.values())

        for k, v in scott_chunk.items():
            self.scott_data[k] = v['data']

        if new_file.artist is not None:
            if len(new_file.artist) > 34:
                raise
            else:
                self.scott_data['artist'] = new_file.artist.ljust(34).encode()

        if new_file.title is not None:
            if len(new_file.title) > 43:
                raise
            else:
                self.scott_data['title'] = new_file.title.ljust(43).encode()

        if new_file.trivia is not None:
            if len(new_file.trivia) > 34:
                raise
            else:
                self.scott_data['trivia'] = new_file.trivia.ljust(34).encode()

        if new_file.year is not None:
            if len(str(new_file.year)) > 4:
                raise
            else:
                self.scott_data['year'] = str(new_file.year).ljust(4).encode()

        if new_file.cart is not None:
            if len(new_file.cart) > 4:
                raise
            else:
                self.scott_data['cart'] = new_file.cart.encode()

        if new_file.category is not None:
            if len(new_file.category) > 4:
                raise
            else:
                self.scott_data['category'] = new_file.category.encode()

        duration = datetime.strftime(
            datetime.strptime(
                str(timedelta(seconds = self.wave_data['duration'])),
                '%H:%M:%S.%f'),
                '%M:%S')
        self.scott_data['asclen'] = duration.rjust(5).encode()

        # intro int
        if new_file.intro is not None:
            if new_file.intro > self.wave_data['duration']:
                raise
            else:
                self.scott_data['start_seconds'] = int(new_file.intro)
                self.scott_data['start_hundred'] = int((new_file.intro % 1) * 100)

        # sec float
        if new_file.sec is not None:
            if new_file.sec > self.wave_data['duration']:
                raise
            else:
                self.scott_data['eomstart'] = int(new_file.sec * 10)
                self.scott_data['eomlength'] = int(((new_file.sec * 10) % 1) * 100)
        else:
            self.scott_data['eomstart'] = int(self.wave_data['duration'] * 10)
            self.scott_data['eomlength'] = int(((self.wave_data['duration'] * 10) % 1) * 100)

        # eom float
        if new_file.eom is not None:
            if new_file.eom > self.wave_data['duration']:
                raise
            else:
                self.scott_data['end_seconds'] = int(new_file.eom)
                self.scott_data['end_hundred'] = int((new_file.eom % 1) * 100)
        else:
            self.scott_data['end_seconds'] = int(self.wave_data['duration'])
            self.scott_data['end_hundred'] = int((self.wave_data['duration'] % 1) * 100)


        if new_file.start_timestamp is not None:
            self.scott_data['start_date'] = str(new_file.start_timestamp[0]).encode()
            self.scott_data['start_hour'] = new_file.start_timestamp[1] - 128

        if new_file.end_timestamp is not None:
            self.scott_data['kill_date'] = str(new_file.end_timestamp[0]).encode()
            self.scott_data['kill_hour'] = new_file.end_timestamp[1] - 128

        self.scott_data['hrcanplay'] = bytes(np.packbits(new_file.hrcanplay, bitorder = 'big'))

        self.scott_data['sampleRate'] = int(self.fmt_data['sampleRate'] / 100)

        if self.fmt_data['chan'] == 1:
            self.scott_data['stereo'] = b'M'
        elif self.fmt_data['chan'] == 2:
            self.scott_data['stereo'] = b'S'

        record_date = datetime.fromtimestamp(self.filename.stat().st_ctime)
        self.scott_data['record_date'] = datetime.strftime(record_date, "%y%m%d").encode()
        self.scott_data['record_hour'] = int(datetime.strftime(record_date, "%H")) - 128


        f, s = generate_format(scott_chunk)
        scott = struct.pack(f, *self.scott_data.values())

        if new_file.category is not None and new_file.cart is not None:
            cart_file = pathlib.Path(new_file.filename.parents[0], new_file.category + new_file.cart + '.wav')
        else:
            cart_file = new_file.filename

        with open(cart_file, 'wb') as fh:
            fh.write(riff)
            fh.write(fmt)
            fh.write(scott)
            fh.write(data)
            fh.write(self.audio)

        return cart_file

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


