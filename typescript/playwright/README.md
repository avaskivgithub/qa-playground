# Overview

- Install browsers and packages. For details see: https://playwright.dev/docs/intro#installation
```
# install browsers
npx playwright install

# install packages
npm install -D
```

- Record/Playback
```
npx playwright codegen wikipedia.org
```
- Run tests
```
npx playwright test --project=chromium
```
- Debug
```
# to debug
$env:PWDEBUG=1
# to disable debug
$env:PWDEBUG=""
```
- *Q:* How to run only one test, calc? *A:* Add annotation only 
```
test.only('calc add 2 numbers', async ({page}) => {
```

- Added to the playwright.config.ts use.headless to have the ability to disable it for tests

- Tried trace 
```
npx playwright show-trace .\test-results\tests-example-my-test-chromium\trace.zip
```

- Via *npm init* added package files
