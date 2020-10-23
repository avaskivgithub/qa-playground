using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;

namespace DependencyInjection
{
    public interface IGreetingService
    {
        public void Run();
    }
}
