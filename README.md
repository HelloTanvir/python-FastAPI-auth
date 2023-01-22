### This app is created using FastAPI web framework of python

#### Main purpose of the app is a complete user authentication

#### Used JWT for handling the authentication

#### It creates access token and refresh token when signed up or logged in. Stores the user name, email, password hash, and created refresh token in MongoDB. Returns a pair of tokens to the user.

#### Access token will be expired after 15 minutes. To generate a new pair of tokens, there is a route /refresh-tokens, this will generate a new pair of tokens and update the refresh token in db and return tokens to the user. Also, refresh token will be expired after a week

### The app is deployed in Azure

[Live](https://fastapi-auth.azurewebsites.net/)

[Api Doc](https://fastapi-auth.azurewebsites.net/docs)
