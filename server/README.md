# server


## endpoints

#### login
`mutation { login ( username: "${username}", password: "${password}") {id isAdmin} }`

#### create user
`mutation { createUser(username:"${username}", email:"${email}", password: "${password}") { status } }`

#### add challenge
`mutation { addChallenge(flag:"${flag}", category: "${category}", title: "${title}", points: ${points}, description: "${description}") { status } }`
