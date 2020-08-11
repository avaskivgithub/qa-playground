using System;
using Xunit;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using SystemTestsRestApi.Clients;
using SystemTestsRestApi.Models;
using DataRepository;

namespace SystemTestsRestApi
{
    public class GetResultsTests
    {
        private HttpClient _httpClient;
        private HttpTestClient _httpTestClient;
        private IResultsRepository _repository;

        public GetResultsTests()
        {
            _httpClient = new HttpClient();
            _httpClient.BaseAddress = new Uri("https://localhost:5001/");
            _httpTestClient = new HttpTestClient(_httpClient);
            _repository = new SqLiteResultsRepository();
        }

        [Fact]
        public async void GetResults_WithEmptyDb_ReturnsEmpty200Response()
        {
            // 1. Setup test data: delete ../RestApi/sqlitetest.db
            DataRepository.SqLiteResultsRepository.DeleteDatabase();
            DataRepository.SqLiteResultsRepository.CreateDatabase();

            // 2. Call /results
            IEnumerable<Result> results = await _httpTestClient.GetResults();

            // 3. Check that response is 200 and empty response body
            Assert.Equal(0, results.Count());

        }
    }
}
