# Calling Rust from Python

Quick exploration of using Rust for extending Python packages.

## Timings

See [test.py](test.py).

I felt it was interesting to compare different implementations of taking the maximum value of an
array. Some in Python and some through Rust.

```plain
Python max():      0.085s
Python for-loop:   0.161s
Rust max():        1.361s
Rust 'do nothing': 1.228s
Rust actual max(): 0.133s
Rust pyarrow:      0.359s
```

Note, calculating the maximum value in Rust is slow because the array data has to be converted and
copied.

### Running it yourself

```sh
python -m venv venv
source venv/bin/activate
maturin develop
python test.py
```

## Tools used

-   [pyo3](https://github.com/PyO3/pyo3)
-   [maturin](https://github.com/PyO3/maturin)
-   [pyarrow integration for Rust](https://docs.rs/arrow/latest/arrow/pyarrow/): "Pass Arrow objects
    from and to PyArrow"

## Helpful resources

-   [Rust in Python's Arrow revolution](https://www.datawill.io/posts/pandas-arrow-rust/)
