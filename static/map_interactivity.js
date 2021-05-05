const updateCredits = function (module_year, moduleCredits, classlist) {

  if (classlist.contains("selected")) {
    creditsArray[module_year - 1] += moduleCredits;
    } else {
    creditsArray[module_year - 1] -= moduleCredits;
  }

  let creditsDiv = document.querySelector(`.year${module_year}`);
  let numSpan = creditsDiv.querySelector("span");
  numSpan.innerText =  creditsArray[module_year - 1];
};

const moduleList = document.querySelectorAll(".module_box");

var creditsArray = [0, 0, 0, 0];
var moduleIterator = 0;

moduleList.forEach((module) => {

  let moduleCredits = parseInt(module.getAttribute("data-credits"));
  let module_year = module.getAttribute("data-year");

  let nameBox = module.querySelector(".module_name");

  nameBox.addEventListener("click", (event) => {
    module.classList.toggle("selected");
    updateCredits(module_year, moduleCredits, module.classList);
  });

  moduleIterator += 1
});
