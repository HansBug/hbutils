"""
Overview:
    This module provides functionality to enhance logging output with colors for different log levels.
    It includes an `ANSIColors` class defining ANSI escape sequences for various colors and styles,
    and a `ColoredFormatter` class to format log messages with these colors based on their severity level.
    
    The module supports multi-line log messages with proper indentation alignment, making logs more
    readable and visually organized.

Example::
    >>> import logging
    >>> from hbutils.logging import ColoredFormatter
    >>> 
    >>> logger = logging.getLogger()
    >>> logger.setLevel(logging.DEBUG)
    >>> console_handler = logging.StreamHandler()
    >>> console_handler.setFormatter(ColoredFormatter())
    >>> logger.addHandler(console_handler)
    >>> 
    >>> # Test single line message
    >>> logger.info("This is a single line message")
    >>> # Test multi-line message
    >>> logger.warning("This is a multi-line message:\\nLine 2 content\\nLine 3 content\\nLine 4 content")
    >>> logger.error(
    ...     "Error details:\\n  - Error code: 500\\n  - Error message: Internal server error\\n  - Stack trace follows...")
"""

import logging
import os

__all__ = [
    'ANSIColors',
    'ColoredFormatter',
    'format_multiline_message',
]


class ANSIColors:
    """
    A collection of ANSI escape sequences for terminal text coloring and styling.
    
    These constants can be used to format strings with various colors and text styles
    in terminal environments that support ANSI escape codes.
    
    Attributes:
        * RESET (str): Reset all text formatting to default.
        * BOLD (str): Apply bold text style.
        * UNDERLINE (str): Apply underline text style.
        * BLACK (str): Apply black color to text.
        * RED (str): Apply red color to text.
        * GREEN (str): Apply green color to text.
        * YELLOW (str): Apply yellow color to text.
        * BLUE (str): Apply blue color to text.
        * MAGENTA (str): Apply magenta color to text.
        * CYAN (str): Apply cyan color to text.
        * WHITE (str): Apply white color to text.
        * BRIGHT_BLACK (str): Apply bright black (gray) color to text.
        * BRIGHT_RED (str): Apply bright red color to text.
        * BRIGHT_GREEN (str): Apply bright green color to text.
        * BRIGHT_YELLOW (str): Apply bright yellow color to text.
        * BRIGHT_BLUE (str): Apply bright blue color to text.
        * BRIGHT_MAGENTA (str): Apply bright magenta color to text.
        * BRIGHT_CYAN (str): Apply bright cyan color to text.
        * BRIGHT_WHITE (str): Apply bright white color to text.
    
    Example::
        >>> print(f"{ANSIColors.RED}This is red text{ANSIColors.RESET}")
        This is red text  # (displayed in red in terminal)
        >>> print(f"{ANSIColors.BOLD}{ANSIColors.GREEN}Bold green text{ANSIColors.RESET}")
        Bold green text  # (displayed in bold green in terminal)
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
    Format a multi-line message with proper indentation for continuation lines.

    The first line of the message remains unchanged, while all subsequent lines
    are indented by the specified number of spaces to align with the message content.
    
    :param message: The message to format, potentially containing multiple lines.
    :type message: str
    :param indent_length: The number of spaces to indent continuation lines.
    :type indent_length: int

    :return: The formatted message with proper indentation for multi-line content.
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
    A logging formatter that applies colors to log messages based on their severity level.

    This formatter enhances log readability by applying different colors to different
    log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL) and formatting components
    (timestamp, level name, logger name, message). It also supports multi-line messages
    with proper indentation alignment.
    
    The color scheme is:
        - DEBUG: Blue
        - INFO: Green
        - WARNING: Yellow
        - ERROR: Red
        - CRITICAL: Bold Red

    Attributes:
        COLORS (dict): Mapping of log level names to their corresponding ANSI color codes.
        datefmt (str): The date format string for timestamps.
    
    Example::
        >>> import logging
        >>> logger = logging.getLogger(__name__)
        >>> handler = logging.StreamHandler()
        >>> handler.setFormatter(ColoredFormatter())
        >>> logger.addHandler(handler)
        >>> logger.setLevel(logging.DEBUG)
        >>> 
        >>> logger.debug("Debug message")
        >>> logger.info("Info message")
        >>> logger.warning("Warning message\\nwith multiple lines")
        >>> logger.error("Error message")
        >>> logger.critical("Critical message")
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
        Initialize the ColoredFormatter with custom date format and optional parameters.

        :param datefmt: The date format string for formatting timestamps in log messages.
                       Defaults to '%Y-%m-%d %H:%M:%S'.
        :type datefmt: str
        :param args: Additional positional arguments passed to the parent Formatter class.
        :param kwargs: Additional keyword arguments passed to the parent Formatter class.
        
        Example::
            >>> formatter = ColoredFormatter(datefmt='%H:%M:%S')
            >>> formatter = ColoredFormatter(datefmt='%Y/%m/%d %H:%M:%S')
        """
        super().__init__(*args, **kwargs)
        self.datefmt = datefmt
        self._indent_cache = {}

    def _calculate_indent_length(self, record: logging.LogRecord) -> int:
        """
        Calculate the length of the log prefix for proper multi-line message indentation.
        
        The prefix includes the timestamp, level name, and logger name. This method
        calculates the total character length (excluding ANSI color codes) to determine
        how much to indent continuation lines in multi-line messages.

        Results are cached based on (level name, logger name) to improve performance.
        
        :param record: The log record containing information about the log event.
        :type record: logging.LogRecord

        :return: The length of the prefix without ANSI color codes, used for indentation.
        :rtype: int
        
        Example::
            >>> # For a log record with level INFO and logger name 'myapp'
            >>> # Prefix might be: "[2024-01-15 10:30:45] INFO     myapp "
            >>> # This method would return the character count of that prefix
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
        Format the specified log record as colored text with proper multi-line indentation.
        
        This method applies appropriate colors based on the log level and formats the
        message with the following structure:
        [timestamp] level_name logger_name message
        
        Multi-line messages are automatically indented so that continuation lines align
        with the start of the message content.

        :param record: The log record to be formatted.
        :type record: logging.LogRecord

        :return: The formatted log message with appropriate colors and proper multi-line indentation.
        :rtype: str
        
        Example::
            >>> import logging
            >>> record = logging.LogRecord(
            ...     name='test', level=logging.INFO, pathname='', lineno=0,
            ...     msg='Multi-line\\nmessage', args=(), exc_info=None
            ... )
            >>> formatter = ColoredFormatter()
            >>> formatted = formatter.format(record)
            >>> # Output will be colored and properly indented:
            >>> # [2024-01-15 10:30:45] INFO     test Multi-line
            >>> #                                    message
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
        record_copy.args = None  # Clear args since we've already formatted the message

        formatter = logging.Formatter(format_str, datefmt=self.datefmt)
        return formatter.format(record_copy)
