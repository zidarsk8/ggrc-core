# Advanced query API

Quick overview of the expected advanced API behaviour.

API endpoint should be `/query` and in the future it should replace the current
`/search`. Due to expected bigger queries it should listen for both GET or POST
requests.

Payload of the advanced query should contain an array of queries.

```python
request = [
  {...}, # query 1
  {...}, # query 2
  {...}, # query 3
  ...
]
```
Results for such request will be an array of objects, where each contains results of the query

```python
result = [
  {...}, # response to query 1
  {...}, # response to query 2
  {...}, # response to query 3
  ...
]
```

## query structure

In this section we will assume that the request has the following structure with a single query
and all results will be for it.
```python
request = [ query ]
```

All queries have a query type which can be: list (default), count, join.
If query type is not specified the list type will be used.

- list: most basic query returning a list of results
- join: Basically same as the list, but each value can contain a response to a join subquery
- count: Returns only the number of matched items.

### basic query

The most simple query that will return empty results looks like
```python
query = {
    "object_type": "<object type>",
}
```
result:
```python
result = [{
    "<object type>": {
        "order": [],
        "count": 0,
        "values": {}
    }
}]
```

### filtered query

#### list

To get any results from the query, we need to add a filter with an expression. 
An empty expression will match all objects of a certain type.
```python
query = {
    "object_type": "<object type>",
    "expression": {},
}
```
is the same as 
```python
query = {
    "object_type": "<object type>",
    "expression": {},
    "type": "list"
}
```
result:
```python
result = [{
    "<object type>": {
        "order": [ ... ], # list of ids in the selected order
        "count": X, # number of results  
        "values": {
            a: none,
            b: none,
            c: none,
            ...
        }
    }
}]
```

#### count

count queries - the result object will only return the number matched items.
```python
query = {
    "object_type": "<object type>",
    "expression": {},
    "type": "count"
}
```
result:
```python
result = [{
    "<object type>": {
        "count": X, # number of results  
    }
}]
```

#### join

join queries - left join on relationships
```python
query = {
    "object_type": "<object type>",
    "expression": {},
    "type": "join"
    "join": {
        "query": {
            "object_type": "<object type 2>",
          	"expression": {}
        },
        "on": [0] 
    }
}
```
result:
```python
result = [{
    "<object type>": {
        "order": [ ... ], # list of ids in the selected order
        "count": X, # number of results  
        "values": {
            a: {
                "<object type 2>": {
                    "order": [ ... ],
                    "count": Y,
                    "values": {
                        ...
                    }
                }
            },
            b: {
                "<object type 2>": {
                    "order": [ ... ],
                    "count": Z,
                    "values": {
                        ...
                    }
                }
            },
            ...
        }
    }
}]
```

### Combined queries

If you have the same filter expression for multiple object, you can combine them in a single query.

Example for getting counts of objects in the left hand nave (with or without a filter)

```python
query = {
    "object_type": ["<object type 1>", "<object type 2>", ... ],
    "expression": {},
    "type": "count"
}
```
result:
```python
result = [{
    "<object type 1>": {
        "count": X, # number of results  
    },
    "<object type 2>": {
        "count": X, # number of results  
    },
    ...
}]
```




### Filter expressions

The filter expression has the basic with left side, operator and right side.

```python
expression = {
    "left": <literal or another expression>,
    "op": { "name": "<operator name>" },
    "right": <literal or another expression>,
}
```

There are two main groups of operators. Operators for expressions and operators for literals.
- Operators for literals are
  - ue
  - equals `=`
  - not equals `!=`
  - contains `~`
  - does not contain `!~`
  - greater than `>`
  - less than `<`
  - relevant `relevant` - special for "relevant to" filters. 
- Operators for expressions:
  - OR
  - AND

#### relevant expressions

There are two main cases of relevant expressions. Both expressions are used to get an object type and ids to which the current object should be relevant.

- first is where we specify the relevant to object\_type and ids

```python
expression = {
    "left": "<object type>",
    "op": { "name": "<operator name>" },
    "right": [ ... ],  # list of ids
}
```

- second relevant expression can only be used when there are multiple queries. It is used with a special keyword `__previous__`. Here the right part of the expression specifies the zero based index of the query  in the request. Instead of specifying object type and ids, we specify a query and use object type and ids from that query. 

```python
request = [
    { ... }, # query 0
    { ... }, # query 1
    { ... }, # query 2 
    
    {
      	"object_type": "<object type>",
    	"filter": {
        	"expression": {
        
    			"left": "__previous__",
    			"op": { "name": "<operator name>" },
    			"right": <zero based index of the previous query>, 
        },
    },  
]
```



## Full example

### Request

