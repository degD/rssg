#!/bin/bash

# 0. source path. update accordingly
REPO="ssh://git@codeberg.org/redged/blog.git"

# 1. build source
set -eu
python3 build.py

# 2. clone repo pages branch to tmp
TEMP="$(mktemp -d)"
git clone --quiet --branch pages "$REPO" "$TEMP"

# 3. inside there, delete all but .git
find "$TEMP" -mindepth 1 -maxdepth 1 ! -name .git -exec rm -rf {} +

# 4. git add. if no change exit
cp -R build/. "$TEMP/"
cd "$TEMP"
git add --all
if git diff --cached --quiet; then
    echo "nothing changed."
    exit 0
fi

# 5. push to deploy
git commit -m "deploy site"
git push origin pages
