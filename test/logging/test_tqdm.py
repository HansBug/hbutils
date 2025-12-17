import os
import warnings
from io import StringIO
from unittest.mock import patch, MagicMock

import pytest


@pytest.fixture
def mock_stderr():
    """Mock stderr for testing output."""
    return StringIO()


@pytest.fixture
def simple_tqdm(mock_stderr):
    """Create a SimpleTqdm instance with mocked stderr."""
    from hbutils.logging.progress import SimpleTqdm
    return SimpleTqdm(file=mock_stderr, disable=False)


@pytest.fixture
def simple_tqdm_with_total(mock_stderr):
    """Create a SimpleTqdm instance with total and mocked stderr."""
    from hbutils.logging.progress import SimpleTqdm
    return SimpleTqdm(total=100, file=mock_stderr, disable=False)


@pytest.fixture
def simple_tqdm_disabled():
    """Create a disabled SimpleTqdm instance."""
    from hbutils.logging.progress import SimpleTqdm
    return SimpleTqdm(disable=True)


@pytest.fixture
def mock_time():
    """Mock time.time() for consistent testing."""
    with patch('time.time') as mock:
        mock.return_value = 1000.0
        yield mock


@pytest.fixture
def clear_instances():
    """Clear SimpleTqdm instances before and after tests."""
    from hbutils.logging.progress import SimpleTqdm
    SimpleTqdm._instances.clear()
    yield
    SimpleTqdm._instances.clear()


