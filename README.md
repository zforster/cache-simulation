# Cache Simulation - Operating Systems Assessment
A program to simulate a cache on given files using the least recently used (LRU) replacement strategy.

# Input
The first line describes the cache. Each of the following lines describes a memory access.

The cache is described by four integers:

W is the number of bits in one word. 

C is the number of data bytes in the cache. 

B is the number of bytes in one cache block.

k is the number of lines in a block. 

All W, C, B and k will be positive integers. 

Each memory access is described by one address, which is a W-bit integer.

# Output
For each memory access in the input, print 'C' if it is served by the cache, and print 'M' if it is served by the memory.
