# server


## endpoints

#### login
`mutation { login ( username: "${username}", password: "${password}") {status} }`

#### create user
`mutation { createUser(username:"test", email:"test@example.com", password: "abcd1234") { status } }`

#### add challenge
`mutation { addChallenge(flag:"flag1234", category: "pwn", title: "pwn 100", points: 200, description: "This is pwn 100") { status } }`
