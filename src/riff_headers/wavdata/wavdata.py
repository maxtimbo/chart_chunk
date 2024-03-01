import io
import struct
import pathlib

from datetime import datetime, timedelta


class WavData:
    def __init__(self, filename: pathlib.Path) -> None:
        self.filename = filename

        self.riff_fmt_end: int
        self.data_position: int
        self.scott_begin: int
        self.scott_end: int
        self.scott_end_fillout: int

        self.riff_data: dict    = {}
        self.data_meta: dict    = {}
        self.scott_data: dict   = {}

        self.is_scott: bool     = False

    def get_riff_data(self):
        with io.open(self.filename, 'rb') as fh:
            riff_data = struct.unpack('<4sl4s4slhhllhh', fh.read(36))
            self.riff_data['riff']         = riff_data[0].decode('ascii')
            self.riff_data['size']         = riff_data[1]
            self.riff_data['wave']         = riff_data[2].decode('ascii')
            self.riff_data['fmt']          = riff_data[3].decode('ascii')
            self.riff_data['fmtsize']      = riff_data[4]
            self.riff_data['tag']          = riff_data[5]
            self.riff_data['chan']         = riff_data[6]
            self.riff_data['samplerate']   = riff_data[7]
            self.riff_data['transfrate']   = riff_data[8]
            self.riff_data['align']        = riff_data[9]
            self.riff_data['bitspersamp']  = riff_data[10]
            self.riff_fmt_end = fh.tell()
            search_bytes = fh.read(550)
            self.get_data_size(search_bytes)
            self.get_scott_data(search_bytes)

    def get_mpeg_data(self):
        with io.open(self.filename, 'rb') as fh:
            fh.seek(self.riff_fmt_end)
            mpeg = struct.unpack('<2hl4h2l', fh.read(24))
            self.riff_data['extra']     = mpeg[0]
            self.riff_data['layer']     = mpeg[1]
            self.riff_data['bitrate']   = mpeg[2]
            self.riff_data['mode']      = mpeg[3]
            self.riff_data['extmode']   = mpeg[4]
            self.riff_data['emphasis']  = mpeg[5]
            self.riff_data['flags']     = mpeg[6]
            self.riff_data['PTSlow']    = mpeg[7]
            self.riff_data['PTShigh']   = mpeg[8]

    def get_scott_data(self, search_bytes):
        index = search_bytes.find(b'scot')
        if index != -1:
            self.is_scott = True
            self.scott_begin = index + self.riff_fmt_end
            if self.scott_begin - self.riff_fmt_end == 24:
                self.get_mpeg_data()
            with io.open(self.filename, 'rb') as fh:
                fh.seek(self.scott_begin)
                scott_data = struct.unpack(
                    '<4slB43p3p4sc5shhhh6s6sbbchcBlHL12sLLlhh3s4sc3s4sc21s108s34s34s2sc4scb6sHHBLH3L',
                    fh.read(381)
                )
                self.scott_data['scott']        = scott_data[0].decode('ascii')
                self.scott_data['cksize']       = scott_data[1]
                self.scott_data['attrib']       = bin(scott_data[2])
                self.scott_data['title']        = scott_data[3].decode('utf-8', 'ignore')
                self.scott_data['unknown1']     = scott_data[4]
                self.scott_data['cart']         = scott_data[5].decode('ascii')
                self.scott_data['padd']         = scott_data[6]
                self.scott_data['asclen']       = scott_data[7].decode('ascii')
                self.scott_data['start_seconds']= f'{scott_data[8]}.{scott_data[9]}'
                self.scott_data['end_seconds']  = f'{scott_data[10]}.{scott_data[11]}'
                self.scott_data['start_time']   = self.convert_timestamp(
                        scott_data[12],
                        scott_data[14]
                )
                self.scott_data['end_time']     = self.convert_timestamp(
                        scott_data[13],
                        scott_data[15]
                )
                self.scott_data['digital']      = scott_data[16].decode('ascii')
                self.scott_data['sampleRate']   = scott_data[17]
                self.scott_data['stereo']       = scott_data[18].decode('ascii')
                self.scott_data['compression']  = scott_data[19]
                self.scott_data['eomstart']     = scott_data[20]
                self.scott_data['eomlength']    = scott_data[21]
                self.scott_data['attrib2']      = bin(scott_data[22])
                self.scott_data['future1']       = scott_data[23]
                self.scott_data['cfcolo']       = scott_data[24]
                self.scott_data['ccolo']        = scott_data[25]
                self.scott_data['segeompos']    = scott_data[26]
                self.scott_data['vtstartsec']   = scott_data[27]
                self.scott_data['vtstarthun']   = scott_data[28]
                self.scott_data['pcat']         = scott_data[29]
                self.scott_data['pcopy']        = scott_data[30]
                self.scott_data['ppadd']        = scott_data[31]
                self.scott_data['pocat']        = scott_data[32]
                self.scott_data['pocopy']       = scott_data[33]
                self.scott_data['popadd']       = scott_data[34]
                self.scott_data['hrcanplay']    = "returns 168 b'1'"
                self.scott_data['future2']      = scott_data[36].decode('ascii')
                self.scott_data['artist']       = scott_data[37].decode('ascii')
                self.scott_data['trivia']       = scott_data[38].decode('ascii')
                self.scott_data['intro']        = scott_data[39].decode('ascii')
                self.scott_data['end']          = scott_data[40].decode('ascii')
                self.scott_data['year']         = scott_data[41].decode('ascii')
                self.scott_data['obsolete2']    = scott_data[42]
                self.scott_data['recorded']     = self.convert_timestamp(
                        scott_data[44],
                        scott_data[43]
                )
                self.scott_data['pitch']        = bin(scott_data[45])
                self.scott_data['playlevel']    = bin(scott_data[46])
                self.scott_data['lenvalid']     = scott_data[47]
                self.scott_data['filelength']   = scott_data[48]
                self.scott_data['newplaylevel'] = scott_data[49]
                self.scott_data['chopsize']     = scott_data[50]
                self.scott_data['vteomovr']     = scott_data[51]
                self.scott_data['desiredlen']   = scott_data[52]
                self.scott_end = fh.tell()
                scraps = struct.unpack('<14s3s16s18s', fh.read(51))
                self.scott_data['fillout1']     = scraps[0]
                self.scott_data['category']     = scraps[1]
                self.scott_data['fillout2']     = scraps[2]
                self.scott_data['fillout3']     = scraps[3]
                self.scott_end_fillout = fh.tell()
                till_data = self.data_position - self.scott_end_fillout
                if till_data == 12:
                    fact_chunk = struct.unpack(f'<4sll', fh.read(till_data))
                    self.scott_data['fact_chunk']   = fact_chunk[0]
                    self.scott_data['fact_size']    = fact_chunk[1]
                    self.scott_data['numsamples']   = fact_chunk[2]

        else:
            self.is_scott = False

    def get_data_size(self, search_bytes):
        index = search_bytes.find(b'data')
        try:
            if index != -1:
                self.data_position = index + self.riff_fmt_end
                with io.open(self.filename, 'rb') as fh:
                    fh.seek(self.data_position)
                    data, audio_length = struct.unpack('<4sl', fh.read(8))
                    self.data_meta['tag'] = data.decode('ascii')
                    self.data_meta['length'] = audio_length
                    self.audio_raw = fh.read(audio_length)
        except:
            raise

    #def write_artist_title(self, new_file: pathlib.Path, artist: str, title: str):
    #    riff_chunk = struct.pack()
    #    data_chunk = struck.pack()

    #def compile_scott(self, artist: str, title: str):
    #    scott_chunk = struck.pack(
    #        '<4slB43p3p4sc5shhhh6s6sbbchcBlHL12sLLlhh3s4sc3s4sc21s108s34s34s2sc4scb6sHHBLH3L',


    @staticmethod
    def convert_timestamp(date, hour_value):
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


