
# Architecture
N/I is Not Implemented

## Signup
```
Token: Guest
                          POST             POST/GET       PUT       DELETE
                            |                 |            |           |
UI                        Signup             N/I          N/I         N/I
                            |                 |            |           |
Hapi Route                /signup POST       N/I          N/I         N/I
                            |                 |            |           |
Postgres Client           client.query       N/I          N/I         N/I
                            .                 .            .           .
                            .                 .            .           .
                            .                 .            .           .
API SQL Function          signup             N/I          N/I         N/I
                            |                 |            |           |
Static Base Function      insert            query        update      delete
                            |                 |            |           |
Static Base Table           +-----------------+------------+-----------+

```
## Signin
```
Token: Guest
                          POST             POST/GET       PUT       DELETE
                            |                 |            |           |
UI                         N/I              Signin        N/I         N/I          
                            |                 |            |           |
Hapi Route                 N/I           /signin POST     N/I         N/I
                            |                 |            |           |
Postgres Client            N/I           client.query     N/I         N/I
                            .                 .            .           .
                            .                 .            .           .
                            .                 .            .           .
API SQL Function          signup             N/I          N/I         N/I
                            |                 |            |           |
Static Base Function      insert            query        update      delete
                            |                 |            |           |
Static Base Table           +-----------------+------------+-----------+

```


## Users

Token: User

|   |   |   |   |   |
| ----- | ---- | ---- | --- | ------ |
| UI                   | Create | Read | Update  | Delete  |
| HTTP  | POST | GET | PUT | DELETE |
| Hapi Route           | -  | /user  | /user  | /user  |
| Postgres Client      | -  | query  | query  | query  |
| API SQL Function     | -  | user  | user  | user  |
| Static Base Function | -  | query  | update  | delete  |
| Static Base Table    | -  | one  | one  | one  |

* assume https is implemented

Token: Admin

|   |   |   |   |   |
| ----- | ---- | ---- | --- | ------ |
| UI                   | Create | Read | Update  | Delete  |
| HTTP  | POST | GET | PUT | DELETE |
| Hapi Route           | -  | /user  | -  | -  |
| Postgres Client      | -  | query  | -  | -  |
| API SQL Function     | -  | user  | -  | -  |
| Static Base Function | -  | query  | -  | -  |
| Static Base Table    | -  | one  | -  | -  |
