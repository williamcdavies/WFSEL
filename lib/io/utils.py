r"""
utils.py

Description:
   Provides definitions for io-utility functions.

Written by William Chuter-Davies
"""

# Standard Library Imports
from pathlib import Path
from typing  import TextIO


def get_program_odir_path(
   prog: str,
   time: str
) -> Path:
   """
   Returns the program's output directory.

   Parameters
   ----------
   prog : :class:`str`
      The program name

   time : :class:`str`
      The program time

   Returns
   -------
   A :class:`pathlib.Path`.
   """
   stem = prog.split(".")[0]
   
   return Path(f"{stem}_{time}")


def get_logstream(
   wdir_path: Path
) -> TextIO:
   """
   Opens a log file for appending.

   Parameters
   ----------
   wdir_path : :class:`pathlib.Path`
      The write directory path

   Returns
   -------
   An open, writable file object.

   Notes
   -----
   The returned file object is a context manager.
   """
   return open(
      wdir_path / "log.txt",
      "a"
   )
