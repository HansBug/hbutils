"""
This module provides a lightweight implementation of tqdm progress bar functionality.

It includes a SimpleTqdm class that mimics the basic behavior of the popular tqdm library,
allowing for progress tracking in loops and iterable operations. If the actual tqdm library
is available, it will be used; otherwise, this simplified version serves as a fallback.

The module supports:

- Progress bars with percentage, elapsed time, and ETA
- Unit scaling for better readability
- Terminal width detection
- Thread-safe multi-progress bar management
- Context manager and iterator protocols
"""

import os
import shutil
import sys
import threading
import time
import warnings

try:
    from tqdm import tqdm as _origin_tqdm
except (ImportError, ModuleNotFoundError):
    _origin_tqdm = None

__all__ = [
    'SimpleTqdm',
    'tqdm',
    'trange',
]


class SimpleTqdm:
    """
    A lightweight implementation of tqdm progress bar.
    
    This class provides basic progress bar functionality similar to tqdm,
    with support for iteration tracking, time estimation, and customizable display.
    
    :ivar _instances: Global list of all active SimpleTqdm instances
    :vartype _instances: list
    :ivar _lock: Thread lock for managing concurrent progress bar updates
    :vartype _lock: threading.Lock
    :ivar _last_print_time: Timestamp of the last global print operation
    :vartype _last_print_time: float
    :ivar _update_interval: Minimum interval between display updates
    :vartype _update_interval: float
    """

    # Global manager for handling multiple progress bars
    _instances = []
    _lock = threading.Lock()
    _last_print_time = 0
    _update_interval = 0.1  # Update interval

    def __init__(self, iterable=None, desc=None, total=None, leave=True,
                 file=None, ncols=None, mininterval=0.1, ascii=None, disable=False, unit='it',
                 unit_scale=False, initial=0, position=None, unit_divisor=1000, **kwargs):
        """
        Initialize a SimpleTqdm progress bar.
        
        :param iterable: Iterable to decorate with a progress bar
        :type iterable: iterable, optional
        :param desc: Prefix for the progress bar
        :type desc: str, optional
        :param total: The number of expected iterations
        :type total: int, optional
        :param leave: If True, keep all traces of the progress bar upon termination
        :type leave: bool
        :param file: Specifies where to output the progress messages
        :type file: file-like object, optional
        :param ncols: The width of the entire output message
        :type ncols: int, optional
        :param mininterval: Minimum progress display update interval in seconds
        :type mininterval: float
        :param ascii: If True, use ASCII characters for the progress bar
        :type ascii: bool, optional
        :param disable: Whether to disable the entire progress bar
        :type disable: bool
        :param unit: String that will be used to define the unit of each iteration
        :type unit: str
        :param unit_scale: If True, the number of iterations will be scaled automatically
        :type unit_scale: bool
        :param initial: The initial counter value
        :type initial: int
        :param position: Specify the line offset to print this bar
        :type position: int, optional
        :param unit_divisor: Divisor for unit scaling (1000 or 1024)
        :type unit_divisor: int
        :param kwargs: Additional keyword arguments (will trigger a warning if provided)
        
        Example::
            >>> with SimpleTqdm(range(100), desc="Processing") as pbar:
            ...     for item in pbar:
            ...         time.sleep(0.01)
            Processing: 100.0% |====================>| 100/100 [00:01<00:00, 99.5it/s]
        """

        if kwargs:
            warnings.warn(f'You are using {self.__class__.__name__} provided by hbutils library, '
                          f'which is an lightweight alternative of real tqdm. '
                          f'Arguments {kwargs!r} are ignored because they are not supported. '
                          f'If you really need them, we suggest you can use tqdm by installing it with `pip install tqdm`.')

        self.iterable = iterable
        self.desc = desc or ""
        self.total = total
        self.leave = leave
        self.file = file or sys.stderr
        self.disable = disable
        self.unit = unit
        self.unit_scale = unit_scale
        self.unit_divisor = unit_divisor
        self.mininterval = mininterval
        self.position = position
        self.ncols = ncols
        self.ascii = ascii

        # Internal state
        self.n = initial
        self.start_time = None
        self.last_print_time = 0
        self.last_print_n = 0

        # If an iterable is provided and total is not specified, try to get its length
        if iterable is not None and total is None:
            try:
                self.total = len(iterable)
            except (TypeError, AttributeError):
                self.total = None

        # Register to global manager
        if not self.disable:
            with SimpleTqdm._lock:
                SimpleTqdm._instances.append(self)

    def _format_sizeof(self, num, suffix="", divisor=None):
        """
        Format number size with unit scaling support.
        
        :param num: The number to format
        :type num: float
        :param suffix: Suffix to append to the formatted number
        :type suffix: str
        :param divisor: Divisor for unit scaling (1000 or 1024)
        :type divisor: int, optional
        
        :return: Formatted string with appropriate unit
        :rtype: str
        
        Example::
            >>> pbar = SimpleTqdm(total=1000, unit_scale=True)
            >>> pbar._format_sizeof(1500, "B")
            '1.5kB'
        """
        if divisor is None:
            divisor = self.unit_divisor

        # Define units
        if divisor == 1024:
            units = ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']
        else:  # divisor == 1000
            units = ['', 'k', 'M', 'G', 'T', 'P', 'E', 'Z']

        if not self.unit_scale:
            return f"{num:.0f}{suffix}"

        for unit in units:
            if abs(num) < divisor:
                if unit == '':
                    return f"{num:.0f}{unit}{suffix}"
                else:
                    return f"{num:.1f}{unit}{suffix}"
            num /= divisor

        return f"{num:.1f}{units[-1]}{suffix}"

    def _get_terminal_width(self):
        """
        Get the terminal width.
        
        :return: Terminal width in characters
        :rtype: int
        
        Example::
            >>> pbar = SimpleTqdm()
            >>> width = pbar._get_terminal_width()
            >>> width >= 80
            True
        """
        if self.ncols:
            return self.ncols

        try:
            # Try using shutil.get_terminal_size()
            return shutil.get_terminal_size().columns
        except (AttributeError, OSError):
            try:
                # Try getting from environment variable
                return int(os.environ.get('COLUMNS', 80))
            except (ValueError, TypeError):
                # Default width
                return 80

    def _create_progress_bar(self, percentage, bar_width):
        """
        Create a progress bar string.
        
        :param percentage: Completion percentage (0-100)
        :type percentage: float
        :param bar_width: Width of the progress bar in characters
        :type bar_width: int
        
        :return: Formatted progress bar string
        :rtype: str
        
        Example::
            >>> pbar = SimpleTqdm()
            >>> pbar._create_progress_bar(50, 20)
            '|==========>---------|'
        """
        if bar_width <= 0:
            return ""

        filled_width = int(bar_width * percentage / 100)

        if self.ascii:
            # Use ASCII characters
            filled_char = '='
            empty_char = '-'
            tip_char = '>' if filled_width < bar_width and percentage > 0 else ''
        else:
            # Use simple characters
            filled_char = '='
            empty_char = '-'
            tip_char = '>' if filled_width < bar_width and percentage > 0 else ''

        # Build progress bar
        if tip_char and filled_width > 0:
            bar = filled_char * (filled_width - 1) + tip_char + empty_char * (bar_width - filled_width)
        else:
            bar = filled_char * filled_width + empty_char * (bar_width - filled_width)

        return f"|{bar}|"

    def __enter__(self):
        """
        Enter the context manager.
        
        :return: Self instance
        :rtype: SimpleTqdm
        
        Example::
            >>> with SimpleTqdm(range(10)) as pbar:
            ...     for item in pbar:
            ...         pass
        """
        if self.start_time is None:
            self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the context manager.
        
        :param exc_type: Exception type if an exception occurred
        :type exc_type: type, optional
        :param exc_val: Exception value if an exception occurred
        :type exc_val: Exception, optional
        :param exc_tb: Exception traceback if an exception occurred
        :type exc_tb: traceback, optional
        
        Example::
            >>> with SimpleTqdm(range(10)) as pbar:
            ...     for item in pbar:
            ...         pass
        """
        self.close()

    def __iter__(self):
        """
        Iterate over the wrapped iterable with progress tracking.
        
        :return: Iterator yielding items from the wrapped iterable
        :raises TypeError: If no iterable was provided during initialization
        
        Example::
            >>> for item in SimpleTqdm(range(5)):
            ...     print(item)
            0
            1
            2
            3
            4
        """
        if self.iterable is None:
            raise TypeError("'NoneType' object is not iterable")

        if self.start_time is None:
            self.start_time = time.time()

        try:
            for item in self.iterable:
                yield item
                self.update(1)
        finally:
            if not self.leave:
                self.close()

    def update(self, n=1):
        """
        Update the progress bar by incrementing the counter.
        
        :param n: Increment to add to the internal counter
        :type n: int
        
        Example::
            >>> pbar = SimpleTqdm(total=100)
            >>> pbar.update(10)
            >>> pbar.n
            10
        """
        if self.disable:
            return

        if self.start_time is None:
            self.start_time = time.time()

        self.n += n

        # Check if display needs to be updated
        current_time = time.time()
        if (current_time - self.last_print_time) >= self.mininterval:
            self.refresh()

    def refresh(self):
        """
        Force refresh of the progress bar display.
        
        Example::
            >>> pbar = SimpleTqdm(total=100)
            >>> pbar.n = 50
            >>> pbar.refresh()  # Force display update
        """
        if self.disable:
            return

        current_time = time.time()
        self.last_print_time = current_time

        # Use global lock to ensure multiple progress bars don't conflict
        with SimpleTqdm._lock:
            self._display()

    def _display(self):
        """
        Display the current progress bar state.
        
        This internal method formats and outputs the progress bar to the file stream.
        It calculates the terminal width, builds the progress bar components including
        description, percentage, progress numbers, time information, ETA, and speed,
        then outputs the formatted string to the specified file.
        
        Example::
            >>> pbar = SimpleTqdm(total=100, desc="Processing")
            >>> pbar.n = 50
            >>> pbar._display()  # Outputs: Processing:  50.0% |=========>---------| 50/100 [00:05<00:05, 10.0it/s]
        """
        if self.start_time is None:
            return

        current_time = time.time()
        elapsed = current_time - self.start_time

        # Get terminal width
        terminal_width = self._get_terminal_width()

        # Build display string parts
        parts = []

        # Description
        desc_part = f"{self.desc}: " if self.desc else ""

        # Percentage and progress numbers
        if self.total is not None:
            percentage = (self.n / self.total) * 100 if self.total > 0 else 0
            percent_part = f"{percentage:6.1f}%"
            # Use formatted number display
            current_formatted = self._format_sizeof(self.n, self.unit)
            total_formatted = self._format_sizeof(self.total, self.unit)
            progress_part = f"{current_formatted}/{total_formatted}"
        else:
            percentage = 0
            percent_part = ""
            # Use formatted number display
            progress_part = self._format_sizeof(self.n, self.unit)

        # Time information
        time_part = f"[{self._format_time(elapsed)}"

        # Estimated time remaining
        eta_part = ""
        if self.total is not None and self.n > 0 and elapsed > 0:
            rate = self.n / elapsed
            if rate > 0:
                eta = (self.total - self.n) / rate
                eta_part = f"<{self._format_time(eta)}"

        # Speed
        speed_part = ""
        if elapsed > 0:
            rate = self.n / elapsed
            # Use formatted speed display
            rate_formatted = self._format_sizeof(rate, f"{self.unit}/s")
            speed_part = f", {rate_formatted}"

        # Combine fixed parts
        fixed_parts = [desc_part, percent_part, progress_part, time_part]
        if eta_part:
            fixed_parts.append(eta_part)
        if speed_part:
            fixed_parts.append(speed_part)
        fixed_parts.append("]")

        # Calculate fixed parts length
        fixed_text = "".join(fixed_parts)
        fixed_length = len(fixed_text)

        # Reserve space for progress bar
        # Progress bar format: |====>----|
        min_bar_width = 10  # Minimum progress bar width
        bar_overhead = 2  # Characters used by | and |

        available_width = terminal_width - fixed_length - bar_overhead - 1  # -1 for safety margin
        bar_width = max(min_bar_width, min(available_width, 50))  # Limit maximum width to 50

        # Create progress bar
        if self.total is not None:
            progress_bar = self._create_progress_bar(percentage, bar_width)
        else:
            # Display simple activity indicator when total is unknown
            progress_bar = self._create_activity_bar()

        # Combine final output
        if self.total is not None:
            line = f"{desc_part}{percent_part} {progress_bar} {progress_part} {time_part}"
            if eta_part:
                line += eta_part
            if speed_part:
                line += speed_part
            line += "]"
        else:
            line = f"{desc_part}{progress_bar} {progress_part} {time_part}"
            if speed_part:
                line += speed_part
            line += "]"

        # Ensure it doesn't exceed terminal width
        if len(line) > terminal_width:
            line = line[:terminal_width - 3] + "..."

        # Clear current line and output
        self.file.write(f"\r{line}")
        self.file.flush()

    _ACTIVITY = ['|', '/', '-', '\\', '|', '/', '-', '\\']

    def _create_activity_bar(self, speed: float = 3.0):
        """
        Create an activity indicator for cases without a known total.
        
        :param speed: Speed of the animation (cycles per second)
        :type speed: float
        
        :return: Current activity indicator character
        :rtype: str
        
        Example::
            >>> pbar = SimpleTqdm()
            >>> indicator = pbar._create_activity_bar()
            >>> indicator in ['|', '/', '-', '\\\\']
            True
        """
        if self.start_time is None:
            self.start_time = time.time()
        idx = int((time.time() - self.start_time) * speed) % len(self._ACTIVITY)
        return self._ACTIVITY[idx]

    def _format_time(self, seconds):
        """
        Format time display.
        
        :param seconds: Time in seconds
        :type seconds: float
        
        :return: Formatted time string in format HH:MM:SS or MM:SS or SS.SSs
        :rtype: str
        
        Example::
            >>> pbar = SimpleTqdm()
            >>> pbar._format_time(65)
            '01:05'
            >>> pbar._format_time(3665)
            '01:01:05'
        """
        if seconds < 60:
            return f"{seconds:05.2f}s"
        elif seconds < 3600:
            mins, secs = divmod(int(seconds), 60)
            return f"{mins:02d}:{secs:02d}"
        else:
            hours, remainder = divmod(int(seconds), 3600)
            mins, secs = divmod(remainder, 60)
            return f"{hours:02d}:{mins:02d}:{secs:02d}"

    def set_description(self, desc=None, refresh=True):
        """
        Set the progress bar description.
        
        :param desc: New description text
        :type desc: str, optional
        :param refresh: Whether to refresh the display immediately
        :type refresh: bool
        
        Example::
            >>> pbar = SimpleTqdm(range(100))
            >>> pbar.set_description("Processing files")
        """
        self.desc = desc or ""
        if refresh:
            self.refresh()

    def set_postfix(self, ordered_dict=None, refresh=True, **kwargs):
        """
        Set postfix information (simplified implementation, not actually displayed).
        
        This method exists for API compatibility with tqdm but does not display
        the postfix information in SimpleTqdm.
        
        :param ordered_dict: Dictionary of postfix key-value pairs
        :type ordered_dict: dict, optional
        :param refresh: Whether to refresh the display immediately
        :type refresh: bool
        :param kwargs: Additional postfix key-value pairs
        
        Example::
            >>> pbar = SimpleTqdm(range(100))
            >>> pbar.set_postfix(loss=0.5, accuracy=0.95)
        """
        if refresh:
            self.refresh()

    def close(self):
        """
        Close the progress bar and clean up resources.
        
        This method performs a final refresh of the progress bar, adds a newline
        if leave is True, or clears the line if leave is False, and removes the
        instance from the global manager.
        
        Example::
            >>> pbar = SimpleTqdm(range(100))
            >>> for item in pbar:
            ...     pass
            >>> pbar.close()
        """
        if self.disable:
            return

        # Final refresh
        self.refresh()

        # If leave is True, add newline; otherwise clear current line
        if self.leave:
            self.file.write("\n")
        else:
            # Clear current line
            terminal_width = self._get_terminal_width()
            self.file.write("\r" + " " * terminal_width + "\r")

        self.file.flush()

        # Remove from global manager
        with SimpleTqdm._lock:
            try:
                SimpleTqdm._instances.remove(self)
            except ValueError:
                pass

    def clear(self):
        """
        Clear the current display.
        
        This method clears the progress bar from the terminal by overwriting
        the current line with spaces.
        
        Example::
            >>> pbar = SimpleTqdm(range(100))
            >>> pbar.clear()  # Clear the progress bar from terminal
        """
        if not self.disable:
            terminal_width = self._get_terminal_width()
            self.file.write("\r" + " " * terminal_width + "\r")
            self.file.flush()

    def write(self, s, file=None, end="\n", nolock=False):
        """
        Write text without disrupting the progress bar display.
        
        This method allows writing messages to the output stream without
        interfering with the progress bar. It temporarily clears the progress
        bar, writes the message, and then refreshes the progress bar.
        
        :param s: String to write
        :type s: str
        :param file: File object to write to
        :type file: file-like object, optional
        :param end: String appended after the last value
        :type end: str
        :param nolock: If True, don't use the global lock
        :type nolock: bool
        
        Example::
            >>> pbar = SimpleTqdm(range(100))
            >>> pbar.write("Processing complete")
        """
        fp = file or self.file

        if not nolock:
            with SimpleTqdm._lock:
                self.clear()
                fp.write(str(s) + end)
                fp.flush()
                self.refresh()
        else:
            fp.write(str(s) + end)
            fp.flush()


def tqdm(iterable=None, desc=None, total=None, leave=True,
         file=None, ncols=None, mininterval=0.1, ascii=None, disable=False, unit='it',
         unit_scale=False, initial=0, position=None, unit_divisor=1000, **kwargs):
    """
    tqdm-compatible interface for creating progress bars.
    
    This function provides a unified interface that uses the real tqdm library if available,
    otherwise falls back to SimpleTqdm. It maintains API compatibility with the standard
    tqdm library while providing a lightweight alternative when tqdm is not installed.
    
    :param iterable: Iterable to decorate with a progress bar
    :type iterable: iterable, optional
    :param desc: Prefix for the progress bar
    :type desc: str, optional
    :param total: The number of expected iterations
    :type total: int, optional
    :param leave: If True, keep all traces of the progress bar upon termination
    :type leave: bool
    :param file: Specifies where to output the progress messages
    :type file: file-like object, optional
    :param ncols: The width of the entire output message
    :type ncols: int, optional
    :param mininterval: Minimum progress display update interval in seconds
    :type mininterval: float
    :param ascii: If True, use ASCII characters for the progress bar
    :type ascii: bool, optional
    :param disable: Whether to disable the entire progress bar
    :type disable: bool
    :param unit: String that will be used to define the unit of each iteration
    :type unit: str
    :param unit_scale: If True, the number of iterations will be scaled automatically
    :type unit_scale: bool
    :param initial: The initial counter value
    :type initial: int
    :param position: Specify the line offset to print this bar
    :type position: int, optional
    :param unit_divisor: Divisor for unit scaling (1000 or 1024)
    :type unit_divisor: int
    :param kwargs: Additional keyword arguments passed to the underlying implementation
    
    :return: Progress bar instance (either real tqdm or SimpleTqdm)
    :rtype: tqdm or SimpleTqdm
    
    Example::
        >>> for i in tqdm(range(100), desc="Processing"):
        ...     time.sleep(0.01)
        Processing: 100.0% |====================>| 100/100 [00:01<00:00, 99.5it/s]
    """
    if _origin_tqdm:
        return _origin_tqdm(iterable=iterable, desc=desc, total=total, leave=leave,
                            file=file, ncols=ncols, mininterval=mininterval,
                            ascii=ascii, disable=disable, unit=unit, unit_scale=unit_scale,
                            initial=initial, position=position, unit_divisor=unit_divisor, **kwargs)
    else:
        return SimpleTqdm(iterable=iterable, desc=desc, total=total, leave=leave,
                          file=file, ncols=ncols, mininterval=mininterval,
                          ascii=ascii, disable=disable, unit=unit, unit_scale=unit_scale,
                          initial=initial, position=position, unit_divisor=unit_divisor, **kwargs)


def trange(*args, **kwargs):
    """
    Shortcut for tqdm(range(*args), **kwargs).
    
    This is a convenience function that creates a progress bar for a range iterator.
    It's equivalent to calling tqdm(range(*args), **kwargs).
    
    :param args: Positional arguments passed to range()
    :type args: int
    :param kwargs: Keyword arguments passed to tqdm()
    
    :return: Progress bar instance wrapping a range iterator
    :rtype: tqdm or SimpleTqdm
    
    Example::
        >>> for i in trange(100, desc="Counting"):
        ...     time.sleep(0.01)
        Counting: 100.0% |====================>| 100/100 [00:01<00:00, 99.5it/s]
    """
    return tqdm(range(*args), **kwargs)
