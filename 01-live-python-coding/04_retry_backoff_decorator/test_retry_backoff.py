from unittest.mock import MagicMock, patch

try:
    import pytest
    raises = pytest.raises
except ImportError:
    from contextlib import contextmanager
    @contextmanager
    def raises(expected_exception):
        class ExcInfo:
            value = None
        info = ExcInfo()
        try:
            yield info
            raise AssertionError(f"Expected exception {expected_exception.__name__} was not raised")
        except expected_exception as e:
            info.value = e

from retry_backoff import retry_with_backoff


class TransientNetworkError(Exception):
    pass


class FatalDatabaseError(Exception):
    pass


def test_success_on_first_try():
    mock_func = MagicMock(return_value="OK")
    decorated = retry_with_backoff(max_retries=3)(mock_func)

    result = decorated()
    assert result == "OK"
    assert mock_func.call_count == 1


def test_retry_eventual_success():
    # Fails twice, succeeds on 3rd attempt
    mock_func = MagicMock(
        side_effect=[
            TransientNetworkError("Network glitch 1"),
            TransientNetworkError("Network glitch 2"),
            "Recovered",
        ]
    )

    with patch("time.sleep") as mock_sleep:
        decorated = retry_with_backoff(
            max_retries=3,
            initial_delay=1.0,
            jitter=False,
            retryable_exceptions=(TransientNetworkError,),
        )(mock_func)

        res = decorated()
        assert res == "Recovered"
        assert mock_func.call_count == 3
        assert mock_sleep.call_count == 2
        # Checks backoff: attempt 1 -> 1.0s, attempt 2 -> 2.0s
        mock_sleep.assert_any_call(1.0)
        mock_sleep.assert_any_call(2.0)


def test_fatal_error_not_retried():
    mock_func = MagicMock(side_effect=FatalDatabaseError("Fatal"))
    decorated = retry_with_backoff(
        max_retries=3, retryable_exceptions=(TransientNetworkError,)
    )(mock_func)

    with raises(FatalDatabaseError):
        decorated()

    assert mock_func.call_count == 1  # Should not retry fatal exceptions


def test_exceeded_max_retries():
    mock_func = MagicMock(side_effect=TransientNetworkError("Always fails"))
    with patch("time.sleep"):
        decorated = retry_with_backoff(
            max_retries=2, retryable_exceptions=(TransientNetworkError,)
        )(mock_func)

        with raises(TransientNetworkError):
            decorated()

        # initial try + 2 retries = 3 calls
        assert mock_func.call_count == 3
