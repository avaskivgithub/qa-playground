const MainPage = {
  pageLink: "http://uitestingplayground.com/",
  pageRefDynamicId: 'a[href*="/dynamicid"]',
  pageRefClassAttr: 'a[href*="/classattr"]',
  pageRefHiddenLayers: 'a[href*="/hiddenlayers"]',
  pageRefLoadDelay: 'a[href*="/loaddelay"]',
  pageRefAjaxDelay: 'a[href*="/ajax"]',
  pageRefIgnoreDomClick: 'a[href*="/click"]',
  pageRefTextInput: 'a[href*="/textinput"]',
  pageRefScrollbars: 'a[href*="/scrollbars"]',
  pageRefDynamictable: 'a[href*="/dynamictable"]',
  pageRefProgressbar: 'a[href*="/progressbar"]',
  pageRefVisibility: 'a[href*="/visibility"]',
}

const DynamicIdPage = {
  pageLink: MainPage.pageLink + "dynamicid",
  btnText: "Button with Dynamic ID",
}

const ClassAttrPage = {
  pageLink: MainPage.pageLink + "classattr",
  btnAttr: "button.btn-primary" // "//button[contains(concat(' ', normalize-space(@class), ' '), ' btn-primary ')]",
}

// [id="greenButton"] hiddenlayers
const HiddenLayersPage = {
  pageLink: MainPage.pageLink + "hiddenlayers",
  btnAttr: '[id="greenButton"]',
  btnHiddenAttr: '[id="blueButton"]'
}

const LoadDelay = {
  pageLink: MainPage.pageLink + "loaddelay",
  btnAttr: "button.btn-primary",
  btnText: "Button Appearing After Delay",
}

const AjaxDelay = {
  pageLink: MainPage.pageLink + "ajax",
  btnAttr: 'button.btn-primary',
  btnResultAttr: '[class="bg-success"]',
  pResultText: "Data loaded with AJAX get request.",
}

const IgnoreDomClick = {
  pageLink: MainPage.pageLink + "click",
  btnAttr: "button.btn-primary",
  btnHiddenAttr: 'button.btn-success',
}

const TextInput = {
  pageLink: MainPage.pageLink + "textinput",
  btnAttr: "button.btn-primary",
  btnText: "Button That Should Change it's Name Based on Input Value",
  textInput: '[id="newButtonName"]',
}

const Scrollbars = {
  pageLink: MainPage.pageLink + "scrollbars",
  btnAttr: "button.btn-primary",
}

const Dynamictable = {
  pageLink: MainPage.pageLink + "dynamictable",
  tableAttr: '[role="table"]',
  rowgroupAttr: '[role="rowgroup"]',
  rowAttr: '[role="row"]',
  columnheaderAttr: '[role="columnheader"]',
  cellAttr: '[role="cell"]',
  labelAttr: '[class="bg-warning"]',
}

const Progressbar = {
  pageLink: MainPage.pageLink + "progressbar",
  progressbarAttr: '[id="progressBar"]',
  btnStartAttr: '[id="startButton"]',
  btnStopAttr: '[id="stopButton"]',
  attrProgressValue: 'aria-valuenow'
}

const ButtonsTable = {
  pageLink: MainPage.pageLink + "visibility",
  btnHideAttr: 'button.btn-primary',
  btn1Attr: '[id="removedButton"]',
  btn3Attr: '[id="overlappedButton"]',
  btn7Attr: '[id="offscreenButton"]',
}

exports.MainPage = MainPage;
exports.DynamicIdPage = DynamicIdPage;
exports.ClassAttrPage = ClassAttrPage;
exports.HiddenLayersPage = HiddenLayersPage;
exports.LoadDelay = LoadDelay;
exports.AjaxDelay = AjaxDelay;
exports.IgnoreDomClick = IgnoreDomClick;
exports.TextInput = TextInput;
exports.Scrollbars = Scrollbars;
exports.Dynamictable = Dynamictable;
exports.Progressbar = Progressbar;
exports.ButtonsTable = ButtonsTable;