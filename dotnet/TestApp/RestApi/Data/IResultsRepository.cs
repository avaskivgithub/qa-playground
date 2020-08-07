using System.Collections.Generic;
using RestApi.Models;

namespace RestApi.Data
{
    public interface IResultsRepository
    {
    Result GetResult(int id);
    IEnumerable<Result> GetResults();
    void SaveResult(Result result);
    void SaveResults(IEnumerable<Result> results);
    }
}
