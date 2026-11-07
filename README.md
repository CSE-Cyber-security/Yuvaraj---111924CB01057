# Password Strength Checker

A small, dependency-free web app that scores a password as you type. Everything runs in the browser, so the password is never stored or sent anywhere.

## Screenshots

| Empty | Weak | Very strong |
|---|---|---|
| ![Empty](screenshots/01-empty.png) | ![Weak](screenshots/02-weak.png) | ![Very strong](screenshots/03-strong.png) |

## Features

- Five-level strength meter (Very weak to Very strong)
- Live checklist: length, lowercase, uppercase, number, symbol, common pattern
- Entropy estimate in bits and an estimated time to crack
- Show/Hide toggle for the password field
- Storm-grey and green terminal-style theme with a monospace font
- Responsive layout, keyboard focus styles, reduced-motion support

## Project structure

```
password-strength-checker/
├── index.html
├── style.css
├── script.js
├── README.md
└── screenshots/
```

## Run it

Open `index.html` in any modern browser. No build step or install needed.

## How the score works

1. The character pool is estimated from the types used (26 lowercase, 26 uppercase, 10 digits, 32 symbols).
2. Entropy is `length x log2(pool)`, reduced for repeated characters.
3. Common words and keyboard patterns (for example `password`, `qwerty`, `123456`) cap the entropy at 20 bits.
4. Time to crack assumes an offline attacker making 10 billion guesses per second and averages half the search space.

| Entropy | Level |
|---|---|
| under 28 bits | Very weak |
| 28 to 39 | Weak |
| 40 to 59 | Fair |
| 60 to 79 | Strong |
| 80 or more | Very strong |

## Limitations

This is an educational estimate, not a security guarantee. It does not check breach databases or dictionary words beyond a short built-in list. Use a password manager and unique passwords for each account.

## Publish on GitHub Pages

1. Push the folder to a repository.
2. Go to Settings > Pages, choose the `main` branch and the `/ (root)` folder.
3. Your site will be live at `https://<username>.github.io/<repo>/`.

## License

MIT
