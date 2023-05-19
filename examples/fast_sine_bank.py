"""Run through the wave types supported by the fast sine bank generator."""
import synthizer
import time

def drive_generator(g):
    freq = 300.0
    while freq >= 100.0:
        g.frequency.value = freq
        freq -= 5.0
        time.sleep(0.03)

with synthizer.initialized(
    log_level=synthizer.LogLevel.DEBUG, logging_backend=synthizer.LoggingBackend.STDERR
):
    ctx = synthizer.Context()
    source = synthizer.DirectSource(ctx)

    print("Sine")
    generator = synthizer.FastSineBankGenerator.create_sine_wave_generator(ctx, 300.0)
    source.add_generator(generator)
    drive_generator(generator)
    generator.dec_ref()

    print("Square partials=10")
    generator = synthizer.FastSineBankGenerator.create_square_wave_generator(ctx, 300.0, 10.0)
    source.add_generator(generator)
    drive_generator(generator)
    generator.dec_ref()

    print("triangle partials=10")
    generator = synthizer.FastSineBankGenerator.create_triangle_wave_generator(ctx, 300.0, 10.0)
    source.add_generator(generator)
    drive_generator(generator)
    generator.dec_ref()

    print("sawtooth partials=30")
    generator = synthizer.FastSineBankGenerator.create_sawtooth_wave_generator(ctx, 300.0, 10.0)
    source.add_generator(generator)
    drive_generator(generator)

    source.dec_ref()
    generator.dec_ref()
    ctx.dec_ref()
