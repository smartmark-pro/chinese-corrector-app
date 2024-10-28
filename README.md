# chinese correction app demo

### How to run it on your own machine

1. Install the requirements

   ```
   $ pip install -r requirements.txt
   ```

2. Run the app

   ```
   $ streamlit run streamlit_app.py
   ```

3. run corrector model service

   .streamlit create file secrets.toml
   ```
   [remote]
   algo_url="http://0.0.0.0:9045/app/corrector/v1/corrector" 
   ```

   run 
   ```
   # todo remove github pip 
   $ pip install git+https://github.com/smartmark-pro/pycorrector.git@feature-mucgecbart
   $ python run_correct_service.py
   ```


