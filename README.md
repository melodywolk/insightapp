# TindArt
TindArt is a web application to allow users to find their match in art, people sharing their tastes and discover new art around them using Flickr photos. Only pictures with #painting and geolocation metadata are considered.
Photographs of paintings are analyzed using a deep learning model based on Fine-tuning CaffeNet for Style Recognition on [Flickr Style](http://sergeykarayev.com/files/1311.3715v3.pdf), to predict image style instead of object category.

## Setup
Install the dependencies for the web server using `pip install -r requirements.txt`.
Then the primary dependency is [Caffe](http://caffe.berkeleyvision.org/). 

Download and compile pycaffe using the [installation instructions](http://caffe.berkeleyvision.org/installation.html), then edit the `views.py` file to point to your SQL database and other files that you may need.

They provide a model trained on 80K images, with final accuracy of 39%. This model outputs 20 differents styles related to
* Optical techniques: Macro, Bokeh, Depth-of-Field, Long Exposure, HDR
* Atmosphere: Hazy, Sunny
* Mood: Serene, Melancholy, Ethereal
* Composition styles: Minimal, Geometric, Detailed, Texture
* Color: Pastel, Bright
* Genre: Noir, Vintage, Romantic, Horror

and their associated probabilities.

After installing caffe, simply do `./scripts/download_model_binary.py models/finetune_flickr_style` to obtain it.

Finally, run the Flask web server via

`sudo python run.py`

## Database Generation

The `readtables.py` file is meant to work with csv files from the Flickr 100M photo set that ce be obtained [here](http://yahoolabs.tumblr.com/post/89783581601/one-hundred-million-creative-commons-flickr-images). After downloading and extracting the files the images can be classified via python using `get_classify_images.py`. To get more recent results from Flickr use `Flickr_stream.py`. Each time the fileset is added to your MySQL database.
`get_user_info.py` is used to get profiles metadata and point the user to its match.
Have fun!