@pytest.mark.unittest
class TestLoggingTqdm:
    def test_init_basic(self, clear_instances):
        """Test basic initialization."""
        from hbutils.logging.progress import SimpleTqdm
        pbar = SimpleTqdm()
        assert pbar.desc == ""
        assert pbar.total is None
        assert pbar.leave is True
        assert pbar.disable is False
        assert pbar.unit == 'it'
        assert pbar.unit_scale is False
        assert pbar.unit_divisor == 1000
        assert pbar.n == 0
        assert pbar.start_time is None

    def test_init_with_parameters(self, mock_stderr, clear_instances):
        """Test initialization with various parameters."""
        from hbutils.logging.progress import SimpleTqdm
        pbar = SimpleTqdm(
            desc="Test",
            total=100,
            leave=False,
            file=mock_stderr,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
            initial=10
        )
        assert pbar.desc == "Test"
        assert pbar.total == 100
        assert pbar.leave is False
        assert pbar.file == mock_stderr
        assert pbar.unit == 'B'
        assert pbar.unit_scale is True
        assert pbar.unit_divisor == 1024
        assert pbar.n == 10

    def test_init_with_iterable(self, clear_instances):
        """Test initialization with iterable."""
        from hbutils.logging.progress import SimpleTqdm
        data = [1, 2, 3, 4, 5]
        pbar = SimpleTqdm(data)
        assert pbar.iterable == data
        assert pbar.total == 5

    def test_init_with_iterable_no_len(self, clear_instances):
        """Test initialization with iterable that has no len."""
        from hbutils.logging.progress import SimpleTqdm
        data = iter([1, 2, 3])
        pbar = SimpleTqdm(data)
        assert pbar.iterable == data
        assert pbar.total is None

    def test_init_with_kwargs_warning(self, clear_instances):
        """Test initialization with unsupported kwargs triggers warning."""
        from hbutils.logging.progress import SimpleTqdm
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            pbar = SimpleTqdm(unsupported_arg=True)
            assert len(w) == 1
            assert "lightweight alternative" in str(w[0].message)

    def test_init_disabled_not_in_instances(self, clear_instances):
        """Test disabled progress bar is not added to instances."""
        from hbutils.logging.progress import SimpleTqdm
        pbar = SimpleTqdm(disable=True)
        assert pbar not in SimpleTqdm._instances

    def test_init_enabled_in_instances(self, clear_instances):
        """Test enabled progress bar is added to instances."""
        from hbutils.logging.progress import SimpleTqdm
        pbar = SimpleTqdm(disable=False)
        assert pbar in SimpleTqdm._instances

    def test_format_sizeof_no_scaling(self, simple_tqdm):
        """Test _format_sizeof without unit scaling."""
        result = simple_tqdm._format_sizeof(1500, "B")
        assert result == "1500B"

    def test_format_sizeof_with_scaling_1000(self, mock_stderr, clear_instances):
        """Test _format_sizeof with unit scaling using divisor 1000."""
        from hbutils.logging.progress import SimpleTqdm
        pbar = SimpleTqdm(unit_scale=True, unit_divisor=1000, file=mock_stderr)
        result = pbar._format_sizeof(1500, "B")
        assert result == "1.5kB"

    def test_format_sizeof_with_scaling_1024(self, mock_stderr, clear_instances):
        """Test _format_sizeof with unit scaling using divisor 1024."""
        from hbutils.logging.progress import SimpleTqdm
        pbar = SimpleTqdm(unit_scale=True, unit_divisor=1024, file=mock_stderr)
        result = pbar._format_sizeof(1536, "B")
        assert result == "1.5KiB"

    def test_format_sizeof_large_numbers(self, mock_stderr, clear_instances):
        """Test _format_sizeof with very large numbers."""
        from hbutils.logging.progress import SimpleTqdm
        pbar = SimpleTqdm(unit_scale=True, unit_divisor=1000, file=mock_stderr)
        result = pbar._format_sizeof(1e12, "B")
        assert result == "1.0TB"

    def test_format_sizeof_zero(self, mock_stderr, clear_instances):
        """Test _format_sizeof with zero."""
        from hbutils.logging.progress import SimpleTqdm
        pbar = SimpleTqdm(unit_scale=True, file=mock_stderr)
        result = pbar._format_sizeof(0, "B")
        assert result == "0B"

    def test_get_terminal_width_with_ncols(self, simple_tqdm):
        """Test _get_terminal_width when ncols is set."""
        simple_tqdm.ncols = 120
        assert simple_tqdm._get_terminal_width() == 120

    @patch('shutil.get_terminal_size')
    def test_get_terminal_width_shutil(self, mock_get_size, simple_tqdm):
        """Test _get_terminal_width using shutil."""
        simple_tqdm.ncols = None
        mock_get_size.return_value.columns = 100
        assert simple_tqdm._get_terminal_width() == 100

    @patch('shutil.get_terminal_size')
    def test_get_terminal_width_shutil_error(self, mock_get_size, simple_tqdm):
        """Test _get_terminal_width when shutil raises error."""
        simple_tqdm.ncols = None
        mock_get_size.side_effect = OSError()
        with patch.dict(os.environ, {'COLUMNS': '90'}):
            assert simple_tqdm._get_terminal_width() == 90

    @patch('shutil.get_terminal_size')
    def test_get_terminal_width_default(self, mock_get_size, simple_tqdm):
        """Test _get_terminal_width default value."""
        simple_tqdm.ncols = None
        mock_get_size.side_effect = OSError()
        with patch.dict(os.environ, {}, clear=True):
            assert simple_tqdm._get_terminal_width() == 80

    def test_create_progress_bar_basic(self, simple_tqdm):
        """Test _create_progress_bar basic functionality."""
        result = simple_tqdm._create_progress_bar(50, 20)
        assert result.startswith("|")
        assert result.endswith("|")
        assert len(result) == 22  # 20 + 2 for | |

    def test_create_progress_bar_zero_width(self, simple_tqdm):
        """Test _create_progress_bar with zero width."""
        result = simple_tqdm._create_progress_bar(50, 0)
        assert result == ""

    def test_create_progress_bar_ascii(self, mock_stderr, clear_instances):
        """Test _create_progress_bar with ASCII characters."""
        from hbutils.logging.progress import SimpleTqdm
        pbar = SimpleTqdm(ascii=True, file=mock_stderr)
        result = pbar._create_progress_bar(50, 20)
        assert "=" in result
        assert "-" in result

    def test_create_progress_bar_complete(self, simple_tqdm):
        """Test _create_progress_bar at 100% completion."""
        result = simple_tqdm._create_progress_bar(100, 20)
        assert result == "|" + "=" * 20 + "|"

    def test_create_progress_bar_zero_percent(self, simple_tqdm):
        """Test _create_progress_bar at 0% completion."""
        result = simple_tqdm._create_progress_bar(0, 20)
        assert result == "|" + "-" * 20 + "|"

    def test_context_manager_enter(self, simple_tqdm, mock_time):
        """Test context manager __enter__."""
        result = simple_tqdm.__enter__()
        assert result is simple_tqdm
        assert simple_tqdm.start_time == 1000.0

    def test_context_manager_exit(self, simple_tqdm):
        """Test context manager __exit__."""
        with patch.object(simple_tqdm, 'close') as mock_close:
            simple_tqdm.__exit__(None, None, None)
            mock_close.assert_called_once()

    def test_iter_no_iterable(self, simple_tqdm):
        """Test __iter__ when no iterable is provided."""
        with pytest.raises(TypeError, match="'NoneType' object is not iterable"):
            list(simple_tqdm)

    def test_iter_with_iterable(self, mock_stderr, mock_time, clear_instances):
        """Test __iter__ with iterable."""
        from hbutils.logging.progress import SimpleTqdm
        data = [1, 2, 3]
        pbar = SimpleTqdm(data, file=mock_stderr)

        result = list(pbar)
        assert result == [1, 2, 3]
        assert pbar.n == 3

    def test_iter_with_leave_false(self, mock_stderr, clear_instances):
        """Test __iter__ with leave=False."""
        from hbutils.logging.progress import SimpleTqdm
        data = [1, 2, 3]
        pbar = SimpleTqdm(data, leave=False, file=mock_stderr)

        with patch.object(pbar, 'close') as mock_close:
            list(pbar)
            mock_close.assert_called_once()

    def test_update_disabled(self, simple_tqdm_disabled):
        """Test update when disabled."""
        initial_n = simple_tqdm_disabled.n
        simple_tqdm_disabled.update(5)
        assert simple_tqdm_disabled.n == initial_n  # Should not change

    def test_update_sets_start_time(self, simple_tqdm, mock_time):
        """Test update sets start_time if not already set."""
        simple_tqdm.update(1)
        assert simple_tqdm.start_time == 1000.0

    def test_update_increments_counter(self, simple_tqdm, mock_time):
        """Test update increments counter."""
        simple_tqdm.update(5)
        assert simple_tqdm.n == 5

    def test_update_calls_refresh(self, simple_tqdm, mock_time):
        """Test update calls refresh when enough time has passed."""
        simple_tqdm.last_print_time = 0
        with patch.object(simple_tqdm, 'refresh') as mock_refresh:
            simple_tqdm.update(1)
            mock_refresh.assert_called_once()

    def test_update_no_refresh_too_soon(self, simple_tqdm, mock_time):
        """Test update doesn't refresh if called too soon."""
        simple_tqdm.last_print_time = 999.95
        simple_tqdm.mininterval = 0.1
        with patch.object(simple_tqdm, 'refresh') as mock_refresh:
            simple_tqdm.update(1)
            mock_refresh.assert_not_called()

    def test_refresh_disabled(self, simple_tqdm_disabled):
        """Test refresh when disabled."""
        with patch.object(simple_tqdm_disabled, '_display') as mock_display:
            simple_tqdm_disabled.refresh()
            mock_display.assert_not_called()

    def test_refresh_calls_display(self, simple_tqdm, mock_time):
        """Test refresh calls _display."""
        with patch.object(simple_tqdm, '_display') as mock_display:
            simple_tqdm.refresh()
            mock_display.assert_called_once()

    def test_display_no_start_time(self, simple_tqdm):
        """Test _display when start_time is None."""
        simple_tqdm.start_time = None
        # Should not raise an exception
        simple_tqdm._display()

    def test_display_with_total(self, simple_tqdm_with_total, mock_time):
        """Test _display with total set."""
        simple_tqdm_with_total.start_time = 999.0
        simple_tqdm_with_total.n = 50
        simple_tqdm_with_total._display()

        output = simple_tqdm_with_total.file.getvalue()
        assert "50.0%" in output

    def test_display_without_total(self, simple_tqdm, mock_time):
        """Test _display without total."""
        simple_tqdm.start_time = 999.0
        simple_tqdm.n = 50
        simple_tqdm._display()

        output = simple_tqdm.file.getvalue()
        assert "50it" in output

    def test_display_with_description(self, mock_stderr, mock_time, clear_instances):
        """Test _display with description."""
        from hbutils.logging.progress import SimpleTqdm
        pbar = SimpleTqdm(desc="Processing", file=mock_stderr)
        pbar.start_time = 999.0
        pbar.n = 10
        pbar._display()

        output = pbar.file.getvalue()
        assert "Processing:" in output

    def test_create_activity_bar(self, simple_tqdm, mock_time):
        """Test _create_activity_bar."""
        simple_tqdm.start_time = 999.0
        result = simple_tqdm._create_activity_bar()
        assert result in ['|', '/', '-', '\\']

    def test_create_activity_bar_sets_start_time(self, simple_tqdm, mock_time):
        """Test _create_activity_bar sets start_time if None."""
        simple_tqdm.start_time = None
        simple_tqdm._create_activity_bar()
        assert simple_tqdm.start_time == 1000.0

    def test_format_time_seconds(self, simple_tqdm):
        """Test _format_time with seconds."""
        result = simple_tqdm._format_time(30.5)
        assert result == "30.50s"

    def test_format_time_minutes(self, simple_tqdm):
        """Test _format_time with minutes."""
        result = simple_tqdm._format_time(90)
        assert result == "01:30"

    def test_format_time_hours(self, simple_tqdm):
        """Test _format_time with hours."""
        result = simple_tqdm._format_time(3665)
        assert result == "01:01:05"

    def test_set_description(self, simple_tqdm):
        """Test set_description."""
        with patch.object(simple_tqdm, 'refresh') as mock_refresh:
            simple_tqdm.set_description("New desc")
            assert simple_tqdm.desc == "New desc"
            mock_refresh.assert_called_once()

    def test_set_description_no_refresh(self, simple_tqdm):
        """Test set_description without refresh."""
        with patch.object(simple_tqdm, 'refresh') as mock_refresh:
            simple_tqdm.set_description("New desc", refresh=False)
            assert simple_tqdm.desc == "New desc"
            mock_refresh.assert_not_called()

    def test_set_description_none(self, simple_tqdm):
        """Test set_description with None."""
        simple_tqdm.set_description(None)
        assert simple_tqdm.desc == ""

    def test_set_postfix(self, simple_tqdm):
        """Test set_postfix."""
        with patch.object(simple_tqdm, 'refresh') as mock_refresh:
            simple_tqdm.set_postfix(loss=0.5, accuracy=0.95)
            mock_refresh.assert_called_once()

    def test_set_postfix_no_refresh(self, simple_tqdm):
        """Test set_postfix without refresh."""
        with patch.object(simple_tqdm, 'refresh') as mock_refresh:
            simple_tqdm.set_postfix(loss=0.5, refresh=False)
            mock_refresh.assert_not_called()

    def test_close_disabled(self, simple_tqdm_disabled):
        """Test close when disabled."""
        simple_tqdm_disabled.close()  # Should not raise exception

    def test_close_with_leave(self, simple_tqdm):
        """Test close with leave=True."""
        simple_tqdm.leave = True
        with patch.object(simple_tqdm, 'refresh') as mock_refresh:
            simple_tqdm.close()
            mock_refresh.assert_called_once()

        output = simple_tqdm.file.getvalue()
        assert output.endswith("\n")

    def test_close_without_leave(self, simple_tqdm):
        """Test close with leave=False."""
        simple_tqdm.leave = False
        with patch.object(simple_tqdm, '_get_terminal_width', return_value=80):
            simple_tqdm.close()

        output = simple_tqdm.file.getvalue()
        assert " " * 80 in output

    def test_close_removes_from_instances(self, clear_instances):
        """Test close removes instance from global list."""
        from hbutils.logging.progress import SimpleTqdm
        pbar = SimpleTqdm()
        assert pbar in SimpleTqdm._instances
        pbar.close()
        assert pbar not in SimpleTqdm._instances

    def test_close_handles_missing_instance(self, simple_tqdm):
        """Test close handles case where instance is not in list."""
        from hbutils.logging.progress import SimpleTqdm
        SimpleTqdm._instances.clear()  # Remove manually
        simple_tqdm.close()  # Should not raise exception

    def test_clear_disabled(self, simple_tqdm_disabled):
        """Test clear when disabled."""
        simple_tqdm_disabled.clear()  # Should not raise exception

    def test_clear_clears_line(self, simple_tqdm):
        """Test clear clears the terminal line."""
        with patch.object(simple_tqdm, '_get_terminal_width', return_value=80):
            simple_tqdm.clear()

        output = simple_tqdm.file.getvalue()
        assert " " * 80 in output

    def test_write_with_lock(self, simple_tqdm):
        """Test write with lock."""
        with patch.object(simple_tqdm, 'clear') as mock_clear, \
                patch.object(simple_tqdm, 'refresh') as mock_refresh:
            simple_tqdm.write("Test message")
            mock_clear.assert_called_once()
            mock_refresh.assert_called_once()

        output = simple_tqdm.file.getvalue()
        assert "Test message\n" in output

    def test_write_without_lock(self, simple_tqdm):
        """Test write without lock."""
        simple_tqdm.write("Test message", nolock=True)
        output = simple_tqdm.file.getvalue()
        assert "Test message\n" in output

    def test_write_custom_file(self, simple_tqdm):
        """Test write to custom file."""
        custom_file = StringIO()
        simple_tqdm.write("Test message", file=custom_file, nolock=True)
        assert "Test message\n" in custom_file.getvalue()

    def test_write_custom_end(self, simple_tqdm):
        """Test write with custom end character."""
        simple_tqdm.write("Test message", end="!", nolock=True)
        output = simple_tqdm.file.getvalue()
        assert "Test message!" in output

    def test_tqdm_function_with_real_tqdm(self):
        """Test tqdm function when real tqdm is available."""
        from hbutils.logging.progress import tqdm

        # Mock the real tqdm
        mock_real_tqdm = MagicMock()
        with patch('hbutils.logging.progress._origin_tqdm', mock_real_tqdm):
            result = tqdm(range(10), desc="test")
            mock_real_tqdm.assert_called_once_with(
                iterable=range(10), desc="test", total=None, leave=True,
                file=None, ncols=None, mininterval=0.1, ascii=None,
                disable=False, unit='it', unit_scale=False, initial=0,
                position=None, unit_divisor=1000
            )

    def test_tqdm_function_without_real_tqdm(self, clear_instances):
        """Test tqdm function when real tqdm is not available."""
        from hbutils.logging.progress import tqdm, SimpleTqdm

        with patch('hbutils.logging.progress._origin_tqdm', None):
            result = tqdm(range(10), desc="test")
            assert isinstance(result, SimpleTqdm)
            assert result.desc == "test"
            assert result.total == 10

    def test_thread_safety(self, clear_instances):
        """Test thread safety of SimpleTqdm."""
        from hbutils.logging.progress import SimpleTqdm
        import threading

        results = []

        def create_progress_bar():
            pbar = SimpleTqdm(range(10), file=StringIO())
            for _ in pbar:
                pass
            results.append(pbar)

        threads = [threading.Thread(target=create_progress_bar) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(results) == 5

    def test_global_instances_management(self, clear_instances):
        """Test global instances list management."""
        from hbutils.logging.progress import SimpleTqdm

        pbar1 = SimpleTqdm()
        pbar2 = SimpleTqdm()

        assert len(SimpleTqdm._instances) == 2
        assert pbar1 in SimpleTqdm._instances
        assert pbar2 in SimpleTqdm._instances

        pbar1.close()
        assert len(SimpleTqdm._instances) == 1
        assert pbar2 in SimpleTqdm._instances

        pbar2.close()
        assert len(SimpleTqdm._instances) == 0
