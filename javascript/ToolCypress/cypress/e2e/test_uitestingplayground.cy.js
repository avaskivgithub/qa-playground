const pages = require('./../../../pages_uitestingplayground');
const utils = require('./clients/utils');
import 'cypress-wait-until';


describe("UI Test Automation Playground http://uitestingplayground.com/", () => {

  beforeEach(() => {
    cy.visit(pages.MainPage.pageLink, { timeout: 10000});
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

    it("Dynamictable: check table content", () => {
      const testPage = pages.Dynamictable;
      let expectedValue;
      let actualValueIndex = -1;

      utils.goToPageAndCheckRedirectedLocation(pages.MainPage.pageRefDynamictable, testPage.pageLink);

      cy.get(testPage.labelAttr).then(($value) => {
        expectedValue = $value.text().split(': ')[1];
        cy.wrap(expectedValue).as('expectedValue');

        let cpuIndex;
        cy.get(testPage.tableAttr).find(testPage.rowgroupAttr).first()
          .get(testPage.rowAttr).get(testPage.columnheaderAttr).then((rows) => {
            rows.toArray().forEach((element) => {
              if (element.innerHTML.includes("CPU")) {
                cpuIndex = rows.index(element);
                cy.wrap(cpuIndex).as('cpuIndex');
              }
            });
        });

        cy.get(testPage.cellAttr).each(($cel, index, $list)=> {
            const t = $cel.text();
            //cy.log(t);
            if (t.includes('Chrome')){
              actualValueIndex = index;
            }
            if (actualValueIndex >= 0 && index == (actualValueIndex + cpuIndex)) {
              expect(t).eq(expectedValue);
            }
        });

      });
    });


    it("Progressbar: stop progress at 35%", () => {
      const testPage = pages.Progressbar;

      utils.goToPageAndCheckRedirectedLocation(pages.MainPage.pageRefProgressbar, testPage.pageLink);

      cy.get(testPage.btnStartAttr).click();
      //https://www.npmjs.com/package/cypress-wait-until
      // cy.waitUntil(() => { return cy.get('[style="width: 28%"]').should('not.exist'); })

      cy.waitUntil(() =>
        cy.get(testPage.progressbarAttr).invoke('attr', testPage.attrProgressValue).then((value) => parseInt(value) >= 35),
        {
          timeout: 30000, // waits up to 2000 ms, default to 5000
          interval: 100 // performs the check every 100 ms, default to 200
        });

      cy.get(testPage.btnStopAttr).click();
      cy.get(testPage.progressbarAttr).invoke('text').should('eq', '35%');
    });

    it('Visibility', () => {
      const testPage = pages.ButtonsTable;

      utils.goToPageAndCheckRedirectedLocation(pages.MainPage.pageRefVisibility, testPage.pageLink);

      cy.get('td').each(($cel, index, $list)=> {
        $cel.find('button').shouldBeActionable;
        cy.wrap($cel).find('button', {timeout:100}).should('be.visible');   
      });

      cy.get(testPage.btnHideAttr).click();
      cy.get(testPage.btnHideAttr).should('be.visible');
      cy.get(testPage.btn1Attr).should('not.exist');
      // TBD: btn 1 / 3 / 7 should('not.be.visible') doesn't work
      //cy.get(testPage.btn3Attr).click();
      //cy.get(testPage.btn7Attr).click();//should('not.be.visible');

      const inxs = new Set([2, 4, 5, 6]);
      cy.get('td').each(($cel, index, $list)=> {
        if (inxs.has(index)){
          cy.wrap($cel).find('button', {timeout:100}).should('not.be.visible');
        }
      });      
    });

});