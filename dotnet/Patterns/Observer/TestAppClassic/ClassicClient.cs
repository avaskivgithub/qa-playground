using System;
using System.Collections.Generic;

// ConcreteObserver
namespace Observer.TestAppClassic
{
    public class ClassicClient : IClassicClient
    {
        private int _priceMin;
        private int _priceMax;
        private int _msgsCount;

        public ClassicClient(int priceMin, int priceMax )
        {
            this._priceMin = priceMin;
            this._priceMax = priceMax;
            this._msgsCount = 0;
        }

        public void ProcessMessageByClient(ClassicMessage msg)
        {
            //if (this._msgsCount == 0) // no message was processed by client
            //{
                Console.WriteLine($"Processing msg price = {msg.Price} with client price range [{this._priceMin}, {this._priceMax}] ");
                this._msgsCount = (msg.Price >= this._priceMin && msg.Price <= this._priceMax) ? this._msgsCount + 1 : this._msgsCount;
                Console.WriteLine($"this._msgsCount = {this._msgsCount}");
            //}
        }

        public bool AnnounceClientIfFree()
        {
            bool ifGotMsgToProcess = true;
            if (this._msgsCount == 0)
            {
                ifGotMsgToProcess = false;
                Console.WriteLine($"I'm client with the price range [{this._priceMin}, {this._priceMax}] and I did not get message within my range");
            }
            return ifGotMsgToProcess;
        }
    }
}