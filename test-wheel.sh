#!/bin/sh

@echo on

unset PYTHONPATH
rm -rf test-ve
python -m venv test-ve
. test-ve/bin/activate
pip install dist/*.whl
pip install pytest
pytest
deactivate
# rm -rf test-ve

