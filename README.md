# Module Selector Web Tool

This GitHub repository contains the Module Selector Web Tool project, currently hosted at https://eo318.pythonanywhere.com/homepage/

## What is this?

The module selector web tool is an interactive diagram designed to help students with their optional module choices by presenting them visually in an interactive diagram. By tracking **module credits** and **pre-requisites/co-requisites**, we hope that this tool can be useful for students to plan their future.

After being linked to the home page, users can click through to a simple options menu where they can choose which departments and years they want displayed, before clicking through to the interactive diagram itself.

## How does it work?

1. A CSV file stores every module and its associated data. This is then imported into our Django database.
2. When the page is loaded, a HTML diagram is dynamically generated from the database, according to the options that the user has selected.
3. A Javascript file reads the HTML and sets up all of the interactivity.

Because the diagram is dynamically generated, adding/removing/updating modules is all simply done through editing and re-importing the CSV. By keeping hard-coding to a minimum, it is also relatively simple to change or add new departments.

## Authors and acknowledgment

This project was written by **Louis Clement-Harris** and **Eilish O'Grady** whilst working as Digital Learning Developers at the University of Exeter. We would also like to thank **Samuel Morrell** for his constant help and advice.
