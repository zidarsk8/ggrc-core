The uniformity of coding style in the front end isn't very good, and it will become more important as we bring on new people.  Hence, we should finally define and enforce a coding style guide.


Mostly cribbed relevant parts from https://github.com/airbnb/javascript and http://sideeffect.kr/popularconvention#javascript

The main departure from Airbnb is in making subordinate syntax elements always indented further than containing elements to maintain clear visual hierarchy.


General
----

Indentation is always 2 spaces, except to maintain alignment in `var` declarations and where clarity demands it.

Lines are maximum 80 characters.

Comments are on their own line, and should be limited to 80 characters per line.

"Module"-level blocks should be separated by 2 blank lines, and "class"-level blocks by 1 blank line.  (E.g., 2 blank lines between any two `can.Model.Cacheable(...)` definitions, and 1 blank line between methods inside the definition.

`FIXME:` and `TODO:` are both acceptable -- the first implies a bug, the second implies a feature/improvement.

Always use semicolons.

We should be compatible with `'use strict';`.


Variable naming
----

Use full/descriptive words.  `query` instead of `q`, `word_list` instead of `wl`, etc.

Use `$` as a prefix always and only for jQuery-valued variables.

Use `_` prefix for "private" variables.

`camelCase` or `underscore_case`?  The more-common Javascript convention is camelCase.  Our codebase is primarily underscore_case, except "classes" and interactions with other libraries.  I see this difference as positive, since it makes clearer what is our code vs. external code.  Thoughts?

this, that & self
----

Try to avoid using `var that = this` or `var self = this;` as much as possible. The preferred way is to call bind with this: `function () {}.bind(this)`.

Comma first/last
----

Sadly, though I prefer comma-first, new javascript files should use comma-last style.  Both styles should pay close attention to vertical alignment of similar syntax elements, as in the following examples.

Existing files with comma-first code should look like:

```javascript
var first = "Something"
  // Note, the comma is indented 2 spaces to make variable names align
  , second = {
      // Note the "extra" indentation to make the first key align with subsequent keys
      first_key: "Value"
    , second_key: "Value2"
    }
  , third = [
      // Again, note the extra indentation to make the elements align
      "first_element"
    , "second_element"
    ]
  , fourth
  , fifth
  , sixth
  // Note trailing semicolon on new line, parallel with commas.
  ;
```

Code in new files should look like:

```javascript
var first = "Something",
  second = {
    // Note "extra" indentation to not interrupt vertical alignment of "higher" variables
    // and to show contents are part of the containing element.
    first_key: "Value",
    // Note no final comma
    second_key: "Value2"
  },
  third = [
    "first_element",
    "second_element"
  ],
  // Final semicolon not on new line
  // Multiple un-initialized variables are okay on the last lines
  fourth, fifth, sixth;
```

(Regarding the "extra" indentation above -- the important part is that "deeper" elements (keys, array values, etc) are further indented than their containing elements.  Another option might be to use a separate `var` line for each declared variable.)


Operator spacing
-----

No space after function names, and no extra space around arguments:
```javascript
// bad
function foo ( arg1, arg2 ) {}

// good
function foo(arg1, arg2) {}

// bad anonymous function
function(arg1, arg2) {}

// good anonymous function
function (arg1, arg2) {}

```

No space before `:`:

```javascript
// no
var a = {
      first : "x"
    };

// yes
var a = {
      first: "x"
    };
```

Conditions must have a single space before the parentheses, and no space within the parentheses:

```javascript
// bad
if(true) {}

// bad
if ( true ) {}

// good
if (true) {}
```

`else` and `else if` and `catch` should be on the same line as the brackets:

(Note, I actually prefer the first style, but don't see it used anywhere...)

```javascript
// no
if (!instance) {
  something();
}
else {
  something_else();
}

// no
if (!instance)
{
  something();
}
else
{
  something_else();
}

// yes
if (!instance) {
  something();
} else if (something_else == 12) {
  something_else_entirely();
} else {
  something_third();
}
```

Statements should never be obfuscated by expressions, because it hide non-local effects. E.g. (from Google style guide).

```javascript
// Okay
if (node) {
  if (node.kids) {
    if (node.kids[index]) {
      foo(node.kids[index]);
    }
  }
}

// Better
if (node && node.kids && node.kids[index]) {
  foo(node.kids[index]);
}

// Bad
node && node.kids && node.kids[index] && foo(node.kids[index]);
```

Cleverness
-----

Conventions are better than cleverness.

Avoid complex logic in `var` lines.  I'm a big violator here, but if `var` definition is complex or order-dependent, we should probably just declare the variables and define/initialize them in separate statements.

No multiline or nested `? :` constructs.

Shout out:

```javascript
// tribute to Brad's love of LISP, but no
switch (true) {
  case !instance:
    something();
    break;
  case something_else == 12:
    something_else_entirely();
    break;
  default:
    something_third();
}

// yes
if (!instance) {
  something();
} else if (something_else == 12) {
  something_else_entirely();
} else {
  something_third();
}
```

Acceptable cleverness:  `~` and `!~` are acceptable for conditions using `indexOf` or `inArray`.
