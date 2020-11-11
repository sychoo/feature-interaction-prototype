# Documentation for Signal Val

## Standard Format
- A signal must be JSON format wrapped around by a pair of $ (dollar sign) like the one as follows

```JSON
${
        "1": {
                "content": {
                        "param": 7
                }
        },

        "2": {
                "content": {
                        "param": 10
                }
        },

        "3": {
                "content": {
                        "param": 15
                }
        }
}$
```


We can assign this signal to a variable using either `val` or `var` declarations as follows

```scala
val signal = ${
        "1": {
                "content": {
                        "param": 7
                }
        },

        "2": {
                "content": {
                        "param": 10
                }
        },

        "3": {
                "content": {
                        "param": 15
                }
        }
}$
```


- A meta-variable refers to a variable that represent a list of values. For example, in the following expression: 


```php
G[1, 3]($param > 0)(0, signal_1) // true
```

- in this STL expression, `$param` refers to all values corresponding to the `"param"` key in the signal JSON value. Internally in the interpreter, it will compare all values corresponding to the `"param"` key to the right hand side of the comparison, in this case, value `0`.


- When meta-variable occurs on both side of the comparison, as follows
```php
G[1, 3]($param == $param)(0, signal_1) // true
```

- the meta-variable will only be compared on individual time level, in this case, for time 1, time 2 and time 3, respectively


- STL script also supported nested level signals as follows, you can simply retrieve the values using mete-variables written like $a.b (access (dot) semantics)

```scala
val signal_3 = ${
        "1": {
                "content": {
                        "ego": {
                                "param": 7
                        },

                        "enemy": {
                                "param": 8
                        }

                }
        },

        "2": {
                "content": {
                        "ego": {
                                "param": 10
                        },

                        "enemy": {
                                "param": 11
                        }
                }
        },

        "3": {
                "content": {
                        "ego": {
                                "param": 15
                        },

                        "enemy": {
                                "param": 16
                        }
                }
        }
}$

println G[1, 3]($ego.param < 0)(0, signal_3) // false
println G[1, 3]($ego.param < $enemy.param)(0, signal_3) // true
```