using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using UImvc.Models;
using UImvc.Services;
using System.Net.Http;

namespace UImvc.Controllers
{
    public class ResultsController : Controller
    {
        private readonly ILogger<ResultsController> _logger;
        private readonly ResultService _resultService;
        private readonly HttpClient _httpClient;

        public ResultsController(ILogger<ResultsController> logger)
        {
            _logger = logger;

            _httpClient = new HttpClient();
            _httpClient.BaseAddress = new Uri("https://localhost:5001/");
            _resultService = new ResultService(_httpClient);
        }

        public async Task<IActionResult> Index()
        {
            // TBD: Result model need fix (with list there is an issue)
            // List<Result> resultsAll = await _resultService.GetResults();
            List<ResultsViewModel> results = new List<ResultsViewModel>
            {
                new ResultsViewModel{Id = 1, Name = "View Name from ResultsController", Res = 1},
                new ResultsViewModel{Id = 2, Name = "View Name from ResultsController 2", Res = 2}
            };      
            return View(results);
        }

        // GET: Result/Details/5
        public async Task<IActionResult> Details(int? id)
        {
            if (id == null)
            {
                return NotFound();
            }

            Result result = await _resultService.GetResultById((int)id);
            if (result == null)
            {
                return NotFound();
            }

            return View(result);
        }
    }
}
