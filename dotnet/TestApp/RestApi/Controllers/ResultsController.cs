using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using Models;
using DataRepository;

namespace RestApi.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class ResultsController : ControllerBase
    {

        private readonly ILogger<ResultsController> _logger;
        private IResultsRepository _repository;

        public ResultsController(ILogger<ResultsController> logger)
        {
            _logger = logger;
            _repository = new SqLiteResultsRepository();
        }

        // TBD: it should be some kind of Post
        [HttpGet]
        [Route("create/db/seeddata")]
        public void PostDatabaseAndSeedData()
        {
            _repository.SaveResults(GenerateTestData());
        }
      
        [HttpGet]
        public IEnumerable<Result> Get()
        {
            // return GenerateTestData();
            return _repository.GetResults();
        }

        [HttpGet]
        [Route("{resultId}")]
        public Result GetResultById(int resultId)
        {
            // return GenerateTestData(resultId + 1).ElementAt(resultId);
            return _repository.GetResult(resultId);
        }

        [HttpPost]
        public void Create(Result result)
        {
            _repository.SaveResult(result);
        }

        private IEnumerable<Result> GenerateTestData(int amount=5)
        {
            var rng = new Random();
            return Enumerable.Range(1, amount).Select(index => new Result
            {
                Id = index,
                Name = "Name" + index.ToString(),
                Description = "Description" + index.ToString(),
                Res = rng.Next(-1, 2),
                Error = "Error" + index.ToString()
            })
            .ToArray();
        }
    }
}
