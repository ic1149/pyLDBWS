# pyLDBWS
This is a simple python app to send national rail "Live Departure Boards Web Service" train times request, with tkinter GUI.
You can enter the key, CRS and WSDL version easily.
They will be put in the right position of the envelope and data will be get automaticly.
A .exe version is also included.

## Detailed description and screenshots

### main menu

![pyldbws_mainmenu](https://user-images.githubusercontent.com/126190900/222441181-a3442bb8-9e21-41ce-a08a-5d1e9e7b7b86.png)

you can enter your key, CRS, and WSDL version you wish to use and simply send a request.
There are some useful links at the right side for your convenience.

### the menu after sending the request

![pyldbws_aftersending](https://user-images.githubusercontent.com/126190900/222441791-c00bb00b-8a63-45ab-b52d-5bf34b395527.png)

click "output full data" to view complete data

### normal output window

![pyldbws_output](https://user-images.githubusercontent.com/126190900/222442092-e3fb581b-87ae-4066-b211-c64fed823c77.png)


### full output window

![pyldbws_fulloutput](https://user-images.githubusercontent.com/126190900/222442178-0b381bd5-f79b-419e-880b-94fa712a9d10.png)

### error checking

![pyldbws_error](https://user-images.githubusercontent.com/126190900/222441579-a6b13bcf-199f-46aa-86fd-e0981f47ddd6.png)

The program will check your entered information before sending the request.

## details about entering the info

-the key is 36 digits, including the hyphens
  
-please enter a key and do not use the default one (that is just a place holder!)
  
-the CRS (station code) is 3 upper case letters (although the program will automatically change it to upper case)
  
-list of CRS: https://www.nationalrail.co.uk/stations_destinations/48541.aspx
  
-the format of WSDL version is YYYY-MM-DD
  
-default WSDL version is 2021-11-01
  
-documentation of LDBWS: http://lite.realtime.nationalrail.co.uk/openldbws/
