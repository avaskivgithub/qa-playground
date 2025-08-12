# Overview
Not to hit real test apis we can start local server just not to reach limit of the real test api.

## Api\

- Start API
```
qa-playground> cd demo\dotnet\Mocks\Api
qa-playground\demo\dotnet\Mocks\Api> python -m http.server 8888
```

- Run get request
```
curl http://127.0.0.1:8888/api/users.html
```