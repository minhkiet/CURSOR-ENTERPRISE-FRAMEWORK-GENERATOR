@echo off
cd /d "d:\PROJECTS\CURSORS\CURSOR ENTERPRISE FRAMEWORK GENERATOR"
echo Y | git filter-repo --path demos/fitness/node_modules/ --invert-paths --force
