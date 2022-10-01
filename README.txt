How to run this API:
    main script to run : App.py
    there are 3 section in API, 
        1. "Hello World" Basic API, to show how basic flask API work
        2. "Text Processing" API, to process inputted text in provided field in the API
        3. "File Processing" API, to process inputted CSV file* in provided field in the API (it will takes time based on how much data in the CSV)
            you can access processed file in "http://127.0.0.1:5000/download", since this API is running in internal server

What does "Text Processing" and "File Processing" do?
    the API will process the inputted text/file so that there are no more unnecessary character in the text so the text will look more tidier, 
    moreover, the API also will also replace non-formal word to formal (in Bahasa) word that already provided in "kamusalay.csv"

Processed data will be inputted to our "text_processing.db" database for documentation porpuse


*Data should be in the first column of the CSV