const deptsForm = document.querySelector(".depts_selector");
const deptsCheckboxes = deptsForm.querySelectorAll("input")
const yearsForm = document.querySelector(`.years_selector`);
const yearsCheckboxes = yearsForm.querySelectorAll("input")
const goButton = document.querySelector(`button`);
const urlRoot = window.location.href.slice(0, -13)

goButton.addEventListener("click", (event) => {

  let deptsList = []
  let yearsList = []

  iterator = 0;

  deptsCheckboxes.forEach((checkbox) => {
    if (checkbox.checked) {
      deptsList.push("1")
    } else {
      deptsList.push("0")
    }
    iterator += 1;
  });
  deptsList = deptsList.join("");
  iterator = 0;
  yearsCheckboxes.forEach((checkbox) => {
    if (checkbox.checked) {
      yearsList.push("1")
    } else {
      yearsList.push("0")
    }
    iterator += 1;
  });
  yearsList = yearsList.join("");
  location.href = urlRoot+deptsList+yearsList+"/";
});
