"""
Test errors of the interpreter (basic functions)
"""
from pathlib import Path

import pytest


from yamlpp import Interpreter, YAMLppError
from yamlpp.util import print_yaml

CURRENT_DIR = Path(__file__).parent 

SOURCE_DIR = CURRENT_DIR / 'Source'

def test_err_0():
    """
    Test first YAMLpp program with errors
    """
    FILENAME = SOURCE_DIR / 'test1.yaml'
    i = Interpreter()
    i.load(FILENAME)
    
    # rename key
    switch = i.initial_tree.server['.switch']
    switch['.cases2'] = switch.pop('.cases')

    

    with pytest.raises(YAMLppError) as e:
        tree = i.tree
    assert "not contain '.cases'" in str(e)
    assert "Line 9" in str(e)

