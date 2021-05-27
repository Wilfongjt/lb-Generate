
# Architecture

```
UI                 New User          Login             
                     |                 |
Hapi Route         /signup POST      /signup POST
                     |                 |       
Postgres Client    client.query      client.query
                     .                 .
                     .                 .
                     .                 .
API Function       signup            signin
                     |                 |
Base Function      insert            query        update      delete
                     |                 |            |           |
Base Table           +-----------------+------------+-----------+
```
```           POST                    GET/POST                    PUT                         DELETE
api_guest   /signup(text, json)     /signin(text, json)
api_user    /user(text, json)       /user(text, json, json)     /user(text, text, json)     /user(text, text)
```

