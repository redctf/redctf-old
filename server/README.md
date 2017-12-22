# server


## endpoints


### Mutations
#### login
`mutation { login ( username: "${username}", password: "${password}") {id isSuperuser} }`

#### create user
`mutation { createUser(username:"${username}", email:"${email}", password: "${password}") { status } }`

#### add challenge
`mutation { addChallenge(flag:"${flag}", category: "${category}", title: "${title}", points: ${points}, description: "${description}") { status } }`

### Queries
#### whoami
`query { me {id isSuperuser username}}`
