# How to Write a Git Commit message

This is all shamelessly based on [chris.beams.io](http://chris.beams.io/posts/git-commit/).

1. Separate subject from body with a blank line
2. Limit the subject line to 50 characters
3. Capitalize the subject line
4. Do not end the subject line with a period
5. Use the imperative mood in the subject line (spoken or written as if giving a command or instruction)
6. Wrap the body at 72 characters
7. Use the body to explain what and why vs. how

A properly formed git commit subject line should always be able to complete the following sentence:

**If applied, this commit will _your subject line here_**

Good: If applied, this commit will **refactor subsystem X for readability**

Bad: If applied, this commit will **fixes for broken stuff**

Commit message should be summary line and description of what you have done in the imperative mode, that is as if you were commanding someone. Write "fix", "add", "change" instead of "fixed", "added", "changed".

Examples:

#### Bad
1. Fixed bug with {something}.
2. changing behavior of {something}
3. more fixes for broken stuff
4. sweet new API methods
5. Removing stuff

#### Good
1. Fix bug when {something_else} doesn't exist
2. Change behavior of {something} to do {behavior_x}
3. [don't do this, fix one specific thing in a commit]
4. Add {method_a}, {method_b} and {method_c} methods to API
5. Remove unused {method_a}, {method_b}...


# Pull request titles

For pull request titles we should use the same rules as for the subject line of a commit, but we need to prefix the issue id (or QUICK-FIX or DOCS if there is no issue id).

Examples:

```
CORE-9999 Fix performance issues on bulk operations
QUICK-FIX Prevent breaking tasks into multiple lines
DOCS Add section that explains client side mappings
```
