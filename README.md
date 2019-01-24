This repository contain the all data and scripts used in the pipeline of Data Integration project of Knowledge and Data Integration course. 
The files contained are:
  -Data_Scraping_PNE.py, python script for the Data scraping process, performed using the python library "Beautifulsoup" and      "requests" 
  -Hosp_geocoding.py, python script for the geocoding process, performed with the "googlemaps" python library and "difflib",      this last library was used to found the best string match for the hospital name in the "Ospedali.xls" Excel file.
  -Hospital_latlng.csv, comma-separated file containing latitude and longitude of the Hospitals obtained with Hosp_geocoding.py
  -Ospedali.xls, Excel file containing address and some other data of every italian hospital
  -default_sintesi_stru_ajax.php.html, html file used to perform the Data scraping process.
  -Exam_group8_HealthcareFaacility directory that contain:
    -KDI_Data_Integration_ProjetReport_HealthcareFacilityGroup8.pdf, project report
    -FINAL_ONTOLOGY.owl, final version of our ontology
    -Evaluation of the Model_HealthcareFacilityGroup8.pdf, evaluation of our project
    -geo_2007.owl, ontology for the geospatial data
    -Models, directory contain all the ttl file of our model
    -RDF_data, directory contain all the ttl file of our rdf file obtained from the integration of Karma
    
