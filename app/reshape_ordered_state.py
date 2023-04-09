from algorism import sliding_puzzle as sp
import sys

def get_order(init_shape,order_shape):
    input=sys.argv[1:]
    order=sp.main(input,init_shape,order_shape)
    #print()
    #print(order)
    return order

#print(get_order('6 7 8 3 4 5 0 1 2','6 7 8 0 3 5 4 2 1'))