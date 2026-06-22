with open(".venv/lib/python3.14/site-packages/streamlit/static/static/js/index.dkY5s53S.js", "r", encoding="utf-8") as f:
    content = f.read()

target = "RH=G("
idx = content.find(target)
print("RH=G( index:", idx)
if idx != -1:
    print(content[idx-100:idx+900])

