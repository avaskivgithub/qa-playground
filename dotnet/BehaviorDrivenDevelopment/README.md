# Overview

Using example: https://docs.specflow.org/projects/getting-started/en/latest/GettingStarted/Step1.html

- Create Calculator project
```
dotnet new classlib -o SpecFlowCalc
```

- Create SpecFlow test project https://docs.specflow.org/projects/specflow/en/latest/Installation/Project-and-Item-Templates.html#installing-the-project-template
```
dotnet new -i SpecFlow.Templates.DotNet
dotnet new specflowproject -o Test
```

- Add Calculator project as a reference to the test project
```
dotnet add Test.csproj reference ../SpecFlowCalc/SpecFlowCalc.csproj
```

- Create a living doc
```
dotnet tool install --global SpecFlow.Plus.LivingDoc.CLI

Test> cd .\bin\Debug\netcoreapp3.1\
Test\bin\Debug\netcoreapp3.1> livingdoc test-assembly Test.dll -t TestExecution.json
```