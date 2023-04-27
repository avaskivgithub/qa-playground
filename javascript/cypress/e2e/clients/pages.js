const MainPage = {
  pageLink: "http://uitestingplayground.com/",
  elementDynamicId: 'a[href*="/dynamicid"]',
  elementClassAttr: 'a[href*="/classattr"]',
  elementHiddenLayers: 'a[href*="/hiddenlayers"]'
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

exports.MainPage = MainPage;
exports.DynamicIdPage = DynamicIdPage;
exports.ClassAttrPage = ClassAttrPage;
exports.HiddenLayersPage = HiddenLayersPage;