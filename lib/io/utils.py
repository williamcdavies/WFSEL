r"""
utils.py

Description:
   Provides definitions for io-utility functions.

Written by William Chuter-Davies
"""

# Standard Library Imports
from datetime import datetime
from pathlib import  Path
from typing  import  TextIO


def get_logstream(
   wdir: Path
) -> TextIO:
   """
   Opens a log file for appending.

   Parameters
   ----------
   wdir : :class:`pathlib.Path`
      The write directory

   Returns
   -------
   An open, writable file object.

   Notes
   -----
   The returned file object is a context manager.
   """
   timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")

   return open(
      wdir / (timestamp + ".log"),
      "a"
   )
