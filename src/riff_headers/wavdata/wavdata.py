import io
import struct
import pathlib

from datetime import datetime, timedelta

from . import *


class WavData:
    def __init__(self, filename: pathlib.Path) -> None:
        self.filename = filename
        self.header = self.get_header()

        self.riff_data: dict    = {}
        self.data_meta: dict    = {}
        self.scott_data: dict   = {}

        self.is_scott: bool     = False

    def get_header(self) -> io.BytesIO:
        with open(self.filename, 'rb') as fh:
            header = io.BytesIO(fh.read(512))

        return header

    def get_riff_data(self) -> None:
        def generate_riff(chunk: dict) -> None:
            f, s = generate_format(chunk)
            d = struct.unpack(f, self.header.read(s))
            for field, data in zip(chunk, d):
                self.riff_data[field] = data


        generate_riff(riff_chunk)
        generate_riff(fmt_chunk)

        if self.riff_data['fmtsize'] == 40:
            generate_riff(mpeg_chunk)
        else:
            generate_riff(pcm_chunk)

    def get_scott_data(self) -> None:
        self.header.seek(0)
        index = self.header.read().find(b'scot')
        if index != -1:
            self.is_scott = True
            f, s = generate_format(scott_chunk)
            self.header.seek(index)

            scott_data = struct.unpack(f, self.header.read(s))

            skip_fields = []
            skip_fields.extend(range(9, 17, 1))

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
                    self.scott_data[field] = i, data

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
        except:
            raise

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


