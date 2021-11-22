"""Fade out a direct source over 2 seconds."""

import math
import sys
import synthizer


def circle(ctx, source, distance=10.0, circle_time=5.0):
    batch = synthizer.AutomationBatch(ctx)
    step_time = circle_time / 360
    start_time = source.suggested_automation_time.value
    for step in range(0, 361):
        angle = math.radians(step)
        x, y = math.cos(angle) * distance, math.sin(angle) * distance
        batch.append_property(
            start_time + step * step_time,
            source.position,
            (x, y, 0),
            synthizer.InterpolationType.LINEAR,
        )
    batch.send_user_event(start_time + circle_time, source, 0)
    batch.execute()


if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <file>")
    sys.exit(1)

# Initialize all needed Synthizer objects
with synthizer.initialized(logging_backend=synthizer.LoggingBackend.STDERR):
    ctx = synthizer.Context(enable_events=True)
    ctx.default_panner_strategy.value = synthizer.PannerStrategy.HRTF
    buffer = synthizer.Buffer.from_file(sys.argv[1])
    generator = synthizer.BufferGenerator(ctx)
    generator.buffer.value = buffer
    source = synthizer.Source3D(ctx)
    source.add_generator(generator)

    # Rotate a source around the listener, starting from the right using the default parameters of distance=10.0 and circle_time=5.0
    circle(ctx, source)

    running = True
    # Repeat until the UserAutomationEvent corresponding to the end of the fadeout is raised
    while running:
        for event in ctx.get_events():
            if isinstance(event, synthizer.UserAutomationEvent):
                print("Fadeout complete.")
                running = False
