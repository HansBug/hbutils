"""
Colored logging formatter utilities with ANSI styling and multi-line alignment.

This module provides utilities for enhancing Python logging output using ANSI
escape sequences. It includes a color palette class for terminal styling,
a formatter that applies color based on log severity, and a helper function
for aligning multi-line log messages with the log prefix.

The main public components are:

* :class:`ANSIColors` - ANSI escape sequences for colors and styles.
* :class:`ColoredFormatter` - Logging formatter with colorized output.
* :func:`format_multiline_message` - Indentation helper for multi-line messages.

.. note::
   ANSI escape codes are intended for terminal output. Some environments
   (such as Windows cmd without ANSI support or log files) may not render
   colors correctly.

Example::

    >>> import logging
    >>> from hbutils.logging.format import ColoredFormatter
    >>>
    >>> logger = logging.getLogger("example")
    >>> logger.setLevel(logging.DEBUG)
    >>> handler = logging.StreamHandler()
    >>> handler.setFormatter(ColoredFormatter())
    >>> logger.addHandler(handler)
    >>>
    >>> logger.info("Single line message")
    >>> logger.warning("Multi-line message:\\nLine 2\\nLine 3")

"""

import logging
import os
from typing import Dict, Tuple

__all__ = [
    'ANSIColors',
    'ColoredFormatter',
    'format_multiline_message',
]


class ANSIColors:
    """
    ANSI escape sequences for terminal text coloring and styling.

    These constants can be used to format strings with various colors and
    text styles in terminal environments that support ANSI escape codes.

    :cvar str RESET: Reset all text formatting to default.
    :cvar str BOLD: Apply bold text style.
    :cvar str UNDERLINE: Apply underline text style.
    :cvar str BLACK: Apply black color to text.
    :cvar str RED: Apply red color to text.
    :cvar str GREEN: Apply green color to text.
    :cvar str YELLOW: Apply yellow color to text.
    :cvar str BLUE: Apply blue color to text.
    :cvar str MAGENTA: Apply magenta color to text.
    :cvar str CYAN: Apply cyan color to text.
    :cvar str WHITE: Apply white color to text.
    :cvar str BRIGHT_BLACK: Apply bright black (gray) color to text.
    :cvar str BRIGHT_RED: Apply bright red color to text.
    :cvar str BRIGHT_GREEN: Apply bright green color to text.
    :cvar str BRIGHT_YELLOW: Apply bright yellow color to text.
    :cvar str BRIGHT_BLUE: Apply bright blue color to text.
    :cvar str BRIGHT_MAGENTA: Apply bright magenta color to text.
    :cvar str BRIGHT_CYAN: Apply bright cyan color to text.
    :cvar str BRIGHT_WHITE: Apply bright white color to text.

    Example::

        >>> print(f"{ANSIColors.RED}This is red text{ANSIColors.RESET}")
        This is red text  # Displayed in red in a compatible terminal
        >>> print(f"{ANSIColors.BOLD}{ANSIColors.GREEN}Bold green text{ANSIColors.RESET}")
        Bold green text  # Displayed in bold green

    """
    RESET = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"


def format_multiline_message(message: str, indent_length: int) -> str:
    """
    Format a multi-line message with indentation for continuation lines.

    The first line of the message is preserved, while each subsequent line
    is prefixed with a number of spaces specified by ``indent_length``. This
    function is commonly used to align multi-line log messages with a log
    prefix.

    :param message: The message to format, potentially containing multiple lines.
    :type message: str
    :param indent_length: Number of spaces to indent continuation lines.
    :type indent_length: int
    :return: The formatted message with indentation applied to continuation lines.
    :rtype: str

    Example::

        >>> msg = "First line\\nSecond line\\nThird line"
        >>> result = format_multiline_message(msg, 4)
        >>> print(result)
        First line
            Second line
            Third line

    """
    lines = message.splitlines(keepends=False)
    if len(lines) == 0:
        return ''

    # First line remains unchanged
    formatted_lines = [lines[0]]

    # Subsequent lines get indented
    indent = ' ' * indent_length
    for line in lines[1:]:
        formatted_lines.append(indent + line)

    return os.linesep.join(formatted_lines)


