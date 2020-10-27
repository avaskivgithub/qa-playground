using System;

namespace Observer.TestAppWithEvents
{

    public class TestAppLogic
    {
        public event EventHandler<MsgsCounterEventArgs> ProcessMsg; // event using built-in EventHandler delegate
        private int _globalCurrentAmount;
        private int _globalThreshold;
        private MsgsCounterEventArgs msgsCounterEvent; 


        public TestAppLogic(MsgsCounterEventArgs msgsCounterEvent)
        {
            this._globalCurrentAmount = 0;
            this._globalThreshold = msgsCounterEvent.GlobalThreshold;
            this.msgsCounterEvent = msgsCounterEvent;
        }

        public MsgsCounterEventArgs MsgsCounterEventArgs()
        {
            return this.msgsCounterEvent;
        }

        public void StartSelling(MsgsCounterEventArgs e)
        {
            Console.WriteLine("Start Selling!");          
            OnProcessMsg(this.msgsCounterEvent);
        }

        protected virtual void OnProcessMsg(MsgsCounterEventArgs e) //protected virtual method
        {
            // Console.WriteLine($"Before process e.GlobalCurrentAmount = {e.GlobalCurrentAmount}");
            if (this._globalCurrentAmount < this._globalThreshold)
            {
                this._globalCurrentAmount += 1; 
                e.GlobalCurrentAmount = this._globalCurrentAmount;
                ProcessMsg?.Invoke(this, e); // if ProcessMsg is not null then call delegate
               
            }
            else
            {
                // call print out clients that didn't process the msg
                e.GlobalAnounceFreeCients = true;
                ProcessMsg?.Invoke(this, e);
            }
            // Console.WriteLine($"After process e.GlobalCurrentAmount = {e.GlobalCurrentAmount}");
        }
    }

    public class Message
    {
        public int Price {get; set;}
    }

    public class MsgsCounterEventArgs : EventArgs
    {
        public int GlobalCurrentAmount { get; set; } // TBD: initialize with 0 by default
        public int GlobalThreshold { get; set; }
        public bool GlobalAnounceFreeCients { get; set; }
        public Message Msg {get; set;}
    }

    public class Client
    {

        private int _priceMin;
        private int _priceMax;
        private int _msgsCount;

        public Client(int priceMin, int priceMax )
        {
            this._priceMin = priceMin;
            this._priceMax = priceMax;
            this._msgsCount = 0;
        }

        // Client (event handler)
        public void ProcessMessageByClient(object sender, MsgsCounterEventArgs e)
        {
            if (e.GlobalAnounceFreeCients)
            {
                Console.WriteLine("did not get message within my range");
            }
            else if (this._msgsCount == 0) // no message was processed by client
            {
                Console.WriteLine($"Processing message from client with max = {this._priceMax}");
                this._msgsCount = (e.Msg.Price >= this._priceMin && e.Msg.Price <= this._priceMax) ? this._msgsCount + 1 : this._msgsCount;
                Console.WriteLine($"this._msgsCount = {this._msgsCount}");
                Console.WriteLine($"client's e.GlobalCurrentAmount = {e.GlobalCurrentAmount}");
            }
            Console.WriteLine(e.GlobalCurrentAmount);
        }
    }
}
