"""Fade out a direct source over 2 seconds."""

import sys
import synthizer


def fadeout(ctx, obj, time):
    # Create an AutomationBatch, a one-use queue for automating object properties
    batch = synthizer.AutomationBatch(ctx)

    # Determine when the fadeout should actually start
    # Get the suggested automation time that Synthizer provides
    start_time = obj.suggested_automation_time.value

    # Determine when the fadeout will conclude
    # The volume will slowly decrease over the period [start_time, end_time]
    end_time = start_time + fadeout_time

    # Note that we need two points to apply linear interpolation between, otherwise the library has no way of knowing when the intended timeline actually starts
    # As a result, add a dummy automation point that just uses the current gain of the source to mark where it starts
    batch.append_property(
        start_time, obj.gain, obj.gain.value, synthizer.InterpolationType.NONE
    )
    batch.append_property(end_time, obj.gain, 0.0, synthizer.InterpolationType.LINEAR)

    # Add a user event to the timeline so the script can determine roughly when the fadeout ended
    # It doesn't matter what the event parameter is here but for more complicated scripts an enum value or some kind of object reference can be derived from the parameter
    batch.send_user_event(end_time, obj, 0)

    # Finally queue all of these events to be executed
    batch.execute()


if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <file>")
    sys.exit(1)

# Initialize all needed Synthizer objects
with synthizer.initialized(logging_backend=synthizer.LoggingBackend.STDERR):
    ctx = synthizer.Context(enable_events=True)
    buffer = synthizer.Buffer.from_file(sys.argv[1])
    generator = synthizer.BufferGenerator(ctx)
    generator.buffer.value = buffer
    source = synthizer.DirectSource(ctx)
    source.add_generator(generator)

    # Fade out over 2 seconds
    fadeout(ctx, source, 2.0)
    running = True

    # Repeat until the UserAutomationEvent corresponding to the end of the fadeout is raised
    while running:
        for event in ctx.get_events():
            if isinstance(event, synthizer.UserAutomationEvent):
                print("Fadeout complete.")
                running = False
