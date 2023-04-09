from algorism import sliding_puzzle as sp
import sys

def bis(prev_state):
    input=sys.argv[1:]
    init_state = '8 7 6 1 2 5 0 3 4'
    order=sp.main(input,prev_state,init_state)
    print()
    #print(order)
    return order

print()
print(bis('8 7 6 5 4 3 2 1 0'))