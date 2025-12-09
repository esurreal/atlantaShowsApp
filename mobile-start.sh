#!/bin/bash

# Mobile App Start Script for Atlanta Concerts
# -----------------------------
# This script rebuilds the frontend, copies to Capacitor, and opens the mobile IDE.

set -e

FRONTEND_DIR=frontend
BUILD_DIR=dist
CAPACITOR_BASE=node_modules/.bin

# Step 1: Rebuild frontend
cd $FRONTEND_DIR
npm install
npm run build

# Step 2: Copy build to Capacitor
npx cap copy

# Step 3: Open IDEs
read -p "Open Android IDE? (y/n): " open_android
if [ "$open_android" = "y" ]; then
  npx cap open android
fi

read -p "Open iOS IDE? (y/n): " open_ios
if [ "$open_ios" = "y" ]; then
  npx cap open ios
fi

echo "Done! You can now run the app on your emulator or device."
