namespace Tests.Models
{
    public class Result
    {
        public Int32 page {get; set;}
        public Int32 per_page {get; set;}

        public Int32 total {get; set;}
        public Int32 total_pages {get; set;}

        public List<Item> data {get; set;} = default!;
    }
}