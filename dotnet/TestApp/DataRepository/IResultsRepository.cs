using System.Collections.Generic;
using Models;


namespace DataRepository
{
    public interface IResultsRepository
    {
    Result GetResult(int id);
    IEnumerable<Result> GetResults();
    void SaveResult(Result result);
    void SaveResults(IEnumerable<Result> results);
    }
}
