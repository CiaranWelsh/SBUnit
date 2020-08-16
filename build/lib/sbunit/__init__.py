#todo we can make this smarter by having a regestration system
#  then people could implement their backend elsewhere, i.e.
#  without having to fork this repo

BACKENDS = ["tellurium"]

BACKEND = "tellurium"

if BACKEND not in BACKENDS:
    raise ValueError(f"Backend {BACKEND} not recognized")

if BACKEND == "tellurium":
    from ._tellurium_backend import TestCase
