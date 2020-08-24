using Microsoft.AspNetCore.Mvc;
using System.Text.Encodings.Web;

namespace MvcMovie.Controllers
{
    public class HelloWorldController : Controller
    {
        // 
        // GET: /HelloWorld/
        public ActionResult Index()
        {
            return View();
            //return "Why error CS0029: Cannot implicitly convert type Microsoft.AspNetCore.Mvc.ViewResult to string";
            // see https://stackoverflow.com/questions/6226811/problems-with-redirecttoaction-mvc2-cannot-implicitly-convert-type-system-web/6226850
        }

        // 
        // GET: /HelloWorld/Welcome/ 

        // GET: /HelloWorld/Welcome/ 
        // Requires using System.Text.Encodings.Web;
        public ActionResult Welcome(string name, int numTimes = 1)
        {
            //return HtmlEncoder.Default.Encode($"Hello {name}, NumTimes is: {numTimes}");
            
            ViewData["Message"] = "Hello " + name;
            ViewData["NumTimes"] = numTimes;

            return View();
            
        }
    }
}