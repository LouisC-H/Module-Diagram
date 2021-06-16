import DiagramController from "./DiagramController.js";

// Initialise a list of all module objects in the diagram
const moduleQuery = document.querySelectorAll(".module_box");
const creditsDisplay = document.querySelector(`.credits`);

const dController = new DiagramController(moduleQuery, creditsDisplay);
