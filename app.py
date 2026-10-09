import os

# Ưu tiên lấy từ Secrets của Streamlit nếu có, nếu không thì lấy từ ô nhập
api_key_final = st.secrets.get("AIzaSyCHz1KaZ1mdkbwaScQTxfiEtSoU-pxgm5s") or api_key
client = genai.Client(api_key=api_key_final)
