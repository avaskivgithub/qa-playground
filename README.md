# qa-playground
A playground for playing around with testing using a ["Test App"](python/README.md).

["Test App"](python/README.md) (with following [hierarchy](python/simple_app_with_tests/docs/app/1_hierarchy) ) is the most simple test management tool, that in a nutshell consists of:
* [sqlite](python/simple_app_with_tests/docs/app/2_db_sqlite) as a backend with a single table Results that has (Id, Name, Description, Res, Error) fields
* [REST api](python/simple_app_with_tests/docs/app/3_api) to do CRUD operations on the Results table records
* UI (if created) that uses api to add / edit / delete tests (you can see screenshots of a similar [app created with dotnet](dotnet/README.md) )

## Purpose
"Test App" is a playground for testing (to show what the process / tests can look like). This app can be used to:
* add new features to the [app](python/simple_app_with_tests/project/app) (this way you'll try a programming language) based on suggested [backlog](python/simple_app_with_tests/docs/backlog)
* add automated [api](python/simple_app_with_tests/project/tests/tests/api) and [web ui](python/simple_app_with_tests/project/tests/tests/wui) tests (note that those tests are not unit tests, but more of the system tests that perform black box testing)
* create test design and extend [example](python/simple_app_with_tests/docs/sprint1/testcases) / [user stories](python/simple_app_with_tests/docs/sprint1/stories) / describe issues
* fix app itself or tests for this app
