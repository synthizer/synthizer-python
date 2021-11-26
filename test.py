import datetime
import random as r
import array

import synthizer

from synthizer import Buffer, BufferGenerator, Context, Generator, Source3D

blen = 100


with synthizer.initialized():
    synthizer_context = Context(enable_events=True)
    synthizer_context.gain = 0
    buffer = Buffer.from_float_array(44100, 1, array.array("f", [0.0] * blen))
    previous_time = datetime.datetime.now()
    while True:
        for event in synthizer_context.get_events():
            if isinstance(event, synthizer.FinishedEvent):
                event.source.get_userdata().dec_ref()
        if (True and datetime.datetime.now() - previous_time).microseconds >= 500000:
            generator = BufferGenerator(synthizer_context)
            generator.buffer = buffer
            source = Source3D(synthizer_context)
            source.position = (
                r.randint(-15, 15),
                r.randint(-15, 15),
                r.randint(-15, 15),
            )
            source.add_generator(generator)
            generator.set_userdata(source)
            previous_time = datetime.datetime.now()
