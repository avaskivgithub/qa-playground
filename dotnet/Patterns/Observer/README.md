# Observer
Materials
- https://docs.microsoft.com/en-us/dotnet/standard/events/ <= extremly confusing
- https://www.tutorialsteacher.com/csharp/csharp-event <= makes much more sense
- https://www.dofactory.com/net/observer-design-patterne


## Test App
This project is an app that counts received requests by different clients:

- list of clients are kept by the app
    - a _notification list_ is a list to which clients are added  
    - _messages counter_ keeps amount of processed messages
    - _messages counter threshold_ is the limit of messages that can be processed by the defined list of clients

- messages are processed
  - _message_ that is processed by _client_ has _price_ field
  - _messages counter_ is increased each time a message is received and current value is printed out to the console
  - all clients from the _notification list_ receives the _message_

- clients listen to messages
  - each _client_ has it's own _price range_ and _processed state_
  - when _client_ is created then _price range_ can be set and _processed state_ is set to 0 by default
  - _client_. _processed state_ is increased only if _message_._price_ is in the _client_._price range_, otherwise message is ignored 
  - clients that already got requests (_processed state_ >= 1) should not process messages

- when _messages counter_ reaches _messages counter threshold_
  - clients that didn't receive the _message_ should print out into the console _'client.name was not used'_ 