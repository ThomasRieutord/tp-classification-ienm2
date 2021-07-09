#!/usr/bin/bash
# Download the necessary data from Meteonet and uncompress it

echo "Starting the download (this may take some time)"

mkdir no_save
cd no_save

echo " [1/4] Downloading observation data"
wget https://meteonet.umr-cnrm.fr/dataset/data/SE/ground_stations/SE_ground_stations_2018.tar.gz

echo " [2/4] Downloading model data"
wget https://meteonet.umr-cnrm.fr/dataset/data/SE/weather_models/2D_parameters/SE_weather_models_2D_parameters_2018.tar.gz

echo " [3/4] Uncompressing observation data"
tar xzf SE_ground_stations_2018.tar.gz

echo " [4/4] Uncompressing model data"
tar --to-command='tar -xzf -' -xzf SE_weather_models_2D_parameters_2018.tar.gz

cd ..

echo "Download and uncompression successfully done! Now starting the data preparation."

conda activate meteonet_toolbox
python prepare_data.py
conda deactivate

echo "Done! Data is ready for pratical work"
