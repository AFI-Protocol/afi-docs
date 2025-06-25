#!/bin/bash
git init
git remote add origin git@github.com:AFI-Protocol/afi-docs.git
git add .
git commit -m "Initial commit for afi-docs"
git push -u origin main
