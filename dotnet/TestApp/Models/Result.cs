using System;

namespace RestApi.Models
{
    public class Result
    {
        public int Id { get; set; }

        public string Name { get; set; }
        public string Description { get; set; }
        public int Res { get; set; }
        public string Error { get; set; }
    }
}
