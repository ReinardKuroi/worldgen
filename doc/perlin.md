# Perlin noise using numpy

[**An image synthesizer** by Ken Perlin](http://www.cs.cmu.edu/afs/cs.cmu.edu/academic/class/15869-f11/www/readings/perlin85_imagesynthesizer.pdf)

Value noise is computed from pseudo-random gradient vector multiplication.
Therefore, it is possible to optimize some parts of it using vector operations.
Fading and normalizing is applicable to the position vectors themselves.
Dot product calculations are the obvious choice as well.