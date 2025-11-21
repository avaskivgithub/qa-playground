*** Settings ***
Documentation     Example test case using the gherkin syntax.
...
...               This test has a workflow similar to the keyword-driven
...               examples. The difference is that the keywords use higher
...               abstraction level and their arguments are embedded into
...               the keyword names.
...
...               This kind of _gherkin_ syntax has been made popular by
...               [http://cukes.info|Cucumber]. It works well especially when
...               tests act as examples that need to be easily understood also
...               by the business people.
Library           RequestLibrary.py

*** Test Cases ***
Simple Get Request
    Given api is up
    When user calls "/api/users"
    Then result status code is "200"
        and body contains "\"total\":12"

*** Keywords ***
Api is up
    Call get    /api/echo

User calls "${expression}"
    Call get    ${expression}

Result status code is "${result}"
    Result code should be  ${result}

Body contains "${result}"
    Result body should contain  ${result}
