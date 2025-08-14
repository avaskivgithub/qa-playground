using Tests.Clients;
using Tests.Models;
using Tests.Fixtures;
using System.Net.Http;
using System.Threading.Tasks;
using System.Net;
using Newtonsoft.Json;


namespace Tests.TestsApi
{
    /// <summary>
    /// Smoke tests to check test api
    /// </summary>
    [Parallelizable(ParallelScope.All)]
    [TestFixture]
    public class GetUsers
    {
        private string testEndpoint;
        private ApiClient api;

        [OneTimeSetUp]
        public async Task SetupAsync()
        {
            testEndpoint = FixtureConfiguration.GetSetting("ApiEndpointsUsers");
            api = new ApiClient();
        }

        [OneTimeTearDown]
        public async Task TeardownAsync()
        {
        }

        public async Task<Result> ReadResponseBodyFromRequest(HttpResponseMessage responseMessage)
        {
            string responseContent = await responseMessage.Content.ReadAsStringAsync();
            Console.WriteLine(responseContent);
            Result actualResponseBody = JsonConvert.DeserializeObject<Result>(responseContent);

            // Mocked delay to test out [Parallelizable(ParallelScope.All)]
            System.Threading.Thread.Sleep(2000);
            return actualResponseBody;
        }

        [Test]
        public async Task GetUsers_StatusBody_200WithTotalPages()
        {
            // Arrange

            // Act
            HttpResponseMessage responseMessage = await api.GetAsync(
                testEndpoint
                );
            Result actualResponseBody = await ReadResponseBodyFromRequest(responseMessage);

            // Check
            Assert.That(responseMessage.StatusCode, Is.EqualTo(HttpStatusCode.OK));
            Assert.That(actualResponseBody.total, Is.EqualTo(12));
        }

        [Test]
        public async Task GetUsers_Body_MultipleCheck()
        {
            // Arrange
            var expectedPage = 1;
            var expectedPerPage = 6;
            var expectedTotal = 12;
            var expectedTotalPages = 2;

            // Act
            HttpResponseMessage responseMessage = await api.GetAsync(
                testEndpoint
                );
            Result actualResponseBody = await ReadResponseBodyFromRequest(responseMessage);

            // Assert - multiple check
            Assert.Multiple(() =>
            {
                Assert.That(actualResponseBody.page, Is.EqualTo(expectedPage), "Page number mismatch");
                Assert.That(actualResponseBody.per_page, Is.EqualTo(expectedPerPage), "Per page count mismatch");
                Assert.That(actualResponseBody.total, Is.EqualTo(expectedTotal), "Total count mismatch");
                Assert.That(actualResponseBody.total_pages, Is.EqualTo(expectedTotalPages), "Total pages mismatch");

                Assert.That(actualResponseBody.data, Is.Not.Null.And.Not.Empty, "Data list is null or empty");

                // Check first item in data list
                var firstItem = actualResponseBody.data.First();
                Assert.That(firstItem.id, Is.EqualTo(1), "First item ID mismatch");
                Assert.That(firstItem.first_name, Is.EqualTo("George"), "First item first name mismatch");
                Assert.That(firstItem.last_name, Is.EqualTo("Bluth"), "First item last name mismatch");
                Assert.That(firstItem.email, Is.EqualTo("george.bluth@reqres.in"), "First item email mismatch");
            });
        }

        [TestCase("page", 1)]
        [TestCase("per_page", 6)]
        [TestCase("total", 12)]
        [TestCase("total_pages", 2)]
        // [Ignore("Skipping this test temporarily")]
        // [Parallelizable(ParallelScope.Self)]
        public async Task GetUsers_ResultsFieldValidation(
            string fieldName,
            int expectedValue)
        {
            // Arrange
            string endpoint = $"{testEndpoint}?page=1";

            // Act
            HttpResponseMessage responseMessage = await api.GetAsync(endpoint);
            Result actualResponseBody = await ReadResponseBodyFromRequest(responseMessage);


            // Assert
            // Use reflection to get the property value
            var propertyInfo = typeof(Result).GetProperty(fieldName);
            Assert.That(propertyInfo, Is.Not.Null, $"Property '{fieldName}' not found on Result");

            var actualValue = propertyInfo.GetValue(actualResponseBody);
            Assert.That(actualValue, Is.EqualTo(expectedValue), $"Mismatch for field '{fieldName}'");
        }

    }
}