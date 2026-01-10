import datetime
import time
from typing import NamedTuple


class Time(NamedTuple):
    sec: int
    min: int
    hor: int
    day: int

    @classmethod
    def from_sec(cls, sec):
        min = hor = day = 0

        if sec >= 60:
            _, _sec = divmod(sec, 60)
            min += _
        if min >= 60:
            _, min = divmod(min, 60)
            hor += _
        if hor >= 24:
            _, hor = divmod(hor, 24)
            day += _

        return cls(
            sec, min, hor, day
        )

    @property
    def time_DHMS(self):
        """
        获取时间
        :return: 元组 (天, 时, 分, 秒)
        """
        return self.day, self.hor, self.min, self.sec

    @property
    def seconds(self):
        """
        获取秒数
        :return: 秒数
        """
        return self.day * 24 * 60 * 60 + self.hor * 60 * 60 + self.min * 60 + self.sec

    def __str__(self):
        return f"Day: {self.day}, {self.hor}:{self.min}:{self.sec}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.seconds})"


class Stopwatch:
    __slots__ = ('start_time', 'end_time', 'elapsed_time', 'running')

    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.elapsed_time = None

        self.running = False

    def start(self):
        self.start_time = time.time()
        self.running = True

    def stop(self):
        if not self.running:
            raise RuntimeError("Timer not running")

        self.running = False

        self.end_time = time.time()
        self.elapsed_time = Time(self.end_time - self.start_time)

        return self.elapsed_time


class IntervalRecorder:
    __slots__ = ('_last_time', '_running')

    def __init__(self):
        self._last_time = None
        self._running = False

    def start(self):
        self._last_time = time.time()
        self._running = True

    def record(self):
        res = time.time() - self._last_time
        self._last_time = time.time()
        return Time(res)

    def lap(self):
        return Time(time.time() - self._last_time)

    def stop(self):
        self._running = False


class DatetimeParser:
    __slots__ = ('_fmt',)

    def __init__(self, fmt):
        self._fmt = fmt

    def parse(self, time_str):
        return datetime.datetime.strptime(time_str, self._fmt)

    @property
    def fmt(self):
        return self._fmt
