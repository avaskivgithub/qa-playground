using System.Collections.Generic;
using System.Net.Http;
using System.Threading.Tasks;
using UImvc.Models;

namespace UImvc.Services
{
    // Based on https://github.com/MicrosoftDocs/mslearn-aspnet-core/blob/master/modules/create-razor-pages-aspnet-core/src/ContosoPets.Ui/Services/ProductService.cs
    public class ResultService
    {
        private readonly string _route;
        private readonly HttpClient _httpClient;

        public ResultService(
            HttpClient httpClient)
        {
            _httpClient = httpClient;
            _route = "/results";
        }

        public async Task<IEnumerable<Result>> GetResults()
        {
            var response = await _httpClient.GetAsync(_route);
            response.EnsureSuccessStatusCode();

            var Results = await response.Content.ReadAsAsync<IEnumerable<Result>>();

            return Results;
        }

        public async Task<Result> GetResultById(int ResultId)
        {
            var response = await _httpClient.GetAsync($"{_route}/{ResultId}");
            response.EnsureSuccessStatusCode();

            var Result = await response.Content.ReadAsAsync<Result>();

            return Result;
        }

        public async Task UpdateResult(Result Result)
        {
            await _httpClient.PutAsJsonAsync<Result>($"{_route}/{Result.Id}", Result);
        }

        public async Task CreateResult(Result Result)
        {
            await _httpClient.PostAsJsonAsync<Result>(_route, Result);
        }

        public async Task DeleteResult(int ResultId)
        {
            await _httpClient.DeleteAsync($"{_route}/{ResultId}");
        }
    }
}