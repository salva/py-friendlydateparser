#!/bin/sh

@echo on

unset PYTHONPATH
rm -rf dist
python -m venv test-ve
. test-ve/bin/activate
pip install dist/*.whl
pytest
deactivate
# rm -rf test-ve

