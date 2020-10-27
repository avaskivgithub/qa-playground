using System;
using System.Collections.Generic;

namespace Observer.TestAppClassic
{
    // Observer
    public interface IClassicClient
    {
        public void ProcessMessageByClient(ClassicMessage msg);
        public bool AnnounceClientIfFree();
    }
}