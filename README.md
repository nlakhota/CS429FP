STEPS:
*Make sure, all necessary libraries are download for this project. i.e. Scrapy, Scikit-Learn, Flask, etc.*

1. Once all files have been downloaded, go ahead and head to the Crawler directory at the first level. 

2. Once there, type in “scrapy crawl mycrawler -o Crawler\\data\\output.json”. This will run the crawler on our designated website and output the data in the data folder located inside the Crawler of the second level.

3. Next, from the same directory, run the following command “python indexer.py”. This will run the indexer which will read from the “output.json” and output the following three files: inverted_index.txt, tfidf_scores.txt, product_descriptions.txt.

4. Afterwards, run the command “python flask_app.py”. This will start the server and also asks for k input.
 
5. Using another command prompt or powershell, run the following command, “python flask_request.py”. This will then ask for a query to search. Example would be: “yearlong adventure for a long time”.
 
6. Finally, top-K results will be outputted as a JSON file inside the data folder named query_result.json. 
