using System.IO;
using System.Linq;
using Dapper;
using RestApi.Models;

namespace RestApi.Data
{
    public class SqLiteResultsRepository : SqLiteBaseRepository, IResultsRepository
    {
        public void SaveResult(Result result)
        {
            if (!File.Exists(DbFile))
            {
                CreateDatabase();
            }

            using (var cnn = SimpleDbConnection())
            {
                cnn.Open();
                result.Id = cnn.Query<int>(
                    @"INSERT INTO Results
                    ( Name, Description, Res, Error ) VALUES
                    ( @Name, @Description, @Res, @Error );
                    SELECT last_insert_rowid()", result).First();
            }
        }

        private static void CreateDatabase()
        {
            using (var cnn = SimpleDbConnection())
            {
                cnn.Open();
                cnn.Execute(
                    @"CREATE TABLE Results
                        (
                            Id integer primary key AUTOINCREMENT,
                            Name TEXT,
                            Description BLOB,
                            Res INT,
                            Error BLOB
                        )");
            }
        }

        public Result GetResult(int id)
        {
            if (!File.Exists(DbFile)) return null;

            using (var cnn = SimpleDbConnection())
            {
                cnn.Open();
                Result result = cnn.Query<Result>(
                    @"SELECT Id, Name, Description, Res, Error
                    FROM Results
                    WHERE Id = @id", new { id }).FirstOrDefault();
                return result;
            }
        }
    }
}
