# Configuring Linger

As explained in the next section, Python exposes Synthizer events.  Prior to
0.9, events were a way to make sure that generators were destroyed after they
finished playing.  0.9, however, introduced a better mechanism, which allows one
to configure an object to stick around until it's "finished".  To configure this
in Python:

```
generator.config_delete_behavior(linger=True)
```

Other keyword arguments to `config_delete_behavior` correspond to other fields
on `syz_DeleteBehaviorConfig`, which is explained in the main Synthizer manual.

This isn't enabled by default because it is more important for applications to
be aware of the resources they are using, and making `dec_ref()` destroy the
object nearly immediately allows for this clarity.  Additionally, enabling it on
extremely long sounds is generally not the desired effect (in that case you also
want to pass `linger_timeout`).  That said, it is efficient enough to be used
without restriction.

The object reference in the main Synthizer manual explains what each object does
when lingering.
