using System;

namespace Observer.SimpleExampleWithEvents
{

    // https://www.tutorialsteacher.com/csharp/csharp-event

    // Observer pattern related: observer abstraction 
    public delegate void Notify();  // delegate

    public class ProcessBusinessLogic
    {
        public event Notify ProcessCompleted; // event

        // Observer pattern related: subject implementation
        public void StartProcess()
        {
            Console.WriteLine("Process Started!");
            // some code here..
            OnProcessCompleted();
        }

        // Observer pattern related: subject abstraction
        protected virtual void OnProcessCompleted() //protected virtual method
        {
            //if ProcessCompleted is not null then call delegate
            ProcessCompleted?.Invoke(); 
        }
    }
}
