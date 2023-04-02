import time


class Timer:
    def __init__(self):
        self._elapsed_time_sec: float = 0

    def elapsed_ms(self) -> int:
        return int(self._elapsed_time_sec * 1000)

    def elapsed_sec(self) -> float:
        return self._elapsed_time_sec

    def __enter__(self):
        self._start_time: float = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._elapsed_time_sec = time.perf_counter() - self._start_time

    def __call__(self) -> str:
        return f"{self.elapsed_ms()} ms"
