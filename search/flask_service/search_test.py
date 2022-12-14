#!/usr/bin/env python3
import search
import pytest
import random
from hypothesis import given, strategies as st

@given(st.integers())
def test_show(x):
    assert int(search.show(x)) == x

# Testing various properties for the Hamming distance
class TestHamming:

    # v1 = v2 <=> d(v1,v2) = 0
    @given(st.integers(min_value=0),st.integers(min_value=0))
    def test_separation(self,v1,v2):
        try :
            # Vectors are either different or their distance is 0
            assert (search.hamming_distance(str(bin(v1)),str(bin(v2))) == 0) != (v1 != v2)
        # Also testing ValueError exception
        except ValueError :
            assert len(bin(v1)) != len(bin(v2))
    
    @given(st.integers(min_value=0),st.integers(min_value=0))
    def test_symmetry(self,v1,v2):
        try :
            # Vectors can be mirrored in the function
            assert search.hamming_distance(str(bin(v1)),str(bin(v2))) == search.hamming_distance(str(bin(v2)),str(bin(v1)))
        # Also testing ValueError exception
        except ValueError :
            assert len(bin(v1)) != len(bin(v2))
    

    @given(st.integers(min_value=0),st.integers(min_value=0),st.integers(min_value=0))
    def test_triangle_inequality(self,v1,v2,v3):
        try :
            # d(a,c) <= d(a,b)+d(b,c)
            assert search.hamming_distance(str(bin(v1)),str(bin(v3))) <= search.hamming_distance(str(bin(v1)),str(bin(v2))) + search.hamming_distance(str(bin(v2)),str(bin(v3)))
        # Also testing ValueError exception
        except ValueError :
            assert (len(bin(v1)) != len(bin(v2))) | (len(bin(v2)) != len(bin(v3))) | (len(bin(v1)) != len(bin(v3)))
    
# Testing KNN
#class TestKNN:
#    NB_FEATURES = 40
#    DB_SIZE = 200_000
#
#    def test_binary(self):
#        DB = [''.join(map(str, [random.randint(0, 1) for j in range(self.NB_FEATURES)])) for k in range(self.DB_SIZE)]
#        KNN_improved()

    

if __name__ == "__main__":
    test_show()
