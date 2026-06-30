#!/bin/zsh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
APP_NAME="Stellaris Writing"
DESKTOP_APP="$HOME/Desktop/$APP_NAME.app"
APP_CONTENTS="$DESKTOP_APP/Contents"
APP_MACOS="$APP_CONTENTS/MacOS"
APP_RESOURCES="$APP_CONTENTS/Resources"
LAUNCHER="$APP_MACOS/$APP_NAME"

notify() {
  if [ "${STELLARIS_SETUP_SILENT:-0}" = "1" ]; then
    echo "$1"
    return
  fi

  osascript -e "display dialog \"$1\" buttons {\"OK\"} default button \"OK\"" || echo "$1"
}

if ! command -v npm >/dev/null 2>&1; then
  notify "npm was not found. Please install Node.js first, then run this setup again."
  exit 1
fi

cd "$PROJECT_DIR"

if [ ! -d "node_modules" ]; then
  npm install
fi

if [ ! -f "src-tauri/icons/icon.icns" ]; then
  npm run icons:generate
fi

rm -rf "$DESKTOP_APP"
mkdir -p "$APP_MACOS" "$APP_RESOURCES"
cp "$PROJECT_DIR/src-tauri/icons/icon.icns" "$APP_RESOURCES/AppIcon.icns"

cat > "$APP_CONTENTS/Info.plist" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>CFBundleDevelopmentRegion</key>
  <string>en</string>
  <key>CFBundleDisplayName</key>
  <string>$APP_NAME</string>
  <key>CFBundleExecutable</key>
  <string>$APP_NAME</string>
  <key>CFBundleIconFile</key>
  <string>AppIcon</string>
  <key>CFBundleIdentifier</key>
  <string>com.stellaris.writing.launcher</string>
  <key>CFBundleName</key>
  <string>$APP_NAME</string>
  <key>CFBundlePackageType</key>
  <string>APPL</string>
  <key>CFBundleShortVersionString</key>
  <string>0.1.0</string>
  <key>CFBundleVersion</key>
  <string>1</string>
</dict>
</plist>
PLIST

cat > "$LAUNCHER" <<LAUNCH
#!/bin/zsh
set -euo pipefail
cd "$PROJECT_DIR"

if ! command -v npm >/dev/null 2>&1; then
  osascript -e 'display dialog "npm was not found. Please install Node.js first." buttons {"OK"} default button "OK"'
  exit 1
fi

if [ ! -d "node_modules" ]; then
  npm install
fi

npm run desktop
LAUNCH

chmod +x "$LAUNCHER"
touch "$DESKTOP_APP"

notify "Stellaris Writing has been added to your Desktop. Double-click it to launch the local desktop app."
