using Newtonsoft.Json;
using Tests.Fixtures;


namespace Tests.Clients
{
    public class ApiClient
    {


        private string BaseUrl;
        private string ApiKey;

        private readonly HttpClient httpClient;

        /// <summary>
        /// Client for https://reqres.in/api-docs/
        /// </summary>
        /// <param name="baseUrl"></param>
        /// <param name="apiKey"></param>
        public ApiClient(string baseUrl=null,
                        string apiKey=null)
        {
            BaseUrl = baseUrl ?? FixtureConfiguration.GetSetting("ApiBaseUrl");
            ApiKey = apiKey ?? FixtureConfiguration.GetSetting("ApiKey");
            httpClient = new HttpClient();
        }


        public Uri GetFullUri(string relativeUri)
        {
            return new Uri(
                new Uri(BaseUrl),
                relativeUri);
        }

        public async Task<HttpRequestMessage> GetAuthenticatedRequestAsync(string relativeUri, HttpMethod httpMethod)
        {
            Uri fullUri = GetFullUri(relativeUri);
            HttpRequestMessage httpRequestMessage = new HttpRequestMessage(httpMethod, fullUri);

            // TBD: read key from env vars
            // string testBearerToken = Environment.GetEnvironmentVariable("TestBearerToken");
            httpRequestMessage.Headers.Add("x-api-key", ApiKey);

            return httpRequestMessage;
        }


        private async Task<HttpRequestMessage> GetAuthenticatedRequestAsync<T>(string relativeUri, HttpMethod httpMethod, T body)
        {
            HttpRequestMessage httpRequestMessage = await GetAuthenticatedRequestAsync(relativeUri, httpMethod);
            httpRequestMessage.Content = new StringContent(
                JsonConvert.SerializeObject(body),
                System.Text.Encoding.UTF8,
                "application/json");
            return httpRequestMessage;
        }

        public async Task<HttpResponseMessage> GetAsync(string relativeUri)
        {
            HttpRequestMessage authenticatedHttpRequest =
                await GetAuthenticatedRequestAsync(relativeUri, HttpMethod.Get);
            return await httpClient.SendAsync(authenticatedHttpRequest);
        }

        public async Task<HttpResponseMessage> PostAsync<T>(string relativeUri, T body)
        {
            HttpRequestMessage authenticatedHttpRequest = await GetAuthenticatedRequestAsync(relativeUri, HttpMethod.Post, body);
            return await httpClient.SendAsync(authenticatedHttpRequest);
        }

        public async Task<HttpResponseMessage> PutAsync<T>(string relativeUri, T body)
        {
            HttpRequestMessage authenticatedHttpRequest = await GetAuthenticatedRequestAsync(relativeUri, HttpMethod.Put, body);
            return await httpClient.SendAsync(authenticatedHttpRequest);
        }

        public async Task<HttpResponseMessage> PutNoBodyAsync(string relativeUri)
        {
            HttpRequestMessage authenticatedHttpRequest = await GetAuthenticatedRequestAsync(relativeUri, HttpMethod.Put);
            return await httpClient.SendAsync(authenticatedHttpRequest);
        }

        public async Task<HttpResponseMessage> PatchAsync<T>(string relativeUri, T body)
        {
            HttpRequestMessage authenticatedHttpRequest = await GetAuthenticatedRequestAsync(relativeUri, HttpMethod.Patch, body);
            return await httpClient.SendAsync(authenticatedHttpRequest);
        }

        public async Task<HttpResponseMessage> DeleteAsync<T>(string relativeUri)
        {
            HttpRequestMessage authenticatedHttpRequest = await GetAuthenticatedRequestAsync(relativeUri, HttpMethod.Delete);
            return await httpClient.SendAsync(authenticatedHttpRequest);
        }

        public async Task<HttpResponseMessage> DeleteNoBodyAsync(string relativeUri)
        {
            HttpRequestMessage authenticatedHttpRequest = await GetAuthenticatedRequestAsync(relativeUri, HttpMethod.Delete);
            return await httpClient.SendAsync(authenticatedHttpRequest);
        }
    }
}
