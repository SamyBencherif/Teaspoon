
# Teaspoon

### The minimal (usable) programming language

Teaspoon is designed to be the easiest language to implement that is also reasonable easy to code in.

For example languages like brainf*** are dead simple to implement, but are obscenely difficult to write code in.
Python or EMScript is quite easy to write code in but obscenely difficult to implement.

Teaspoon is a middle ground.

- [ ] Consider briefly if there is a way to merge implementations into a single codebase
- [ ] Optimize Heavily
- [ ] Swift / ObjC implementation


Optimizations

Argparse is run O(el) times when it could be run O(l) times.

where el is effective lines and l is lines.

ie in

```
for i in range(10):
    print(i)
```

there are 2 lines. but there are 21 effective lines!