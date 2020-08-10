using System;
using Xunit;

namespace SystemTestsRestApi
{
    public class GetResultsTests
    {
        [Fact]
        public void GetResults_WithEmptyDb_ReturnsEmpty200Response()
        {
            // 1. Setup test data: delete ../RestApi/sqlitetest.db

            // 2. Call /results

            // 3. Check that response is 200 and empty response body
            Assert.True(false);

        }
    }
}
