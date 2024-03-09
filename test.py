import pyarrow as pa

import max_rust

class Stopwatch:
    def __init__(self, timer=None):
        if timer is None:
            from timeit import default_timer as timer
        self.timer = timer
        self._start = self._end = self._elapsed = None

    def __enter__(self):
        self._start = self.timer()
        return self

    def __exit__(self, *args):
        self._end = self.timer()

    @property
    def elapsed(self):
        assert self._end is not None and self._start is not None
        return self._end - self._start


def max_for_loop(lst):
    ans = -1
    for elt in lst:
        if elt > ans:
            ans = elt
    return ans


def main():
    N = int(1e7)
    lst = list(range(N))

    with Stopwatch() as sw:
        x = max(lst)
        assert x == N - 1
    print(f"Python max(): {sw.elapsed:10.3f}s", flush=True)

    with Stopwatch() as sw:
        x = max_for_loop(lst)
        assert x == N - 1
    print(f"Python for-loop: {sw.elapsed:7.3f}s", flush=True)

    with Stopwatch() as sw:
        x = max_rust.max_pure(lst)
        assert x == N - 1
    print(f"Rust max(): {sw.elapsed:12.3f}s", flush=True)
    pure_rust = sw.elapsed

    with Stopwatch() as sw:
        x = max_rust.do_nothing(lst)
        assert x == N - 1
    print(f"Rust 'do nothing': {sw.elapsed:2.3f}s", flush=True)
    nothing = sw.elapsed

    print(f"Rust actual max(): {pure_rust - nothing:2.3f}s")

    lst_pa = pa.array(lst, type=pa.int32())
    with Stopwatch() as sw:
        x = max_rust.max_arrow(lst_pa)
        assert x == N - 1
    print(f"Rust pyarrow: {sw.elapsed:10.3f}s", flush=True)


if __name__ == "__main__":
    main()
