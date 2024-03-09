use std::sync::Arc;

use pyo3::{exceptions::PyValueError, prelude::*};

use arrow::{
    pyarrow::PyArrowType,
    array::{Array, ArrayData, Int32Array, make_array},
};


#[pyfunction]
fn max_pure(v: Vec<i32>) -> Option<i32> {
    v.into_iter().max()
}

#[pyfunction]
fn do_nothing(_v: Vec<i32>) -> Option<i32> {
    return Some(9999999);
}

// https://docs.rs/arrow/latest/arrow/pyarrow/index.html
#[pyfunction]
fn max_arrow(array: PyArrowType<ArrayData>) -> PyResult<Option<i32>> {
    let array = array.0; // Extract from PyArrowType wrapper
    let array: Arc<dyn Array> = make_array(array); // Convert ArrayData to ArrayRef
    let array: &Int32Array = array.as_any().downcast_ref()
        .ok_or_else(|| PyValueError::new_err("expected int32 array"))?;

    Ok(array.iter().max().expect("expected max in32"))
}

#[pymodule]
fn max_rust(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(max_pure, m)?)?;
    m.add_function(wrap_pyfunction!(do_nothing, m)?)?;
    m.add_function(wrap_pyfunction!(max_arrow, m)?)?;
    Ok(())
}
