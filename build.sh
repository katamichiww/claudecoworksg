#!/bin/sh
mkdir -p dist
cp *.html dist/
cp styles.css nav.js sitemap.xml robots.txt llms.txt dist/
cp favicon*.png apple-touch-icon.png dist/
cp -r uploads dist/
cp -r .well-known dist/
cp -r blog dist/
