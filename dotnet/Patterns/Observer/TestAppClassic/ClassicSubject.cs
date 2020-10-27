using System;
using System.Collections.Generic;

namespace Observer.TestAppClassic
{
    // ConcreatSubject
    public class ClassicSubject : IClassicSubject
    {
        private ClassicMessageCounter _msgCounter;
        private List<IClassicClient> _listClients = new List<IClassicClient>();

        public ClassicSubject(int threshold)
        {
            this._msgCounter = new ClassicMessageCounter()
            {
                CurrentAmount = 0,
                Threshold = threshold,
                AnounceFreeCients = false
            };
        }

        public void Attach(IClassicClient client)
        {
            this._listClients.Add(client);
        }

        public void Detach(IClassicClient client)
        {
            this._listClients.Remove(client);
        }

        // Notify
        public void StartSelling(List<ClassicMessage> listOfMessagesWithPrices)
        {
            foreach(var msg in listOfMessagesWithPrices)
            {
                foreach(var client in this._listClients)
                {
                    if (this._msgCounter.CurrentAmount < this._msgCounter.Threshold)
                    {
                        client.ProcessMessageByClient(msg);
                        this._msgCounter.CurrentAmount += 1;
                    }
                }
            }

            if (this._msgCounter.CurrentAmount >= this._msgCounter.Threshold)
            {
                foreach(var client in this._listClients)
                {
                    // we reached Threshold, time to announce what clients were left
                    client.AnnounceClientIfFree();
                }
            }
        }
    }
}