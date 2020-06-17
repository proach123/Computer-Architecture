

"""Main."""

import sys
from cpu import *

cpu = CPU()

if len(sys.argv) > 1:
    print(sys.argv[1])
    cpu.load(sys.argv[1])
    cpu.run()
else:
    print('requires an argument.')


# "\Users\patri\Desktop\python\week-6\Computer-Architecture\ls8\examples\call.ls8"
# Example of how to run a file off the args
# 

# cpu.load()
# cpu.run()
