import pytest
import pandas as pd

def test_cleaning():
    df = pd.DataFrame({'a': [1, 2, None]})
    assert df.dropna().shape[0] == 2
