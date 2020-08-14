using System;
using System.IO;
using System.Data.SQLite;

namespace DataRepository
{
    public class SqLiteBaseRepository
    {
        public static string DbFile
        {
           // get { return Environment.CurrentDirectory + "\\sqlitetest.db"; }
           // get { return Directory.GetParent(Environment.CurrentDirectory).FullName + "\\sqlitetest.db"; }
           get {return Path.GetTempPath() + "\\sqlitetest.db";}
        }

        public static SQLiteConnection SimpleDbConnection()
        {
            Console.WriteLine(DbFile);
            return new SQLiteConnection("Data Source=" + DbFile);
        }
    }
}