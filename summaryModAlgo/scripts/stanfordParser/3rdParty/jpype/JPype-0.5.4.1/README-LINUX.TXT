This release include preliminary support for linux.

In order to compile the source, distribution, you need to make the 2 following changes :

1) in setup.py, change the line 19 to reflect the path to YOUR JDK installation

Also, even if you do install from binary, you have to make the following change after installing.

in the file jpype/_copy.py, at line 33, change to reflect the path to YOUR JDK installation

These two steps are temporary, and should disappear before the 0.3 final.

There is one additional problem with jpype and linux. You can more about it and a solution in the examples/linux directory.