class ColoredFormatter(logging.Formatter):
    """
    Logging formatter with ANSI colors and multi-line alignment.

    The formatter applies a color scheme based on log severity and ensures
    multi-line messages are indented to align with the log message content.

    Color scheme:

    - DEBUG: Blue
    - INFO: Green
    - WARNING: Yellow
    - ERROR: Red
    - CRITICAL: Bold Red

    :cvar dict COLORS: Mapping of log level names to ANSI color codes.
    :ivar str datefmt: Date format string for timestamp rendering.
    :ivar dict _indent_cache: Cached prefix lengths for indentation calculation.

    Example::

        >>> import logging
        >>> logger = logging.getLogger("demo")
        >>> handler = logging.StreamHandler()
        >>> handler.setFormatter(ColoredFormatter())
        >>> logger.addHandler(handler)
        >>> logger.setLevel(logging.DEBUG)
        >>> logger.warning("Warning message\\nwith multiple lines")

    """
    COLORS = {
        'DEBUG': ANSIColors.BLUE,
        'INFO': ANSIColors.GREEN,
        'WARNING': ANSIColors.YELLOW,
        'ERROR': ANSIColors.RED,
        'CRITICAL': ANSIColors.BOLD + ANSIColors.RED,
    }

    def __init__(self, datefmt: str = '%Y-%m-%d %H:%M:%S', *args, **kwargs):
        """
        Initialize the formatter.

        :param datefmt: Date format string for timestamps, defaults to
            ``'%Y-%m-%d %H:%M:%S'``.
        :type datefmt: str
        :param args: Additional positional arguments passed to
            :class:`logging.Formatter`.
        :param kwargs: Additional keyword arguments passed to
            :class:`logging.Formatter`.

        Example::

            >>> formatter = ColoredFormatter(datefmt='%H:%M:%S')
            >>> formatter = ColoredFormatter(datefmt='%Y/%m/%d %H:%M:%S')

        """
        super().__init__(*args, **kwargs)
        self.datefmt = datefmt
        self._indent_cache: Dict[Tuple[str, str], int] = {}

    def _calculate_indent_length(self, record: logging.LogRecord) -> int:
        """
        Calculate prefix length for multi-line indentation.

        The prefix includes the timestamp, level name, and logger name. This
        length excludes ANSI escape codes and is cached based on the log
        level and logger name for performance.

        :param record: The log record containing log context.
        :type record: logging.LogRecord
        :return: Prefix length used to indent continuation lines.
        :rtype: int

        Example::

            >>> # For level INFO and logger name 'myapp'
            >>> # Prefix: "[2024-01-15 10:30:45] INFO     myapp "
            >>> # This method returns the length of that prefix.

        """
        # Create a cache key based on level name and logger name
        cache_key = (record.levelname, record.name)

        if cache_key not in self._indent_cache:
            # Format timestamp part
            timestamp = self.formatTime(record, datefmt=self.datefmt)
            timestamp_part = f"[{timestamp}]"

            # Format level part (8 characters wide)
            level_part = f"{record.levelname:<8}"

            # Format logger name part
            name_part = f"{record.name}"

            # Calculate total length: [timestamp] + space + level + space + name + space
            indent_length = len(timestamp_part) + 1 + len(level_part) + 1 + len(name_part) + 1
            self._indent_cache[cache_key] = indent_length

        return self._indent_cache[cache_key]

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the specified log record with color and indentation.

        Output structure:

        ``[timestamp] level_name logger_name message``

        Multi-line messages are indented so that continuation lines align
        with the first character of the message content.

        :param record: The log record to format.
        :type record: logging.LogRecord
        :return: The formatted log message as a string.
        :rtype: str

        Example::

            >>> import logging
            >>> record = logging.LogRecord(
            ...     name='test', level=logging.INFO, pathname='', lineno=0,
            ...     msg='Multi-line\\nmessage', args=(), exc_info=None
            ... )
            >>> formatter = ColoredFormatter()
            >>> formatted = formatter.format(record)
            >>> print(formatted)
            [2024-01-15 10:30:45] INFO     test Multi-line
                                             message

        """
        log_color = self.COLORS.get(record.levelname, ANSIColors.RESET)

        # Build the format string
        format_str = f"{ANSIColors.BRIGHT_BLACK}[%(asctime)s]{ANSIColors.RESET} "
        format_str += f"{log_color}%(levelname)-8s{ANSIColors.RESET} "
        format_str += f"{ANSIColors.CYAN}%(name)s{ANSIColors.RESET} "
        format_str += f"%(message)s"

        # Calculate indent length for multi-line messages
        indent_length = self._calculate_indent_length(record)

        # Format multi-line message with proper indentation
        original_message = record.getMessage()
        formatted_message = format_multiline_message(original_message, indent_length)

        # Create a new record with the formatted message
        record_copy = logging.makeLogRecord(record.__dict__)
        record_copy.msg = formatted_message
        record_copy.args = None  # Clear args since the message is already formatted

        formatter = logging.Formatter(format_str, datefmt=self.datefmt)
        return formatter.format(record_copy)
