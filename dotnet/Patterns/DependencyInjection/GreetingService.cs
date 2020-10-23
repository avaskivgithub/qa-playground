using System;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;

namespace DependencyInjection
{
    public class GreetingService : IGreetingService
    {
        private readonly ILogger<GreetingService> log;
        private readonly IConfiguration conf;

        public GreetingService(ILogger<GreetingService> log, IConfiguration conf)
        {
            this.log = log;
            this.conf = conf;
        }

        public void Run()
        {

            for(int i=0; i < this.conf.GetValue<int>("LoopTimes"); i++)
            {
                // structured log
                this.log.LogInformation("We run {runnum}", i);
            }

            Console.ReadKey();
        }
    }
}
