# 0x00. Pagination
## Resources
### Read or watch:
- [REST API Design: Pagination](https://www.moesif.com/blog/technical/api-design/REST-API-Design-Filtering-Sorting-and-Pagination/#pagination)
- [HATEOAS](https://en.wikipedia.org/wiki/HATEOAS)
## Pagination
- Most endpoints that returns a list of entities will need to have some sort of pagination.
- Without pagination, a simple search could return millions or even billions of hits causing extraneous network traffic.
- Paging requires an implied ordering. By default this may be the item’s unique identifier, but can be other ordered fields such as a created date.
## Offset Pagination
- This is the simplest form of paging. Limit/Offset became popular with apps using SQL databases which already have LIMIT and OFFSET as part of the SQL SELECT Syntax. Very little business logic is required to implement Limit/Offset paging.
- Limit/Offset Paging would look like GET /items?limit=20&offset=100. This query would return the 20 rows starting with the 100th row.
### Example
(Assume the query is ordered by created date descending)
1. Client makes request for most recent items: GET /items?limit=20
2. On scroll/next page, client makes second request GET /items?limit=20&offset=20
3. On scroll/next page, client makes third request GET /items?limit=20&offset=40
As a SQL statement, the third request would look like:
```SQL
SELECT
    *
FROM
    Items
ORDER BY Id
LIMIT 20
OFFSET 40;
```
### Benefits
- Easiest to implement, almost no coding required other than passing parameters directly to SQL query.
- Stateless on the server.
- Works regardless of custom sort_by parameters.
### Downsides
- Not performant for large offset values. Let’s say you perform a query with a large offset value of 1000000. The database needs to scan and count rows starting with 0, and will skip (i.e. throw away data) for the first 1000000 rows.
- Not consistent when new items are inserted to the table (i.e. Page drift) This is especially noticeable when we are ordering items by newest first. Consider the following that orders by decreasing Id:
    1. Query GET /items?offset=0&limit=15
    2. 10 new items added to the table
    3. Query GET /items?offset=15&limit=15 The second query will only return 5 new items, as adding 10 new items moved the offset back by 10 items. To fix this, the client would really need to offset by 25 for the second query GET /items?offset=25&limit=15, but the client couldn’t possibly know other objects being inserted into the table.
- Even with limitations, offset paging is easy to implement and understand and can be used in applications where the data set has a small upper bounds.
## Keyset Pagination
Keyset pagination uses the filter values of the last page to fetch the next set of items. Those columns would be indexed.
### Example
(Assume the query is ordered by created date descending)
1. Client makes request for most recent items: GET /items?limit=20
2. On scroll/next page, client finds the minimum created date of 2021-01-20T00:00:00 from previously returned results. and then makes second query using date as a filter: GET /items?limit=20&created:lte:2021-01-20T00:00:00
3. On scroll/next page, client finds the minimum created date of 2021-01-19T00:00:00 from previously returned results. and then makes third query using date as a filter: GET /items?limit=20&created:lte:2021-01-19T00:00:00
```SQL
SELECT
    *
FROM
    Items
WHERE
  created <= '2021-01-20T00:00:00'
ORDER BY Id
LIMIT 20
``` 
### Benefits
- Works with existing filters without additional backend logic. Only need an additional limit URL parameter.
- Consistent ordering even when newer items are inserted into the table. Works well when sorting by most recent first.
- Consistent performance even with large offsets.
### Downsides
- Tight coupling of paging mechanism to filters and sorting. Forces API users to add filters even if no filters are intended.
- Does not work for low cardinality fields such as enum strings.
- Complicated for API users when using custom sort_by fields as the client needs to adjust the filter based on the field used for sorting.

Keyset pagination can work very well for data with a single natural high cardinality key such as time series or log data which can use a timestamp.
## Seek Pagination
- Seek Paging is an extension of Keyset paging. By adding an after_id or start_id URL parameter, we can remove the tight coupling of paging to filters and sorting. Since unique identifiers are naturally high cardinality, we won’t run into issues unlike if sorting by a low cardinality field like state enums or category name.
- The problem with seek based pagination is it’s hard to implement when a custom sort order is needed.
### Example
(Assume the query is ordered by created date ascending)
1. Client makes request for most recent items: GET /items?limit=20
2. On scroll/next page, client finds the last id of ‘20’ from previously returned results. and then makes second query using it as the starting id: GET /items?limit=20&after_id=20
3. On scroll/next page, client finds the last id of ‘40’ from previously returned results. and then makes third query using it as the starting id: GET /items?limit=20&after_id=40
- Seek pagination can be distilled into a where clause
```SQL
SELECT
    *
FROM
    Items
WHERE
  Id > 20
LIMIT 20
```
- The above example works fine if ordering is done by id, but what if we want to sort by an email field? For each request, the backend needs to first obtain the email value for the item who’s identifier matches the after_id. Then, a second query is performed using that value as a where filter.
- Let’s consider the query GET /items?limit=20&after_id=20&sort_by=email, the backend would need two queries. The first query could be O(1) lookup with hash tables though to get the email pivot value. This is fed into the second query to only retrieve items whose email is after our after_email. We sort by both columns, email and id to ensure we have a stable sort incase two emails are the same. This is critical for lower cardinality fields.
1.
```SQL
SELECT
    email AS AFTER_EMAIL
FROM
    Items
WHERE
  Id = 20
```
2.
```SQL
SELECT
    *
FROM
    Items
WHERE
  Email >= [AFTER_EMAIL]
ORDER BY Email, Id
LIMIT 20
```
### Benefits
- No coupling of pagination logic to filter logic.
- Consistent ordering even when newer items are inserted into the table. Works well when sorting by most recent first.
- Consistent performance even with large offsets.
### Downsides
- More complex for backend to implement relative to offset based or keyset based pagination
- if items are deleted from the database, the start_id may not be a valid id.
## Sorting
- Like filtering, sorting is an important feature for any API endpoint that returns a lot of data. If you’re returning a list of users, your API users may want to sort by last modified date or by email.
- To enable sorting, many APIs add a sort or sort_by URL parameter that can take a field name as the value.
- However, good API designs give the flexibility to specify ascending or descending order. Like filters, specifying the order requires encoding three components into a key/value pair.
### Example formats
- GET /users?sort_by=asc(email) and GET /users?sort_by=desc(email)
- GET /users?sort_by=+email and GET /users?sort_by=-email
- GET /users?sort_by=email.asc and GET /users?sort_by=email.desc
- GET /users?sort_by=email&order_by=asc and GET /users?sort_by=email&order_by=desc
### Multi-Column Sort
- It’s not recommended to use the last design where sort and order are not paired. You may eventually allow sorting by two or more columns:
```SQL
SELECT
    email
FROM
    Items
ORDER BY Last_Modified DESC, Email ASC
LIMIT 20
```
- To encode this multi-column sort, you could allow multiple field names such as:
    1. GET /users?sort_by=desc(last_modified),asc(email)
    2. GET /users?sort_by=-last_modified,+email
## HATEOAS
- Hypermedia as the engine of application state (HATEOAS) is a constraint of the REST software architectural style that distinguishes it from other network architectural styles.
- With HATEOAS, a client interacts with a network application whose application servers provide information dynamically through hypermedia. A REST client needs little to no prior knowledge about how to interact with an application or server beyond a generic understanding of hypermedia.
- By contrast, clients and servers in Common Object Request Broker Architecture (CORBA) interact through a fixed interface shared through documentation or an interface description language (IDL).
- The restrictions imposed by HATEOAS decouple client and server. This enables server functionality to evolve independently.
### Example
- A user-agent makes an HTTP request to a REST API through an entry point URL. All subsequent requests the user-agent may make are discovered inside the response to each request. The media types used for these representations, and the link relations they may contain, are part of the API. The client transitions through application states by selecting from the links within a representation or by manipulating the representation in other ways afforded by its media type. In this way, RESTful interaction is driven by hypermedia, rather than out-of-band information.
- For example, this GET request fetches an account resource, requesting details in a JSON representation:
```HTTP
GET /accounts/12345 HTTP/1.1
Host: bank.example.com
```
The response is:
```HTTP
HTTP/1.1 200 OK

{
    "account": {
        "account_number": 12345,
        "balance": {
            "currency": "usd",
            "value": 100.00
        },
        "links": {
            "deposits": "/accounts/12345/deposits",
            "withdrawals": "/accounts/12345/withdrawals",
            "transfers": "/accounts/12345/transfers",
            "close-requests": "/accounts/12345/close-requests"
        }
    }
}
```
- The response contains these possible follow-up links: POST a deposit, withdrawal, transfer, or close request (to close the account).
- As an example, later, after the account has been overdrawn, there is a different set of available links, because the account is overdrawn.
```JSON
HTTP/1.1 200 OK

{
    "account": {
        "account_number": 12345,
        "balance": {
            "currency": "usd",
            "value": -25.00
        },
        "links": {
            "deposits": "/accounts/12345/deposits"
        }
    }
}
```
- Now only one link is available: to deposit more money (by POSTing to deposits). In its current state, the other links are not available. Hence the term Engine of Application State. What actions are possible varies as the state of the resource varies.
- A client does not need to understand every media type and communication mechanism offered by the server. The ability to understand new media types may be acquired at run-time through "code-on-demand" provided to the client by the server.
