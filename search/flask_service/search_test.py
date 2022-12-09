#!/usr/bin/env python3
import search
import pytest
from hypothesis import given, strategies as st

@given(st.integers())
def test_show(x):
    assert int(search.show(x)) == x

# Testing various properties for the Hamming distance
class TestHamming:

    # v1 = v2 <=> d(v1,v2) = 0
    @given(st.integers(min_value=0),st.integers(min_value=0))
    def test_separation2(self,v1,v2):
        print("(len(v1)="+str(bin(v1))+",len(v2)="+str(bin(v2)))
        try :
            assert (search.hamming_distance(str(bin(v1)),str(bin(v2))) == 0) != (v1 != v2)
        except ValueError :
            assert len(bin(v1)) != len(bin(v2))

if __name__ == "__main__":
    test_show()
