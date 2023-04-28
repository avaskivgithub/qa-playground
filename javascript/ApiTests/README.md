
## Setup
```
npm init
npm install chai --save-dev
npm install chai-http --save-dev
npm install mocha --save-dev
npm install mocha-junit-reporter --save-dev
```

## Reporters
* simple list (build-in reporter)
```
mocha --reporter list  'tests/*.js' --recursive --timeout 60000 --exit  2>&1 > ./report.log
```

* https://www.npmjs.com/package/mocha-simple-html-reporter
```
npm install --save-dev mocha-simple-html-reporter

// package.json
"test": "mocha --reporter mocha-simple-html-reporter --reporter-options output=report.html 'tests/*.js' --recursive --timeout 60000 --exit"
```

## Links
* https://www.chaijs.com/plugins/chai-http/ - chai http didn't work for me
* https://blog.logrocket.com/testing-node-js-mocha-chai/
* https://mochajs.org/
* https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch