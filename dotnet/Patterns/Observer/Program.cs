using System;
using System.Diagnostics;
using System.Collections.Generic;
using Observer.SimpleExampleWithEvents;
using Observer.TestAppWithEvents;
using Observer.TestAppClassic;

namespace Observer
{

    class Program
    {
        static void Main(string[] args)
        {
            RunTestAppClassic();
            // RunTestAppWithEvents();
            // RunSimpleExample();
        }

        static void RunTestAppClassic()
        {
            Console.WriteLine("Hello Classic Observer pattern! Let's process messages");
            
            // 1. Get test data ready
            List<ClassicClient> allClients = new List<ClassicClient>();
            List<ClassicMessage> listOfMessagesWithPrices = new List<ClassicMessage>();
            for (int i=2; i < 15; i++)
            {
                allClients.Add(new ClassicClient(1, i));
            }

            for (int i=1; i < 10; i++)
            {
                listOfMessagesWithPrices.Add(
                    new ClassicMessage(){Price = i}
                );
            }


            // 2. Test App instance
            ClassicSubject testAppInTesting = new ClassicSubject(threshold: 7);
            foreach (ClassicClient testClient in allClients)
            {
                testAppInTesting.Attach(testClient);
            }

            // 3. Start testing
            testAppInTesting.StartSelling(listOfMessagesWithPrices);
        }

        static void RunTestAppWithEvents()
        {
            Console.WriteLine("Hello Observer pattern! Let's process messages");

            var msgsCounterEvent = new MsgsCounterEventArgs()
                {
                    GlobalAnounceFreeCients = false,
                    GlobalCurrentAmount = 0,
                    GlobalThreshold = 1,
                    Msg = new Message(){ Price = 5 }
                };

            List<Client> allClients = new List<Client>();
            for (int i=2; i < 15; i++)
            {
                allClients.Add(new Client(1, i));
            }

            TestAppLogic testAppInTesting = new TestAppLogic(msgsCounterEvent);
            foreach (Client testClient in allClients)
            {
                testAppInTesting.ProcessMsg += testClient.ProcessMessageByClient;
            }

            testAppInTesting.StartSelling(msgsCounterEvent);
        }

        static void RunSimpleExample()
        {
            Console.WriteLine("RunSimpleExample: Hello Observer pattern!");
            Console.WriteLine("Simple example from https://www.tutorialsteacher.com/csharp/csharp-event");

            // Observer pattern related: intializing subject  (concrete subject)
            ProcessBusinessLogic bl = new ProcessBusinessLogic();

            // Observer pattern related: event handlers (concrete observers)
            void bl_ProcessCompleted() => Console.WriteLine($"{new StackTrace().GetFrame(0).GetMethod().Name}: Process Completed!");
            void b2_ProcessCompleted() => Console.WriteLine($"{new StackTrace().GetFrame(0).GetMethod().Name}: Process Completed!");

            // Observer pattern related: Attaching observers to the list of Subject
            bl.ProcessCompleted += bl_ProcessCompleted; // register with an event
            bl.ProcessCompleted += b2_ProcessCompleted;

            // Observer pattern related: Notifying all observers
            bl.StartProcess();
        }
    }
}
