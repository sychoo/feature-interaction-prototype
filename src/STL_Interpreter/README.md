# STL_Interpreter/
A standalone interpreter that parse, analyze and evaluate STL expressions

## Definition of STL
```
φ::=⊤|π|¬φ|φ1∧φ2 |φ1UIφ2 ,
```
```
signal = 
G[0, 10](DistanceToEnemyDrone > 3)

```
## To Do
main.py
- [ ] implement interpret function


## Install packages
- python3 -m pip install


## Structure
- Node
    - Stmt_List
    - Stmt
        - Expr
            - Val