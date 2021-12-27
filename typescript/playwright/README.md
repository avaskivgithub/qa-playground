# Overview
https://playwright.dev/docs/intro#installation

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
