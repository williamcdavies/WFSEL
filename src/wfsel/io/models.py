"""
Filename:   wfsel.io.models.py
Author:     William Chuter-Davies
"""

# Standard Library Imports
from dataclasses    import dataclass
from datetime       import (
                        UTC,
                        datetime,
                    )


@dataclass(kw_only = True)
class CompletedProcessLog:
    """Encapsulate the result of a completed process."""

    args:       list[str]
    returncode: int
    stdout:     str
    stderr:     str


    def __str__(self) -> str:
        """
        Return a string representation of a completed process log.

        Returns
        -------
        str
            A string representation of the completed process log
        """
        timestamp = datetime.now(tz = UTC).isoformat()

        return (
            f"{timestamp}\n"
            f"args:       {self.args}\n"
            f"returncode: {self.returncode}\n"
            f"stdout:     {self.stdout}\n"
            f"stderr:     {self.stderr}\n"
        )
