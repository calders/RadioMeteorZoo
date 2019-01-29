# RadioMeteorZoo
This code is used to upload subject sets to the Radio Meteor Zoo, or to download Zooniverse classification files and to process the observations.<br/>
I used Anaconda 3.7.1 with the Spyder IDE to develop my Python code.<br/>
Website: https://www.zooniverse.org/projects/zooniverse/radio-meteor-zoo

## Warning ##
Before I used Anaconda 2.4.0 with the Spyder IDE to develop my Python code, so some code might still need Python 2.

## Directory structure
<pre>/zooniverse Contains the Python scripts
/zooniverse/input Contains the input files; the Zooniverse classification files should be put here
/zooniverse/input/csv The BRAMS CSV files
/zooniverse/input/png The BRAMS spectrograms
/zooniverse/input/reference The BRAMS reference files (if applicable)
/zooniverse/output Contains the output files
/zooniverse/output/annotated Annotated spectrograms
/zooniverse/output/aggregated The aggregated BRAMS CSV files
/zooniverse/output/comparison Comparison result files between Zooniverse volunteers and the 'reference'
/zooniverse/output/glue GlueViz files
/zooniverse/output/pickles Some Python scripts produce .p output files (esp. if they take a long time to run)
/zooniverse/output/plots The (preliminary) meteor activity files
/zooniverse/output/png Spectrograms (usually with rectangles from the volunteers superimposed on them)</pre>

## To generate the (preliminary) meteor activity plots
* Download the latest classification file from the Zooniverse platform
* Run generate_aggregated_detection_file_from_Zooniverse_classifications-parallel.py
* Run brams_zoo_meteor_identification.py
* Run brams_zoo_identification_plot.py
* Upload the output PNG file to the FTP server

## To run the Panoptes files
You will need the Panoptes Python client: https://github.com/zooniverse/panoptes-python-client

