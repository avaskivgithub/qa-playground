https://playwright.dev/docs/intro#installation

npx playwright codegen wikipedia.org


npx playwright test --project chromium

# to debug
$env:PWDEBUG=1
# to disable debug
$env:PWDEBUG=""

Q: How to run only one test, calc?
A: Add annotation only 
```
test.only('calc add 2 numbers', async ({page}) => {
```

npx playwright test --project=chromium