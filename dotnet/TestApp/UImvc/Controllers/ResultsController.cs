﻿using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using UImvc.Models;

namespace UImvc.Controllers
{
    public class ResultsController : Controller
    {
        private readonly ILogger<ResultsController> _logger;

        public ResultsController(ILogger<ResultsController> logger)
        {
            _logger = logger;
        }

        public IActionResult Index()
        {
            List<ResultsViewModel> results = new List<ResultsViewModel>
            {
                new ResultsViewModel{Id = 1, Name = "View Name from ResultsController", Res = 1},
                new ResultsViewModel{Id = 2, Name = "View Name from ResultsController 2", Res = 2}
            };      
            return View(results);
        }
    }
}