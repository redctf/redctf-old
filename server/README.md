# server
### Mutations
| Function |  Graphql Command   |
|----------|--------------------|
| Create New User | `mutation { createUser(username:"${username}", email:"${email}", password: "${password}") { status } }`  | 
| Login           | `mutation { login ( username: "${username}", password: "${password}") {id isSuperuser} }`  |
| Create New Team | `mutation { createTeam(teamname:"${teamname}") { token } }`  | 
| Join Team       | `mutation { joinTeam(token:"${token}") { status } }`  | 
| Add Challenge   | `mutation { addChallenge(flag:"${flag}", category: "${category}", title: "${title}", points: ${points}, description: "${description}") { status } }`  | 

### Queries
| Function              |  Graphql Command   |
|-----------------------|--------------------|
| Get User Information  | `query { me {id isSuperuser username}}` |
| Get Team Information  | `query { team {id name, points, users{id, username}}}` |