```python
request = [
    # Part 1: get all documentation requests that haven't been verified,
    # and are related to a PCI program and its Audits.
    {
        "object_type": "Program",
        "expression": {
            "left": "title",
            "op": {"name": "="},
            "right": "PCI"
        },
        "type": "join",
        "join": {
            "query": {
                "object_type": "Audit",
                "expression": {}
                "type": "join",
                "join": {
                    "query": {
                        "object_type": "Request",
                        "expression": {
                            "left": {
                                "left": "response type",
                                "op": {"name": "="},
                                "right": "Documentation",
                            },
                            "op": {"name": "AND"},
                            "right": {
                                "left": "status",
                                "op": {"name": "!="},
                                "right": "Verified",
                            },
                        },
                    },
                    "on": [0, 1]
                },
            },
            "on": [0],
        },
    },

    # Part 2: Get counts for all Sections and Regulations related to Clauses.
    # Used for displaying "expand arrows" in tree views.
    {
        "object_type": "Clause",
        "expression": {},
        "type": "join",
        "join": {
            "query": {
                "object_type": ["Section", "Regulation"],
                "expression": {}
                "type": "count",
            },
            "on": [0]
        }
    },

    # Part 3: multiple groups, used in import export
    {
        "object_type": "Clause",
        "expression": {
            "left": "title",
            "op": {"name": "~"},
            "right": "example"
        },
    },
    {
        "object_type": "Section",
        "expression": {
            "left": "__previous__",
            "op": {"name": "relevant"},
            "right": 2
        },
    },
    {
        "object_type": "Regulation",
        "expression": {
            "left": {
                "left": "__previous__",
                "op": {"name": "relevant"},
                "right": 2
            },
            "op": {"name": "AND"},
            "right": {
                "left": {
                    "left": "__previous__",
                    "op": {"name": "relevant"},
                    "right": 3
                },
                "op": {"name": "AND"},
                "right": {
                    "left": {
                        "left": "Program",
                        "op": {"name": "relevant"},
                        "right": [4, 55, 96],
                    },
                    "op": {"name": "AND"},
                    "right": {
                        "left": "owners",
                        "op": {"name": "~"},
                        "right": "someone",
                    },
                },
            },
        },
    }
]
```

### result:

```python
result = [
    # Part 1
    {
        # Program with "PCI" in the title.
        "Program": {
            "order": [25],
            "count": 1,
            "values": {
                25: {
                    # Audits that are related to Program 25.
                    "Audit": {
                        "order": [5, 7, 1],
                        "count": 3,
                        "values": {
                            1: {
                                # Requests that are related to Audit 1 and
                                # Program 25.
                                "Request": {
                                    "order": [12, 55, 10],
                                    "count": 3,
                                    "values": {
                                        12: None,
                                        10: None,
                                        55: None,
                                    }
                                }
                            },
                            5: {
                                "Request": {
                                    "order": [],
                                    "count": 0,
                                    "values": {},
                                },
                            },
                            7: {
                                "Request": {
                                    "order": [55],
                                    "count": 1,
                                    "values": {
                                        55: None,
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
    },

    # Part 2
    {
        # All clauses
        "Clause": {
            "order": [5, 4, 75, 126, 7],
            "count": 5,
            "values": {
                4: {
                    # Number of sections related to clause 4.
                    "Section": {
                        "count": 71,
                    },
                    "Regulation": {
                        "count": 8,
                    }
                },
                5: {
                    "Section": {
                        "count": 1,
                    },
                    "Regulation": {
                        "count": 0,
                    }
                },
                75: {
                    "Section": {
                        "count": 12,
                    },
                    "Regulation": {
                        "count": 9,
                    }
                },
                7: {
                    "Section": {
                        "count": 36,
                    },
                    "Regulation": {
                        "count": 5,
                    },
                },
                126: {
                    "Section": {
                        "count": 108,
                    },
                    "Regulation": {
                        "count": 142,
                    },
                },
            },
        },
    },

    # Part 3

    # Clauses with the string "example" in the title
    {
        "Clause": {
            "order": [4, 8],
            "count": 2,
            "values": {
                4: None,
                8: None,
            }
        }
    },

    # sections that are related to Clauses with ids 4 or 8
    {
        "Section": {
            "order": [7, 8, 2, 19],
            "count": 4,
            "values": {
                2: None,
                7: None,
                8: None,
                19: None,
            }
        }
    },

    # Regulations that are related to: any of the Clauses [4, 8] AND any of the
    # Sections [7, 8, 2, 19] AND any of the Programs [4, 55, 96] AND has an
    # owner with the string "someone" in the name or email.
    {
        "Regulation": {
            "order": [14, 11, 2, 19, 108],
            "count": 4,
            "values": {
                2: None,
                11: None,
                14: None,
                19: None,
                108: None,
            }
        }
    },
]
```

