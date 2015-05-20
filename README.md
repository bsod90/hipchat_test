Here's my solution to HipChat test assesment.

To install requirements run

```
$ pip install -r requirements.txt
```

To test the solution in terminal mode just run

```
$ ./parser.py
```

And follow on screen instructions.

*NOTE 1:* parse() result converted to JSON only at the printing stage while it was
required to return JSON. It just seems to be a bit more intuitive for me. 
Anyways, I hope it's really minor issue.


To run tests simply run
```
$ nosetests
```
