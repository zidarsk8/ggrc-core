The query helper class will return the same query array with the key "ids"
in the top level of every query dictionary.

Advanced query calls have the following structure:

```
query = [
    {
        object_name: class name of the object we wish to retrieve
        filters: { dictionary describing the filter for the current object
            expression: {}
            order_by: []  not implemented yet
            limit: []  not implemented yet
        }
    },
    ...
]
```


expressions:

Simple expressions have the following structure

```
expression = {
    left: key
    op: {name: = , != , > , < , ~, !~ }
    right: value
}
```


#### example:
  get all programs with the title "Hello"

```python
query = [
    {
        "object_name": "Program",
        "filters": {
            "expression": {
                "left": "title",
                "op": {"name": "="},
                "right": "Hello",
            }
        }
    }
]
```


Advanced filters:

Filter also have AND and OR operators, so you can build any query as an AST.


Relevant filters:
these have a little different structure than other normal filters

```
expression = {
    op: {name: "relevant"},
    object_name: Class of the relevant object
    ids: []  mandatory but can be generated from slugs.
    slugs: [] if present, these slugs will be changed to ids and added to the
    ids list
}
```


Special cases in the relevant expression is when
  object\_name = "\_\_previous\_\_"

In that case the ids, will be used as an index in the query array, and the
relevant filter will check for mappings to any of the objects returned by the
query on that index. Slugs field is ignored if present.


#### example:
  get all Programs that have a mapped regulation with a slug "r-1" or "r-2"

```python
query = [
    {
        "object_name": "Program",
        "filters": {
            "expression": {
                "op": {"name": "relevant"},
                "object_name": "Regulation",
                "slugs": ["r-1", "r-2"],
            }
        }
    }
]
```


#### example:
  get the same programs as before, and all Contracts that are mapped to any of
  those programs and have the word "cat" in the description


```python
query = [
    {  # first query for fetching Programs
        "object_name": "Program",
        "filters": {
            "expression": {
                "op": {"name": "relevant"},
                "object_name": "Regulation",
                "slugs": ["r-1", "r-2"],
            }
        }
    },
    {  # second query for fetching Contracts
        "object_name": "Contract",
        "filters": {
            "expression": {
                "left": {
                    "op": {"name": "relevant"},
                    "object_name": "__previous__",
                    "ids": ["0"],
                },
                "op": {"name": "AND"},
                "right": {
                    "left": "description",
                    "op": {"name": "~"},
                    "right": "cat",
                },
            },
        }
    }
]
```

for more examples see: src/tests/ggrc/converters/test\_export\_csv.py
