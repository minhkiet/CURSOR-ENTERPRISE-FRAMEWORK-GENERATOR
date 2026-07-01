@echo off
:: ============================================================
:: Cursor Enterprise Framework - Build Setup
:: Calls build_setup.ps1 for standalone exe build
:: ============================================================

powershell -ExecutionPolicy Bypass -File "%~dp0build_setup.ps1"
