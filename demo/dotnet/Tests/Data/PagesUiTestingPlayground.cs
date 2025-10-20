namespace Tests.Data
{
    public class MainPage
    {
        public static string pageLink = "http://uitestingplayground.com/";
        public static string pageRefDynamicId = "a[href*='/dynamicid']";
        public static string pageRefClientSideDelay = "a[href*='/clientdelay']";
    }

    public class DynamicIdPage
    {
        public static string pageLink = MainPage.pageLink + "dynamicid";
        public static string btnAttr = "button.btn-primary";
        public static string btnText = "Button with Dynamic ID";
    }

    public class ClientSideDelayPage
    {
        public static string pageLink = MainPage.pageLink + "clientdelay";
        public static string btnAttr = "button.btn-primary";
        public static string btnText = "Button Triggering Client Side Logic";
        public static string pResultField = "[class='bg-success']";
        public static string pResultText = "Data calculated on the client side.";
    }
}