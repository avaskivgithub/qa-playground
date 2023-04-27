const pages = require('./clients/pages');
const utils = require('./clients/utils');


describe("test uitestingplayground", () => {

  beforeEach(() => {
    cy.visit(pages.MainPage.pageLink, { timeout: 10000})
  })

    it("test Dynamic ID page", () => {
      const testPage = pages.DynamicIdPage;
      utils.goToPageAndCheckRedirectedLocation(pages.MainPage.elementDynamicId, testPage.pageLink);

      utils.getElementByLabel(testPage.elementText).click();
      utils.getElementByLabel(testPage.elementText).should('be.enabled');
      // Same with controlled timeout with Chai expect
      // Assertions will retry for up to 2 secs
      utils.checkContainTextWithTimeout(testPage.elementText, 2000 );     
    });

    it("test class attr and check that button is enabled via get with timeout", () => {
      const testPage = pages.ClassAttrPage;
      utils.goToPageAndCheckRedirectedLocation(pages.MainPage.elementClassAttr, testPage.pageLink);

      cy.get(testPage.elementAttr).click();
      utils.checkGetWithTimeout(testPage.elementAttr, 2000 );     
    });

    it("test hidden layer, check that green button can not be hit twice", () => {
      const testPage = pages.HiddenLayersPage;

      utils.goToPageAndCheckRedirectedLocation(pages.MainPage.elementHiddenLayers, testPage.pageLink);

      cy.get(testPage.elementHiddenAttr).should('not.exist');

      cy.get(testPage.elementAttr).then(($selectedElement) => {
        debugger;
        $selectedElement.get(0).click();
      });
      cy.log("debugger did not work :( because tests were opned not on Electron");
      console.log("why logging is not obvious?");

      cy.get(testPage.elementHiddenAttr).should('exist');
      cy.get(testPage.elementAttr).shouldNotBeActionable;
      cy.get(testPage.elementHiddenAttr).shouldBeActionable;    
    });

    it("test page load delay and check button label", () => {
      const testPage = pages.LoadDelay;
      utils.goToPageAndCheckRedirectedLocation(pages.MainPage.elementLoadDelay, testPage.pageLink, 5000);
      utils.checkGetWithTimeout(testPage.elementAttr, 2000 );     
      cy.get(testPage.elementAttr).contains(testPage.elementText);
    });

  });