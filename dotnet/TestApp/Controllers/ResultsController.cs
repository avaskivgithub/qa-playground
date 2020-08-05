using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using RestApi.Models;

namespace RestApi.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class ResultsController : ControllerBase
    {

        private readonly ILogger<ResultsController> _logger;

        public ResultsController(ILogger<ResultsController> logger)
        {
            _logger = logger;
        }

        [HttpGet]
        public IEnumerable<Result> Get()
        {
            var rng = new Random();
            return Enumerable.Range(1, 5).Select(index => new Result
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
