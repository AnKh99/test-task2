### Finding the smallest change in the initial set of data which results in different behavior

The tool is designed to find the least required change in a set of data that results in a different behavior for a
specific tool.

For example, let's say we have:

```text
- hello
- my
- name
- is
- grzegorz brzeczyszczykiewicz
```

We don't know the algorithm behind it, but a specific black box, given this set of data, returns 0 or 1 based on the
sequence of the element.\
We want to determine which elements are responsible for that.\
Let's assume that those are "my" and "is" elements. Having "is" after "my" leads to a working solution (e.g. 0 return
code), having them in another order - to failure (1 return code) =>

This would be OK (return code 0 as the original)

```text
- my
- is
- name
- hello
- grzegorz brzeczyszczykiewicz
```

This would be NOT OK (return code 1)

```text
- name
- grzegorz brzeczyszczykiewicz
- is
- hello
- my
```

Because "is" is before the "my".

To find a solution to that, a method similar to binary search will be used.

First of all, the data will be split into 4 pieces, and they will be shuffled (here is a way to increase performance,
don't use the first partition again, this yields no results, TODO subject for future optimization)

Broad search is used, where each used part is then partitioned again in four pieces and added to the end of the queue.

In this way, a part that contains S2 will be found quickly (hopefully).

When this happens, and a piece of data that contains S2 is before S1, the state changes.

When this happens, queue is erased, and this piece that is confirmed to have S2 in it is being placed in the rest of the
data with a binary approach. Details:

```text
[0, 1, S1, 3, 4, 5, 6, 7]
=>
[0, 1], [S1, 3], [4, 5], [6, S2]
=>
...
=>
[6, S2], [0, 1], [S1, 3], [4, 5]  // state change
=>
[6, S2] is confirmed to have S2, and everything else is confirmed to have S1.

Now [6, S2] will be inserted in the middle of the rest of the data, until another state change is reached.
First placement is at 0.5x of the total 1x of the rest of the elements
Second placement is at 0.75x of the total 1x of the rest of the elements
Third placement is at 0.875x of the total 1x of the rest of the elements
....

Let's say that on the third placement the state changed, it means that S1 is somewhere between Second and Third
placement, therefore between 0.5 and 0.75 of 1x of the elements that are not S2.

After that the recursion happens, and algorithm is called for this piece that has S1, and piece that has S2.
```

There are two interfaces, blackbox and file.

And currently there are two implementations, BlackboxS1S2 and FileJSON

FileJSON works with JSON

BlackboxS1S2 also works with JSON and for it S1 is "S1" and S2 is "S2". Refer to the tests to check more details.

To use it in Makefiles or in some other place, both interfaces IFile and IBlackbox must be implemented, and
after that only main.py needs to be changed.

## Running

`python3 run_tests.py`

Running main.py:
```sh
python3 main.py  --mode json --initial_filename initial_big_data.json --work_folder files --s1_key S1 --s2_key S2 --cleanup
```

or
```sh
python3 main.py  --mode makefile --initial_filename makefile_test.am --work_folder files --s1_key S1 --s2_key S2 --cleanup --blackbox_path check.sh
```

!!!! Running main.py is slow due to the printouts! Forward it into some file for better results!\
`python3 main.py > output.txt && tail -n5 output.txt`

```text
FOUND S1 and S2:  [1, 7498]
TOTAL COUNTER:  112
```

112 is for 10.000 entries, pretty good. Can be 25-50% faster if this first case is optimized, but some other time TODO