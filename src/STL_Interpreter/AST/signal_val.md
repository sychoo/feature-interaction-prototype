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
G[1, 3]($param > 0)(0, signal_1)
```

- in this STL expression, `$param` refers to all values corresponding to the `"param"` key in the signal JSON value. Internally in the interpreter, it will compare all values corresponding to the `"param"` key to the right hand side of the comparison, in this case, value `0`.
