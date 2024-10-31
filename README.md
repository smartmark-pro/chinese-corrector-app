# 中文文本纠错应用

### 在线地址
[在线应用](https://chinese-corrector-app-78ehqwnabadjnigeaw2mzx.streamlit.app/)（可能会无法使用， 需要点击激活）

### 本地部署

1. Install the requirements

   ```
   $ pip install -r requirements.txt
   ```

2. run corrector model service
   
   （注意修改自己的配置）
   
   .streamlit 
   ```
   cp secrets.toml.example secrets.toml
   ```
   run 模型服务
   ```
   $ pip install pycorrector
   $ python run_correct_service.py
   ```

3. Run the app
   ```
   $ streamlit run streamlit_app.py
   ```