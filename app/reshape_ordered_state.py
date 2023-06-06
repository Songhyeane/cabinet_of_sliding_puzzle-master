from algorism import sliding_puzzle as sp
from alogorism1 import sliding_puzzle as sp1
import sys

def get_order(init_shape,order_shape):
    input=sys.argv[1:]
    order=sp.main(input,init_shape,order_shape)
    return order

def get_order_1(init_shape,order_shape):
    input=sys.argv[1:]
    order=sp1.main(input,init_shape,order_shape)
    return order

#print(get_order('6 7 8 3 4 5 0 1 2','6 7 8 0 3 5 4 2 1'))