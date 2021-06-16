# API Architectures
Date: 2021-05-30 13:50:16.455084
Sources:
 
## user
 
|  |  |  |  |  |
|  -  |  -  |  -  |  -  |  -  |
| UI | Create | Read | Update | Delete |
| HTTP | POST | GET | PUT | DELETE |
| Routes | /user | /user | /user | /user |
| Db Client | pg.query( user(token, form) ) | pg.query( user(token, criteria, options) ) | pg.query( user(token, pk, form) ) | pg.query( user(token, pk) ) |
| API SQL Function | api_0_0_1.user(TEXT, JSON) | api_0_0_1.user(TEXT, JSON, JSON) | api_0_0_1.user(TEXT, TEXT, JSON) | api_0_0_1.user(TEXT, TEXT) |
| Static Base Function | base_0_0_1.insert(chelate) | base_0_0_1.query(chelate) | base_0_0_1.update(chelate) | base_0_0_1.delete(chelate) |
| Table | one | one | one | one |
 
## signin
 
|  |  |  |  |  |
|  -  |  -  |  -  |  -  |  -  |
| UI | Read |
| HTTP | GET |
| Routes | /signin |
| Db Client | pg.query( signin(token, criteria) ) |
| API SQL Function | api_0_0_1.signin(TEXT, JSON) |
| Static Base Function | base_0_0_1.query(chelate) |
| Table | one |
 
## signup
 
|  |  |  |  |  |
|  -  |  -  |  -  |  -  |  -  |
| UI | Create |
| HTTP | POST |
| Routes | /signup |
| Db Client | pg.query( signup(token, form) ) |
| API SQL Function | api_0_0_1.signup(TEXT, JSON) |
| Static Base Function | base_0_0_1.insert(chelate) |
| Table | one |