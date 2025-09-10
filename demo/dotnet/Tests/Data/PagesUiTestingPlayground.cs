namespace Tests.Data
{
    public class MainPage
    {
        public static string pageLink = "http://uitestingplayground.com/";
        public static string pageRefDynamicId = "a[href*='/dynamicid']";
    }

    public class DynamicIdPage
    {
        public static string pageLink = MainPage.pageLink + "dynamicid";
        public static string btnAttr = "button.btn-primary";
        public static string btnText = "Button with Dynamic ID";
    }
}