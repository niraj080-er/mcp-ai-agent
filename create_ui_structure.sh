#!/bin/bash

# Root folder
ROOT="ui"

# Create directories
mkdir -p $ROOT/src

# Create files in root
touch $ROOT/index.html
touch $ROOT/package.json
touch $ROOT/vite.config.js
touch $ROOT/.env

# Create files in src
touch $ROOT/src/main.jsx
touch $ROOT/src/App.jsx
touch $ROOT/src/api.js
touch $ROOT/src/styles.css

echo "UI folder structure created successfully!"