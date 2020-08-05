using RestApi.Models;

namespace RestApi.Data
{
    public interface IResultsRepository
    {
    Result GetResult(int id);
    void SaveResult(Result customer);
    }
}
