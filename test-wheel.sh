#!/bin/sh

unset PYTHONPATH
rm -rf test-ve
python -m venv test-ve

(
    set -ex
    . test-ve/bin/activate
    pip install dist/*.whl
    pip install pytest
    pytest
) && rm -Rf test-ve

