# redctf

The most customizeable CTF Framework built with modern technologies.



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

    `sudo pip3 install --upgrade --no-deps  --force-reinstall -r requirements.txt`

## To Develop on Project

Run the following (in order):

1) To Start Rethinkdb (`redctf/client/`)
    
    `rethinkdb`

2) To Run Horizon Server (`redctf/client/`)
    
    `hz serve --dev`

3) To Start Server (`redctf/server/`)

    * Fresh install, start server with test categories and challenges
    
        `python3 reset_db.py --cats --chals && python3 manage.py runserver`
    
    * Simple development
    
        `python3 manage.py runserver`

    
4) To Start Client (`redctf/client/`)
    
    `npm start`



## Configuration 
* Edit IP Options in `redctf/client/.hz/config.toml`.
* Edit RethinkDB Options in `redctf/client/.hz/config.toml`.
* Edit RDB_HOST in `redctf/server/redctf/settings.py`.
* Edit CORS_ORIGIN_WHITELIST in `redctf/server/redctf/settings.py`.


## Sources

* Horizon
   * https://appendto.com/2017/08/using-horizonrethinkdb-react/
