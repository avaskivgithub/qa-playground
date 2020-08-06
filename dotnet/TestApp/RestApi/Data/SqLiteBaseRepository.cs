using System;
using System.Data.SQLite;

namespace RestApi.Data
{
    public class SqLiteBaseRepository
    {
        public static string DbFile
        {
            get { return Environment.CurrentDirectory + "\\sqlitetest.db"; }
        }

        public static SQLiteConnection SimpleDbConnection()
        {
            return new SQLiteConnection("Data Source=" + DbFile);
        }
    }
}