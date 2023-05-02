const pages = require('./../../../pages_uitestingplayground');
const utils = require('./clients/utils');


describe("UI Test Automation Playground http://uitestingplayground.com/", () => {

  beforeEach(() => {
    cy.visit(pages.MainPage.pageLink, { timeout: 10000})
  })

    it("Dynamic ID: test Dynamic ID page", () => {
      const testPage = pages.DynamicIdPage;
      utils.goToPageAndCheckRedirectedLocation(pages.MainPage.pageRefDynamicId, testPage.pageLink);

      utils.getElementByLabel(testPage.btnText).click();
      utils.getElementByLabel(testPage.btnText).should('be.enabled');
      // Same with controlled timeout with Chai expect
      // Assertions will retry for up to 2 secs
      utils.checkContainTextWithTimeout(testPage.btnText, 2000 );     
    });

    it("Class Attribute: test class attr and check that button is enabled via get with timeout", () => {
      const testPage = pages.ClassAttrPage;
      utils.goToPageAndCheckRedirectedLocation(pages.MainPage.pageRefClassAttr, testPage.pageLink);

      cy.get(testPage.btnAttr).click();
      utils.checkGetWithTimeout(testPage.btnAttr, 2000 );     
    });

    it("Hidden Layers: test hidden layer, check that green button can not be hit twice", () => {
      const testPage = pages.HiddenLayersPage;

      utils.goToPageAndCheckRedirectedLocation(pages.MainPage.pageRefHiddenLayers, testPage.pageLink);

      cy.get(testPage.btnHiddenAttr).should('not.exist');

      cy.get(testPage.btnAttr).then(($selectedElement) => {
        debugger;
        $selectedElement.get(0).click();
      });
      cy.log("debugger did not work :( because tests were opned not on Electron");
      console.log("why logging is not obvious?");

      cy.get(testPage.btnHiddenAttr).should('exist');
      cy.get(testPage.btnAttr).shouldNotBeActionable;
      cy.get(testPage.btnHiddenAttr).shouldBeActionable;    
    });

    it("Load Delay: test page load delay and check button label", () => {
      const testPage = pages.LoadDelay;
      utils.goToPageAndCheckRedirectedLocation(pages.MainPage.pageRefLoadDelay, testPage.pageLink, 5000);
      utils.checkGetWithTimeout(testPage.btnAttr, 2000 );     
      cy.get(testPage.btnAttr).contains(testPage.btnText);
    });

    it("AJAX Data: test AJAX request with delay and check result text", () => {
      const testPage = pages.AjaxDelay;
      utils.goToPageAndCheckRedirectedLocation(pages.MainPage.pageRefAjaxDelay, testPage.pageLink);

      cy.get(testPage.btnAttr).click();
      cy.get(testPage.btnResultAttr).should('not.exist');
      utils.checkContainTextWithTimeout(testPage.pResultText, 17000 );
      cy.get(testPage.btnResultAttr).should('exist'); 
    });

    it("Click: test to make sure that it is able to click the button", () => {
      const testPage = pages.IgnoreDomClick;

      utils.goToPageAndCheckRedirectedLocation(pages.MainPage.pageRefIgnoreDomClick, testPage.pageLink);

      cy.get(testPage.btnAttr).should('exist');
      cy.get(testPage.btnAttr).shouldBeActionable;
      cy.get(testPage.btnHiddenAttr).should('not.exist');

      cy.get(testPage.btnAttr).click();

      cy.get(testPage.btnAttr).should('not.exist');
      cy.get(testPage.btnHiddenAttr).should('exist');
      cy.get(testPage.btnHiddenAttr).shouldBeActionable;    
    });

    it("Text Input: test entering text into an edit field has effectl", () => {
      const testPage = pages.TextInput;
      const testNewBtnName = "My new label" + Date();

      utils.goToPageAndCheckRedirectedLocation(pages.MainPage.pageRefTextInput, testPage.pageLink);   
      cy.get(testPage.btnAttr).contains(testPage.btnText);

      cy.get(testPage.textInput).type(testNewBtnName);
      cy.get(testPage.btnAttr).click();

      cy.get(testPage.btnAttr).contains(testNewBtnName);
    });

    it("Scrollbars: test to make sure that it is able to click the button", () => {
      const testPage = pages.Scrollbars;

      utils.goToPageAndCheckRedirectedLocation(pages.MainPage.pageRefScrollbars, testPage.pageLink);

      //cy.get('[style="height:150px;"]').scrollTo('center'); // don't really need this
      cy.get(testPage.btnAttr).shouldBeActionable;

      cy.get(testPage.btnAttr).click();

      cy.get(testPage.btnAttr).shouldBeActionable;   
    });
  });