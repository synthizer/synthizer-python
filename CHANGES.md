# 0.12.2 (2022-03-14)

- Add py.typed.
- Start building wheels for 3.7 and up again.

# 0.12.1 (2021-12-04)

- Build Python 3.10 Windows wheels.
- Drop all Windows wheels older than 3.9.  If you need these, `pip install` with
  properly configured C compilers will stil work.

  # 0.12.0 (2021-11-28)

- Support automation.
- All properties now need to use `.value = ` etc instead of just the raw
  property access.
- Extract the manual from Synthizer's repo and improve it; currently there is no
  GitHub pages, so you'll need to look in the repository itself.
