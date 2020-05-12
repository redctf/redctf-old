# redctf 
![Build](https://github.com/redctf/redctf/workflows/Build/badge.svg)


The most customizeable CTF Framework built with modern technologies.

## Development
Everything is dockerized and easy to start development.

####  Development
`docker-compose -f docker-compose.dev.yml up`

#### Production
`docker-compose -f docker-compose.prod.yml up`



## Composition

#### Client
* ReactJS 15
* React Router 4
* Webpack 3
* Mobx

#### Realtime Integration
* Horizon
* RethinkDB

#### Backend
* Django
* GraphQL


## Requirements
* Horizon
* Rethinkdb
* Django (`redctf/server/`)


## Configuration 
* Edit IP Options in `redctf/client/.hz/config.toml`.
* Edit RethinkDB Options in `redctf/client/.hz/config.toml`.
* Edit RDB_HOST in `redctf/server/redctf/settings.py`.
* Edit CORS_ORIGIN_WHITELIST in `redctf/server/redctf/settings.py`.


## Sources

* Horizon
   * https://appendto.com/2017/08/using-horizonrethinkdb-react/
