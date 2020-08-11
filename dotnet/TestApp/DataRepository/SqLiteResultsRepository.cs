using System.IO;
using System.Linq;
using System.Collections.Generic;
using Dapper;
using Models;

namespace DataRepository
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
                            Name varchar(50),
                            Description varchar(1024),
                            Res INT,
                            Error varchar(256)
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
                using (var multi = cnn.QueryMultiple(@"SELECT Id, Name, Description, Res, Error FROM Results;"))
                {
                    var results = multi.Read<Result>().ToList();
                    return (IEnumerable<Result>)results;
                }  
            }
        }
    }
}
