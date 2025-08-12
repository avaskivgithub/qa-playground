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
    [TestFixture]
    public class GetUsers
    {
        private string testEndpoint;
        private ApiClient api;

        [OneTimeSetUp]
        public async Task  SetupAsync()
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


            return actualResponseBody;
        }

        [Test]
        public async Task GetUsers_Page2_200WithBody()
        {
            // Arrange

            // Act
            HttpResponseMessage responseMessage = await api.GetAsync(
                testEndpoint // + "?page=2"
                );
            Result actualResponseBody = await ReadResponseBodyFromRequest(responseMessage);

            // Check
            Assert.That(responseMessage.StatusCode, Is.EqualTo(HttpStatusCode.OK));
        }
    }
}