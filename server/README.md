# server


## endpoints

#### login
`mutation { login ( username: "${username}", password: "${password}") {status} }`

#### create user
`mutation { createUser(username:"test", email:"test@example.com", password: "abcd1234") { status } }`
