import Module from "./Module.js";

class DiagramController{
  constructor(
    moduleQuery,
    creditsDisplay,
  ) {
    this.moduleQuery = moduleQuery;
    this.creditsDisplay = creditsDisplay;

    this.creditsArray = [0, 0, 0, 0];
    this.moduleList = [];
    this.moduleCodes = [];
    this.selectedModuleCodes = [];

    this.initModuleObjects()
    this.testForMissingYears()
  }

  initModuleObjects() {
    /**
     * Create a list of one module object per module in the diagram, then
     * activate their interactivity
     */

    this.moduleQuery.forEach((module) => {
      this.moduleList.push(new Module(module, this, this.creditsArray));
    });

    this.moduleList.forEach((module) => {
      module.initInteractivity(this.moduleList, this.moduleCodes);
    });
  };

  updateRequisites(moduleObject, moduleClassList){
    /**
     * Updates the list of modules that have been selected, then checks to see
     * if any requisite flags need to be updated.
     * @param {object} moduleObject - The module object being selected/deselected
     * @param {list} moduleClassList - The list of classes belonging to the
     * model's corresponding HTML object
     */

    if (moduleClassList.contains("selected")){
      // if module was just selected, add its code to the list of selected modules
      this.selectedModuleCodes.push(moduleObject.code);
    } else {
      // else if the module was just deselected, remove its code from the list.
      let id = this.selectedModuleCodes.indexOf(moduleObject.code);
      this.selectedModuleCodes.splice(id,  1);
    };

    moduleObject.inversePreReqs.forEach((targetModule) => {
      this.testPreReqsFulfilled(targetModule)
    });
    moduleObject.inverseCoReqs.forEach((targetModule) => {
      this.testCoReqsFulfilled(targetModule)
    });

    this.testForMissingPreReq();
    this.testForMissingCoReq();
    this.testForWeirdModule();
  };

  testPreReqsFulfilled(targetModule){
    /**
    * Check whether or not at least one of the  pre-requisite list options has
    * been fulfilled, and update flags accordingly
    * @param {object} targetModule - The module whose pre-requisites may need updating
    */

    let moduleClassList = targetModule.moduleBox.classList

    let isFulfilled = false

    // For each pre-requisite list options...
    targetModule.preReq.forEach((reqsList) => {

      let listLength = reqsList.length;

      // ... count the number of pre-requisites that have already been selected ...
      reqsList.forEach((preReq) => {
        if (this.selectedModuleCodes.includes(preReq)) {
          listLength -= 1;
        };
        // ... if all of them have been, set isFulfilled = True.
        if (listLength == 0) {
          isFulfilled = true;
        };
      });
    });

    // Update the flag  to match whether or not the module's pre-requisites have
    // been fulfilled.
    if (isFulfilled == false) {
      if (moduleClassList.contains("denied")) {
        } else {
          moduleClassList.toggle("denied")
        }
      } else {
        if (moduleClassList.contains("denied")) {
          moduleClassList.toggle("denied")
          }
      }
  };

  testCoReqsFulfilled(targetModule){
    /**
    * Check whether or not at least one of the  co-requisite list options has
    * been fulfilled, and update flags accordingly
    * @param {object} targetModule - The module whose co-requisites may need updating
    */

    let moduleClassList = targetModule.moduleBox.classList

    let isFulfilled = false

    // For each pre-requisite list options...
    targetModule.coReq.forEach((reqsList) => {

      let listLength = reqsList.length;

      // ... count the number of pre-requisites that have already been selected ...
      reqsList.forEach((coReq) => {
        if (this.selectedModuleCodes.includes(coReq)) {
          listLength -= 1;
        };
        // ... if all of them have been, set isFulfilled = True.
        if (listLength == 0) {
          isFulfilled = true;
        };
      });
    });

    // Update the flag  to match whether or not the module's pre-requisites have
    // been fulfilled.
    if (isFulfilled == false) {
      if (moduleClassList.contains("warning")) {
        } else {
          moduleClassList.toggle("warning")
        }
      } else {
        if (moduleClassList.contains("warning")) {
          moduleClassList.toggle("warning")
          }
      }
  };

