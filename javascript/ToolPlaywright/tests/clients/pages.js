const MainPage = {
  pageLink: "http://uitestingplayground.com/",
  elementDynamicId: 'a[href*="/dynamicid"]',
  elementClassAttr: 'a[href*="/classattr"]',
  elementHiddenLayers: 'a[href*="/hiddenlayers"]',
  elementLoadDelay: 'a[href*="/loaddelay"]',
  elementAjaxDelay: 'a[href*="/ajax"]'
}
const DynamicIdPage = {
  pageLink: MainPage.pageLink + "dynamicid",
  elementText: "Button with Dynamic ID",
}

const ClassAttrPage = {
  pageLink: MainPage.pageLink + "classattr",
  elementAttr: "button.btn-primary" // "//button[contains(concat(' ', normalize-space(@class), ' '), ' btn-primary ')]",
}

// [id="greenButton"] hiddenlayers
const HiddenLayersPage = {
  pageLink: MainPage.pageLink + "hiddenlayers",
  elementAttr: '[id="greenButton"]',
  elementHiddenAttr: '[id="blueButton"]'
}

const LoadDelay = {
  pageLink: MainPage.pageLink + "loaddelay",
  elementAttr: "button.btn-primary",
  elementText: "Button Appearing After Delay",
}

const AjaxDelay = {
  pageLink: MainPage.pageLink + "ajax",
  elementAttr: 'button.btn-primary',
  elementResultAttr: '[class="bg-success"]',
  elementResultText: "Data loaded with AJAX get request.",
}

exports.MainPage = MainPage;
exports.DynamicIdPage = DynamicIdPage;
exports.ClassAttrPage = ClassAttrPage;
exports.HiddenLayersPage = HiddenLayersPage;
exports.LoadDelay = LoadDelay;
exports.AjaxDelay = AjaxDelay