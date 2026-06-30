# Stellaris Writing

Stellaris Writing is a local-first desktop writing check-in app built with React, Vite, and Tauri.

## Quick Start

```sh
npm install
npm run desktop
```

This opens the app as a native desktop window. It does not require Chrome or a browser tab.

## Create A Desktop Launcher On macOS

Double-click:

```text
scripts/setup-desktop-mac.command
```

The setup script will:

- install dependencies if needed
- create `Stellaris Writing.app` on your Desktop
- use the Stellaris star-map icon
- launch the local Tauri desktop app when double-clicked

For a cloned GitHub copy, the user only needs Node.js installed, then double-clicks the setup script.

## Build An Installable App

```sh
npm install
npm run desktop:build
```

The packaged macOS app will be created under:

```text
src-tauri/target/release/bundle/
```

That build is the better option when sending the app to someone who should not run it from source.

## Development Commands

```sh
npm run dev            # browser dev server
npm run desktop        # Tauri desktop dev app
npm run desktop:build  # packaged desktop app
npm run icons:generate # regenerate app icons
npm run build          # frontend production build
npm run lint           # oxlint
```