  testForMissingPreReq(){

    if (document.querySelector(".deniedDiv")) {
      document.querySelector(".deniedDiv").remove()
    }

    const creditsDiv = document.querySelector(".credits");

    const selectedDeniedModules = document.querySelectorAll(".selected.denied")

    if (selectedDeniedModules.length != 0){
      const warningMessage = `<p>You may not have all of the pre-requisites listed for the selected modules :</p>
      <p><span></span></p>
      <p>Please contact the relevant module leaders if you would like to choose these options</p>`;

      const warningDiv = document.createElement("div");
      warningDiv.classList.add("deniedDiv");
      warningDiv.innerHTML = warningMessage;

      creditsDiv.append(warningDiv);

      let missingModulesSpan = creditsDiv.querySelector(".deniedDiv span");
      for (const module of selectedDeniedModules){
          missingModulesSpan.innerHTML += module.querySelector(".module_name").innerText
          missingModulesSpan.innerHTML += "</br>"
        }
    }
  }

  testForMissingCoReq(){

    if (document.querySelector(".warningDiv")) {
      document.querySelector(".warningDiv").remove()
    }

    const creditsDiv = document.querySelector(".credits");

    const selectedDeniedModules = document.querySelectorAll(".selected.warning")

    if (selectedDeniedModules.length != 0){
      const warningMessage = `<p>You may not have all of the co-requisites listed for the selected modules :</p>
      <p><span></span></p>
      <p>Please contact the relevant module leaders if you would like to choose these options</p>`;

      const warningDiv = document.createElement("div");
      warningDiv.classList.add("warningDiv");
      warningDiv.innerHTML = warningMessage;

      creditsDiv.append(warningDiv);

      let missingModulesSpan = creditsDiv.querySelector(".warningDiv span");
      for (const module of selectedDeniedModules){
          missingModulesSpan.innerHTML += module.querySelector(".module_name").innerText
          missingModulesSpan.innerHTML += "</br>"
        }
    }
  }

  testForWeirdModule(){

    if (document.querySelector(".weirdDiv")) {
      document.querySelector(".weirdDiv").remove()
    }

    const creditsDiv = document.querySelector(".credits");

    const selectedDeniedModules = document.querySelectorAll(".selected.weird")

    if (selectedDeniedModules.length != 0){
      const warningMessage = `<p>Please check the detailed module information for :</p>
      <p><span></span></p>`;

      const warningDiv = document.createElement("div");
      warningDiv.classList.add("weirdDiv");
      warningDiv.innerHTML = warningMessage;

      creditsDiv.append(warningDiv);

      let missingModulesSpan = creditsDiv.querySelector(".weirdDiv span");
      for (const module of selectedDeniedModules){
          missingModulesSpan.innerHTML += module.querySelector(".module_name").innerText
          missingModulesSpan.innerHTML += "</br>"
        }
    }
  }

  testForMissingYears(){

    const creditsDiv = document.querySelector(".credits");

    let missingYear = false

    if (creditsDiv.querySelector(".year1")){} else{
      missingYear = true
    }

    if (creditsDiv.querySelector(".year2")){} else{
      missingYear = true
    }

    if (creditsDiv.querySelector(".year3")){} else{
      missingYear = true
    }

    if (missingYear){
      const warningMessage = `<p>Warning: Not all years selcted. Pre-requisites calculate assuming that you have all required modules from missing years</p>`;

      const noYearDiv = document.createElement("div");
      noYearDiv.classList.add("noYearDiv");
      noYearDiv.innerHTML = warningMessage;

      creditsDiv.append(noYearDiv);
    }
  }
}

export default DiagramController;
