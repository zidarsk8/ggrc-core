Performance
===========

When reviewing a pull request we must always check for potential performance issues and bottlenecks. Note that we should try to stick to these guidelines also when writing the code.



Here are a few general things we should pay attention to:

- Avoid searching for multiple items in a list. This can always be avoided by using a js object, or a python set or a python dict.
- When working with multiple objects, preprocessing is a good way of simplifying and speeding up operations.

For the frontend part:

- Avoid fetching data that is not needed

  - Always first check the frontend cache if the data is available and only then fetch it from the backend. Note that in some cases the frontend cache should be avoided, such as, opening a modal window or opening an assessment info pane.
  - Check if the required data has already been sent with any of the other requests (assignees of an assessment are sent with the assessment and do not need to be fetched again.
  - When using the query API try to include all queries in a single request.

- Reduce the amount of data that is fetched. Some of these might need additional work on the backend, but mostly that will be less expensive than a full additional request. Examples would be:

  - Avoid fetching entire objects to read a single property (fetching an Audit to get the audit folder)
  - Fetching the original snapshot object just to check if it exists.


For the backend part:

- Aim to have only constant number of sql queries for every request.
- Check for proper use of eager query and index query.
- Avoid fetching any data from database if ORM has already eagerly loaded it.
- Avoid fetching too much data from database if it is not needed. That means to
  manually write a query with deferred options and joined loads when possible.
- Always take an entire request cycle into consideration. Optimizing one
  smaller function at the expense of other functions needed to do the same work
  but possibly multiple times may not be good. Any optimizations done must
  affect the entire app performance in a positive way overall.
- Avoid using object ids for mappings and use the ORM mapper instead. If we use
  ids, we have to rely on flushes inside of a single request and then we have
  workarounds for imports and bulk operations. Avoiding use of direct ids
  allows simpler code where multiple db operations can be joined together.



Checking for improvements and regressions
-----------------------------------------

When checking for any performance changes we must make sure to use as similar
environment as possible. Time measurements on their own do not prove better
or worse performance, we must always provide a comparison of before and after.

When doing performance checks we must pay attention to:

- Amount of data on both instances that are being compared.
- Whether or not memcache is enabled or disabled.
- If there are migrations between compared instances we must use the data on
  older migration as a benchmark. All increase or decrease of data made in
  a migration must be part of the comparison.
- Which user we are testing under: His global role, and amount of ACL entries
  for that user. Most of the time it should be enough to test under an Admin
  user and Global creator user, both with more than 100k ACL entries.

There are also two types of performance checks:

1. Single action performance: this can be a single REST request, or a single
   sql query, or single function execution.

2. User flow performance: this is a set of actions that a user might perform.

Difference between those two is that past actions might affect the performance
of future actions.

Few examples on what to watch for:

1. If we're measuring performance of adding a comment on an assessment: 

  - Adding a comment right after opening an assessment is not the same as 
    opening an assessment and waiting on all other background requests to 
    finish first before adding a comment.

  - Adding a comment after opening an assessment waiting on everything to 
    finish is not always the same as adding a comment after adding an URL to 
    an assessment and waiting on all requests to finish. In the first case
    permissions will be cached in memcache after opening an assessment, in the
    second case adding a URL creates a mapping and that flushes memcache so 
    performance for the same action will take longer.


