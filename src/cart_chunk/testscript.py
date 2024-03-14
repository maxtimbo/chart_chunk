from cart_chunk import CartChunk, NewCart
from pathlib import Path

f = Path('/space/es1/codingbase/riff_headers/samples/SampleWav.wav')
n = Path(f.parents[0], 'NewCartTest.wav')

wav = CartChunk(f)
new_cart = NewCart(n, 'artist', 'title')
new_cart.trivia = 'test'
new_cart.category = 'NEW'
new_cart.cart = '1234'
#new_cart.intro = 1.159
new_cart.sec = 2.22
#new_cart.eom = 3.12
new_cart.year = 1999
new_cart.start_timestamp = ('121212', 13)
new_cart.end_timestamp = ('041224', 13)

wav.write_copy(new_cart)

scott = CartChunk(n)

#for k, v in scott.scott_data.items():
#    print(f'{k:<20}:{v}')

print(scott.scott_data['start_seconds'])
print(scott.scott_data['start_hundred'])
print(scott.scott_data['start_hour'])
