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

            #self.scott_begin = index + self.riff_fmt_end

            #with io.open(self.filename, 'rb') as fh:
            #    fh.seek(self.scott_begin)
            #    scott_data = struct.unpack(
            #        generate_format(scott_chunk),
            #        fh.read(432)
            #    )
            #    self.scott_data['scott']        = scott_data[0].decode('ascii')
            #    self.scott_data['cksize']       = scott_data[1]
            #    self.scott_data['alter']        = scott_data[2]
            #    self.scott_data['attrib']       = bin(scott_data[3])
            #    self.scott_data['artnum']       = scott_data[4]
            #    self.scott_data['title']        = scott_data[5].decode('ascii')
            #    self.scott_data['cart']         = scott_data[6].decode('ascii')
            #    self.scott_data['padd']         = scott_data[7]
            #    self.scott_data['asclen']       = scott_data[8].decode('ascii')
            #    self.scott_data['start_seconds']= f'{scott_data[9]}.{scott_data[10]}'
            #    self.scott_data['end_seconds']  = f'{scott_data[11]}.{scott_data[12]}'
            #    self.scott_data['start_time']   = self.convert_timestamp(
            #            scott_data[13],
            #            scott_data[15]
            #    )
            #    self.scott_data['end_time']     = self.convert_timestamp(
            #            scott_data[14],
            #            scott_data[16]
            #    )
            #    self.scott_data['digital']      = scott_data[17].decode('ascii')
            #    self.scott_data['sampleRate']   = scott_data[18]
            #    self.scott_data['stereo']       = scott_data[19].decode('ascii')
            #    self.scott_data['compression']  = scott_data[20]
            #    self.scott_data['eomstart']     = scott_data[21]
            #    self.scott_data['eomlength']    = scott_data[22]
            #    self.scott_data['attrib2']      = bin(scott_data[23])
            #    self.scott_data['future1']      = scott_data[24]
            #    self.scott_data['cfcolo']       = scott_data[25]
            #    self.scott_data['ccolo']        = scott_data[26]
            #    self.scott_data['segeompos']    = scott_data[27]
            #    self.scott_data['vtstartsec']   = scott_data[28]
            #    self.scott_data['vtstarthun']   = scott_data[29]
            #    self.scott_data['pcat']         = scott_data[30]
            #    self.scott_data['pcopy']        = scott_data[31]
            #    self.scott_data['ppadd']        = scott_data[32]
            #    self.scott_data['pocat']        = scott_data[33]
            #    self.scott_data['pocopy']       = scott_data[34]
            #    self.scott_data['popadd']       = scott_data[35]
            #    self.scott_data['hrcanplay']    = ''
            #    for x in range(36, 36 + 21, 1):
            #        self.scott_data['hrcanplay'] += str(scott_data[x])
            #    self.scott_data['future2']      = scott_data[57]
            #    self.scott_data['artist']       = scott_data[58]
            #    self.scott_data['trivia']       = scott_data[59]
            #    self.scott_data['intro']        = scott_data[60]
            #    self.scott_data['end']          = scott_data[61]
            #    self.scott_data['year']         = scott_data[62]
            #    self.scott_data['obsolete2']    = scott_data[63]
            #    self.scott_data['recorded']     = self.convert_timestamp(
            #            scott_data[65],
            #            scott_data[64]
            #    )
            #    self.scott_data['mpegrate']     = scott_data[66]
            #    self.scott_data['pitch']        = bin(scott_data[67])
            #    self.scott_data['playlevel']    = bin(scott_data[68])
            #    self.scott_data['lenvalid']     = scott_data[69]
            #    self.scott_data['filelength']   = scott_data[70]
            #    self.scott_data['newplaylevel'] = scott_data[71]
            #    self.scott_data['chopsize']     = scott_data[72]
            #    self.scott_data['vteomovr']     = scott_data[73]
            #    self.scott_data['desiredlen']   = scott_data[74]
            #    self.scott_data['triggers']     = scott_data[75], scott_data[76], scott_data[77]
            #    self.scott_data['category']     = scott_data[78]
            #    self.scott_data['fillout']      = scott_data[79]
            #    self.scott_end = fh.tell()
            #    till_data = self.data_position - self.scott_end
            #    if till_data == 12:
            #        fact_chunk = struct.unpack(f'<4sll', fh.read(till_data))
            #        self.scott_data['fact_chunk']   = fact_chunk[0]
            #        self.scott_data['fact_size']    = fact_chunk[1]
            #        self.scott_data['numsamples']   = fact_chunk[2]

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

                #with io.open(self.filename, 'rb') as fh:
                #    fh.seek(self.data_position)
                #    data, audio_length = struct.unpack('<4sl', fh.read(8))
                #    self.data_meta['tag'] = data.decode('ascii')
                #    self.data_meta['length'] = audio_length
                #    self.audio_raw = fh.read(audio_length)
        except:
            raise

    #def write_artist_title(self, new_file: pathlib.Path, artist: str, title: str):
    #    riff_chunk = struct.pack()
    #    data_chunk = struck.pack()

    #def compile_scott(self, artist: str, title: str):
    #    scott_chunk = struck.pack(
    #        '<4slB43p3p4sc5shhhh6s6sbbchcBlHL12sLLlhh3s4sc3s4sc21s108s34s34s2sc4scb6sHHBLH3L',


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


