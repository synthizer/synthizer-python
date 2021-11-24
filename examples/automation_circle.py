"""Repeatedly rotate a source around the listener."""

import math
import sys
import time
import synthizer


def circle(ctx, source, distance=10.0, circle_time=5.0, circleCount=1):
    batch = synthizer.AutomationBatch(ctx)

    # The time taken to rotate one degree
    step_time = circle_time / 360
    start_time = source.suggested_automation_time.value

    # There are 361 steps (degrees) because we need to complete the circle from degree 359 back to 360
    for step in range(0, 361):
        angle = math.radians(step)
        x, y = math.cos(angle) * distance, math.sin(angle) * distance
        batch.append_property(
            start_time + step * step_time,
            source.position,
            (x, y, 0),
            synthizer.InterpolationType.LINEAR,
        )
    batch.send_user_event(start_time + circle_time, source, circleCount)
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
    while True:
        for event in ctx.get_events():
            if isinstance(event, synthizer.UserAutomationEvent):
                # Use the param passed to the event to determine which circle was just completed and increment for the next function call
                print(f"Circle {event.param} complete.")
                circle(ctx, source, circleCount=event.param + 1)
        time.sleep(0.01)
