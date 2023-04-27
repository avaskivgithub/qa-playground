
## Setup
```
npm init
npm install cypress --save-dev
```

## Configure E2E
```
.\node_modules\.bin\cypress open
```

Add to package.json
```
  "scripts": {
    "cypress:open": "cypress open",
    "cypress:run": "cypress run"
```

Now you can run
```
npx cypress open
npx cypress run
```

## Recorder
See:
* https://www.browserstack.com/docs/automate/cypress/devtools-recorder
* https://www.browserstack.com/docs/automate/cypress/devtools-recorder#enable-recorder

## Run Test Suite
```
// skip --headed if you want headless mode
npx cypress run --headed --spec "cypress/e2e/test_uitestingplayground.cy.js"
```

## Debugging
Cypress tests have to be on Electron in order for "developer tools" to be opened and debugger / .debug() to work. 
* https://www.browserstack.com/guide/how-to-start-with-cypress-debugging
* https://github.com/cypress-io/cypress/issues/3559S