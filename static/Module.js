class Module{
  constructor(
    // The moduleBox html object which displays this module
    moduleBox,
    // The diagramController object stores large-scale data
    diagramController,
  ) {
    // retrieve information stored in moduleBox's classes
    this.name = moduleBox.querySelector(".module_name").innerText
    this.code = moduleBox.getAttribute("data-code")
    this.code = this.code.replace(/\s/g, '')
    this.year = moduleBox.getAttribute("data-year");
    this.credits = parseInt(moduleBox.getAttribute("data-credits"));

    this.preReq =  moduleBox.getAttribute("data-prereq")
    this.preReqsLinear = []
    this.inversePreReqs = []

    this.coReq =  moduleBox.getAttribute("data-coreq")
    this.coReqsLinear = []
    this.inverseCoReqs = []

    this.dController = diagramController
    this.dController.moduleCodes.push(this.code);

    // retrieve refeence to various html objects
    this.moduleBox = moduleBox
    this.creditsDiv = this.dController.creditsDisplay.querySelector(`.year${this.year}`);
  }

  initInteractivity(moduleList, moduleCodes) {
    /**
    * Once all of the module objects have been created, call this function to
    * initialise them to be interactible, inc adding an on-click event listerner
    * @param {object} moduleList - List of the module objects.
    * @param {object} moduleCodes - List of the module's codes.
    */

    // Interpret requisites into structured lists
    let preReqReturns = this.interpretRequisites(this.preReq, this.dController.moduleCodes)
    this.preReq = preReqReturns [0]
    this.preReqsLinear = preReqReturns [1]
    let coReqReturns = this.interpretRequisites(this.coReq, this.dController.moduleCodes)
    this.coReq = coReqReturns [0]
    this.coReqsLinear = coReqReturns [1]

    // Inform the modules that are requisite to this one.
    this.inverseRequisites(moduleList)

    // Set flags according to whether or not the module has pre/co-requisites
    this.setInitialFlags(this.preReqsLinear, this.coReqsLinear, this.moduleBox.classList)

    // Add an event listerner to allow user to select modules
    this.moduleBox.addEventListener("click", (event) => {
      this.selectModule(this.year, this.credits, this.moduleBox, this.creditsDiv, this.dController);
      // this.updatePreRequisites(this.inversePreReqs, moduleList, this.moduleBox.classList, this.code);
      // // Check to see if the module is missing a prerequisite
      // this.testForMissingPreReq();

    });

  }

  setInitialFlags(preReqsList, coReqsList, classList){
    /**
     * Assign "denied" flags to modules with pre-requisites and "warning"
     * labels to complex cases or those with co-requisites
     * @param {list} preReqsList - List containing pre-requisites
     * @param {list} coReqsList - List containing co-requisites
     * @param {classList} classlist - List of the classes of the module box object.
     */

    if (preReqsList == "Warning"|| coReqsList == "Warning") {
      classList.toggle("weird");
      } else {
        if (preReqsList != "N/A") {
          classList.toggle("denied");};
        if (coReqsList != 'N/A') {
          classList.toggle("warning");};
      }


  }

  selectModule(moduleYear, moduleCredits, moduleBox, creditsDiv, dController) {
    /**
     * Set the flags to toggle a module between selected and un-selected, and
     * update credits and requisites.
     * @param {string} module_year - Should be a single digit between 1 and 4 inclusive,
     * corresponding to the year in which students can take the module.
     * @param {number} moduleCredits - The number of credits that the module corresponds to.
     * @param {string} moduleCode - The code of the module being selected.
     * @param {object} moduleBox - Reference to the HTML object displaying the module.
     * @param {object} creditsDiv - List of the object displaying the number of credits.
     * @param {object} dController - parent object tracking "global" variables
     */

    // Update the number of credits selected
    let creditsArray = dController.creditsArray
    let classList = moduleBox.classList

    classList.toggle("selected");

    if (classList.contains("selected")) {
      creditsArray[moduleYear - 1] += moduleCredits;
      } else {
      creditsArray[moduleYear - 1] -= moduleCredits;
    }

    // Update the text in the credits tracker
    let numSpan = creditsDiv.querySelector("span");
    numSpan.innerText =  creditsArray[moduleYear - 1];

    dController.updateRequisites(this, classList);
  };

  interpretRequisites(requisites, moduleCodes){
    /**
     * For a string of requisites, eleminate any corresponding to non-selected modules,
     * then interpret the "and" and "or"s to for a nested list
     * @param {string} requisites - String corresponding to the codes of
     * Pre/Co-requisite modules, separated by "and"/"or" syntax
     * @return {list} Properly formatted list of requisites.
     */

    // extract the string from the object
    if (requisites == ''){
      return ['N/A', 'N/A']
    }
    let num_requisites = 0
    let interpretedReqs = []
    let linearReqs = []

    // split the pre-requisites at each " or "
    requisites.split(" or ").forEach((orsplit) => {
      // split again at each " and "
      let individualReqs = [];
      orsplit.split(" and ").forEach((requisite) => {
        // Remove any spaces that shouldn't be there
        let codeString = requisite.replace(/\s/g, '');
        if (moduleCodes.includes(codeString) || codeString == "Warning"){
          individualReqs.push(codeString);
          linearReqs.push(codeString);
          num_requisites += 1
        } else {
        }
      });
      interpretedReqs.push(individualReqs)
    });

    if (num_requisites == 0){
      return ['N/A', 'N/A']
    } else {
      return [interpretedReqs, linearReqs]
    }
  }

  inverseRequisites(moduleList) {
    /**
     * Find the list of modules that this module is a requisite of, and save
     * it as this.inversePreReqs
     * @param {array} moduleList - array containing the list of module objects on
     * the page.
     */

     if (this.preReqsLinear != "N/A"){
       this.preReqsLinear.forEach((preReq) => {
         moduleList.forEach((module) => {
           if (module.code == preReq) {
             module.inversePreReqs.push(this);
           }
         });
       });
     }

     if (this.coReqsLinear != "N/A"){
       this.coReqsLinear.forEach((coReq) => {
         moduleList.forEach((module) => {
           if (module.code == coReq) {
             module.inverseCoReqs.push(this);
           }
         });
       });
     }
  }

}

export default Module;
