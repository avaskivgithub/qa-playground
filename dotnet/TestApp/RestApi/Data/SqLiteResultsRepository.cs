using System.IO;
using System.Linq;
using System.Collections.Generic;
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

        public void SaveResults(IEnumerable<Result> results)
        {
            if (!File.Exists(DbFile))
            {
                CreateDatabase();
            }

            using (var cnn = SimpleDbConnection())
            {
                cnn.Open();
                foreach (Result result in results)
                {
                    cnn.Query(
                        @"INSERT INTO Results
                        ( Name, Description, Res, Error ) VALUES
                        ( @Name, @Description, @Res, @Error );"
                        , result);
                }
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

        public IEnumerable<Result> GetResults()
        {
            if (!File.Exists(DbFile)) return null;

            using (var cnn = SimpleDbConnection())
            {
                cnn.Open();
                var results = cnn.Query(
                    @"SELECT Id, Name, Description, Res, Error
                    FROM Results;");
                return (IEnumerable<Result>)results;
            }
        }
    }
}
