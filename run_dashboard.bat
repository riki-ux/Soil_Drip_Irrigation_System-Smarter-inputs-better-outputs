@echo off
call .venv\Scripts\activate
streamlit run app.py --server.headless false
pause
.\run_dashboard.bat
