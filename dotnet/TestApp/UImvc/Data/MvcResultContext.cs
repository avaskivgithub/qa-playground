using Microsoft.EntityFrameworkCore;
using UImvc.Models;

namespace UImvc.Data
{
    public class MvcResultContext : DbContext
    {
        public MvcResultContext (DbContextOptions<MvcResultContext> options)
            : base(options)
        {
        }

        public DbSet<Result> Result { get; set; }
    }
}