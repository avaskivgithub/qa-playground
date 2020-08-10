using System;
using Xunit;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using SystemTestsRestApi.Clients;
using SystemTestsRestApi.Models;

namespace SystemTestsRestApi
{
    public class GetResultsTests
    {
        private HttpClient _httpClient;
        private HttpTestClient _httpTestClient;

        public GetResultsTests()
        {
            _httpClient = new HttpClient();
            _httpClient.BaseAddress = new Uri("https://localhost:5001/");
            _httpTestClient = new HttpTestClient(_httpClient);
        }

        [Fact]
        public async void GetResults_WithEmptyDb_ReturnsEmpty200Response()
        {
            // 1. Setup test data: delete ../RestApi/sqlitetest.db

            // 2. Call /results
            IEnumerable<Result> results = await _httpTestClient.GetResults();

            // 3. Check that response is 200 and empty response body
            Assert.Equal(0, results.Count());

        }
    }
}
