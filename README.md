## Python CART CHUNK

### Installation

Clone this repo and install using pip:

```
$ git clone https://github.com/maxtimbo/python_cart_chunk
$ cd python_cart_chunk
$ pip install .
```

### Usage

You can use the CartChunk class to read CART CHUNK headers as well as riff and fmt data of a wave file:

```
from cart_chunk import CartChunk
from pathlib import Path

src = Path('/path/to/wave/file.wav')

wav = CartChunk(src)

if wav.is_scott:
    for key, value in wav.scott_data.items():
        print(f'{key:<20}: {value}')
else:
    print('Does not contain CART CHUNK')

for key, value in wav.riff_data.items():
    print(f'{key:<20}: {value}')

for key, value in wav.fmt_data.items():
    print(f'{key:<20}: {value}')

for key, value in wav.data_meta.items():
    print(f'{key:<20}: {value}')
```

Use the CartChunk class to write a new copy with the CART CHUNK (currently, only artist and title fields are supported):


```
from cart_chunk import NewCart

new_file = Path('/path/to/new/file.wav')

new_cart = NewCart(new_file, 'artist', 'title')

wav.write_copy(new_cart)
```
