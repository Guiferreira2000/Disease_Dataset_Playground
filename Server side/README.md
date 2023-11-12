1º In the ICD_API_Request folder you can find all files that are used to establish an API connection with the ICD 11 database. It is expected in the future to feature a file that establish a conection between the ICD 11 and the Modified_dataset.xlsx. The following links will redirect you to the location for the required documentation.

	1- ICD-API Reference:  
	   Here, you will find each and every endpoint and explanation of the fields returned by the API in a very detailed fashion.

	   This standard format of formally documenting the API has several additional benefits:

			Trying the API From this swagger URL, one can try the API by making requests and see the responses coming

			Automatic client code Generation There are several free and open source software which could generate client code in various programming languages using the Open API documentation. This will make consuming our APIs much easier in the programming language of your choice.   The swagger documentation only supports the JSON(-LD) format.
		
		link:
		https://id.who.int/swagger/index.html
	
	2-Versions of the ICD 11 code (release id)
	link:
	https://icd.who.int/icdapi/docs2/SupportedClassifications/


2º In the  Web interface folder, it is expected that the webpage renders the information available through the ICD_API_Request throw a .js file (main.js). To inspect the web page, please follow the next instructions. Also, available in the readme.txt file inside the web interface folder

	1 - Run the Flask app:
		python app.py


	The development server will automatically reload if you make any changes to the app.py file.

	Now, open your index.html file in a web browser, and you should be able to see the results of the ICD-11 API request in the browser's console.

	Remember, both the Flask server and the index.html file should be running simultaneously to see the results. To stop the Flask server, press CTRL+C in the terminal where it's running.


	2 - Visit http://127.0.0.1:5000/ or http://localhost:5000/ in your browser.
