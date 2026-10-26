# To-Do-List-Application

A simple, browser-based to-do list for managing daily activities. Add tasks, mark them as completed, filter them, and delete them. Tasks are saved in the browser, so they are still there after you reload the page.

## Features

- Add a task with the button or the Enter key
- Mark a task as completed or pending with its checkbox
- Filter tasks by All, Pending, or Completed, with a count for each
- Delete a single task, or clear all completed tasks at once
- Empty-state messages and a running count of tasks left
- Saved automatically in `localStorage`
- Responsive layout for phones and desktops, keyboard accessible, and respects reduced-motion settings

## Project Structure

```
To-Do-List-Application/
├── index.html   # Page structure
├── style.css    # Styling and responsive layout
├── script.js    # Task logic and DOM manipulation
├── README.md    # Project documentation
└── screenshots/ # Output screenshots
```

## How to Run

No build step or dependencies are needed.

1. Download or clone this repository.
2. Open `index.html` in any modern web browser.

## How It Works

- **DOM manipulation:** `script.js` creates the task elements with `document.createElement` and redraws the list whenever the data changes.
- **State:** Tasks are stored as objects (`{ id, text, done }`) in an array and saved to `localStorage` after each change.
- **Security:** Task text is inserted with `textContent`, so anything typed is shown as plain text.

## Screenshots

Screenshots of the running application are in the `screenshots/` folder.

## Author

Your Name — Roll No: 000000
