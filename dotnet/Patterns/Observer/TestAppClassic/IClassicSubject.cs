using System;
using System.Collections.Generic;

namespace Observer.TestAppClassic
{
    // Subject
    public interface IClassicSubject
    {
        public void Attach(IClassicClient client);
        public void Detach(IClassicClient client);
        // Notify
        public void StartSelling(List<ClassicMessage> listOfMessagesWithPrices);
    }
}