# server
### Mutations
| Function |  Graphql Command   |
|----------|--------------------|
| Create New User | `mutation { createUser(username:"${username}", email:"${email}", password: "${password}") { status } }`  | 
| Login           | `mutation { login ( username: "${username}", password: "${password}") {id isSuperuser} }`  |
| Add Challenge   | `mutation { addChallenge(flag:"${flag}", category: "${category}", title: "${title}", points: ${points}, description: "${description}") { status } }`  | 

### Queries
| Function              |  Graphql Command   |
|-----------------------|--------------------|
| Get User Information  | `query { me {id isSuperuser username}}` |
