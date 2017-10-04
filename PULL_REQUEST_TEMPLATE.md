# Issue description

*Explain the issue your changes solve.*

# Steps to reproduce

*Include steps to reproduce the issue (if applicable).*

# Solution description

*Briefly explain the solution or add a link to the technical design document (this will help the reviewer confirm the code does what you intend).*

# Sanity checklist

- [ ] I have clicked through the app to make sure my changes work and not break the app.
- [ ] I have applied the correct milestone and labels.
- [ ] My changes fix the issue described in the description (and do nothing else). 🤞
- [ ] My changes are covered by tests.
- [ ] My changes follow our [performance guidelines](https://github.com/google/ggrc-core/blob/dev/docs/source/guidelines/performance.rst).
- [ ] My changes follow our [js](https://github.com/google/ggrc-core/blob/dev/docs/source/guidelines/javascript.rst) and/or [python](https://github.com/google/ggrc-core/blob/dev/docs/source/guidelines/python.rst) guidelines.
- [ ] My commits follow our [commit guidelines](https://github.com/google/ggrc-core/blob/dev/docs/source/guidelines/git/how_to_write_a_commit_message.rst).

<!-- If your PR includes a migration include the additional checklist items
# Migration checklist
- [ ] db_reset runs without errors or warnings.
- [ ] db_reset ggrc-qa.sql runs without errors or warnings.
-->

# PR Review checklist

- [ ] The solution description matches the changes in the code.
- [ ] There is no apparent way to improve the performance of the new code.
- [ ] There is no apparent way to improve the design of the new code.
- [ ] The changes fix the issue and don't cause any apparent regressions.
- [ ] The pull request is opened against the correct base branch.
- [ ] Labels and milestone are correctly set.
- [ ] Upon merging, the Jira ticket's fixversion is correctly set and the ticket is moved to "QA - In Progress".

<!-- If your code is not finished yet can include a TODO check list
# TODO

- [ ] First item on the TODO
-->
