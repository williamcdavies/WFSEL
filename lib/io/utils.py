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
   program_odir_path: Path
) -> TextIO:
   """
   Opens a log file for appending.

   Parameters
   ----------
   program_odir_path : :class:`pathlib.Path`
      The programm's output directory path

   Returns
   -------
   An open, writable file object.

   Notes
   -----
   The returned file object is a context manager.
   """
   return open(
      program_odir_path / "log.txt",
      "a"
   )
