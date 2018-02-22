# redctf

The most customizeable CTF Framework built with modern technologies.


## Phase One
#### Minimum functionality phase.

<details><summary>View contents</summary>
  
- [x] Auth
  - [x] Login - no access with proper login
  - [x] Register
  - [x] Hide/Show Admin page based on rights
- [x] Admin Page
  - [x] Create Category
  - [x] Create Challenge
- [x] Challenge Board
  - [x] Iterate and display categories and challenges from rethinkdb/horizon
  - [x] Challenge Modals
    - [x] Appearance
    - [x] Pass in Functions for submission
    - [x] Flag Check
    - [x] Sucess or Failure Toasts - should exit on success?
    - [x] Number Solves so far
  - [x] Flag Check in Django
- [x] Scoreboard Page
    - [x] Coloring in Tables
  - [x] Table of competitors
- [x] Team Page
  - [x] Accessible from top nav bar
  - [x] Accessible from scoreboard
  - [x] Graph
  - [x] Table for Challenges solved (and times solved)
- [x] Live Updates
  - [x] Challenge color switch
  - [x] Add categories through admin page
  - [x] Add challenges through admin page
  - [x] Scoreboard color and graph switch
  
</details>

## Phase Two
#### Improvement Phase

<details><summary>View contents</summary>
  
- [ ] CSS Improvements
  - [ ] Fix up components to look better
  - [ ] Move CSS colors to SASS variables
  - [x] Setup Basis for Theming in Phase Three
- [ ] Admin Page
  - [ ] Add CTFs
  - [x] Fix up Admin Panel to be useable
  - [ ] Release Hints
  - [ ] Complete CTF control
    - [ ] Ability to set future start time (with no errors in performance)
    - [ ] Ability to set future end time (and have it automatically stop CTF)
  - [ ] Complete control of Challenges
    - [ ] Better creation - html, more smooth transitions between making challenges
    - [ ] Admin panel
      - [ ] Challenge Row
        - [ ] Edit Challenge - popup with all challenge features for edit
        - [ ] Delete Challenge
        - [ ] Clone Challenge - useful if adding several similar challenges
        - [x] Number solves per challenge
        - [ ] Submitted correct / incorrect flags
        - [ ] Track the amount of times the modal is opened (don't know if it'd be interesting or not)
        - [ ] Graph button - see solves over time of competition
        - [ ] Release hint button
- [ ] Graphs
  - [ ] Legend
  - [ ] Tooltip
- [ ] Large Scale Documentation
  - [ ] Code Documentation
  - [ ] Process Documentation
  - [ ] Public Consumption Documentation
- [ ] Single Sign On Integrations
- [ ] Input Validation (Only Numbers here, Valid Email there, etc)
- [ ] Dockerize
- [ ] Auto-deployment of challenges (into containers possibly)?
- [ ] Link writeups to challenges post-ctf.  Just an idea, but we could have a folder structure, in which `.md` files are rendered into writeups, and we can auto-link challenges based on a configuration flag. For example, when generating a category, we could also trigger scaffolding and a base `/writeups/category/point_value/writeup.md` file. Then in each challenge modal, we check configuration and render a writeup link if configured. Another option - we could make these immediately available after close of CTF.
- [ ] Possible logging of django commands into run-script?  (i.e. Challenge gets created, put line of python into file. User gets created, put line of python into file.  Challenge gets solved, put line of python into file.  This would preserve the history of the CTF. If something catastrophic were to happen, you could theoretically spin up the exact same CTF with exact same user/challenge status by running a single script.  Just a thought.)


</details>

## Phase Three
#### Configuration Phase

<details><summary>View contents</summary>

- [ ] Admin Page
  - [ ] Allow upload custom HTML/CSS
  - [ ] Allow pick color scheme
  - [ ] Allow choose horizontal/vertical challenge board orientation
  - [ ] Choose email verification (i.e. send pwd, force pwd change or email verification link)
  - [ ] Choose team / multiple logins per team
  - [ ] Choose different scss modes (i.e. Vanilla Mode, Midnight Mode, Custom Mode, etc)
  - [ ] First blood points
  - [ ] Points decrease by number of solves
- [ ] Complete Documentation
- [ ] Flash challenges
- [ ] Linting
- [ ] Testing?  (i.e. Unit testing, Integration testing, Acceptance testing)


</details>

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
