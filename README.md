# Mycroft Precise

*A lightweight, simple-to-use, RNN wake word listener.*

Precise is a wake word listener.  The software monitors an audio stream ( usually a microphone ) and when it recognizes a specific phrase it triggers an event.  For example, at Mycroft AI the team has trained Precise to recognize the phrase "Hey, Mycroft".  When the software recognizes this phrase it puts the rest of Mycroft's software into command mode and waits for a command from the person using the device.  Mycroft Precise is fully open source and can be trined to recognize anything from a name to a cough.

In addition to Precise there are several proprietary wake word listeners out there.  If you are looking to spot a wakeword Precise might be a great solution, but if it's too resource intensive or isn't accurate enough here are some [alternative options][comparison].

[comparison]: https://github.com/MycroftAI/mycroft-precise/wiki/Software-Comparison

## Supported Operating Systems

Precise is designed to run on Linux.  It is known to work on a variety of Linux distributions including Debian, Ubuntu and Raspbian.  It probably operates on other \*nx distributions.

## Training Models

### Communal models

Training takes lots of data. The Mycroft community is working together to jointly
build datasets at: 
https://github.com/MycroftAI/precise-community-data.   
These datasets are available for anyone to download, use and contribute to. A number 
of models trained from this data are also provided.

The official models selectable in your device settings at Home.mycroft.ai 
[can be found here](https://github.com/MycroftAI/precise-data/tree/models).  

Please come and help make things better for everyone!

### Train your own model

You can find info on training your own models [here][train-guide]. It requires
running through the [**source install instructions**][source-install] first.

[train-guide]:https://github.com/MycroftAI/mycroft-precise/wiki/Training-your-own-wake-word#how-to-train-your-own-wake-word
[source-install]:https://github.com/MycroftAI/mycroft-precise#source-install

## Installation

If you just want to use Mycroft Precise for running models in your own application,
you can use the binary install option. Note: This is only updated to the latest release,
indicated by the latest commit on the master branch. If you want to train your own models
or mess with the source code, you'll need to follow the **Source Install** instructions below.

### Binary Install

First download `precise-engine.tar.gz` from the [precise-data][precise-data] GitHub
repo. This will get the latest stable version (the master branch). Note that this requires the models to be built the the same latest version in the master branch. Currently, we support both 64 bit Linux desktops (x86_64) and the Raspberry Pi (armv7l).

[precise-data]: https://github.com/mycroftai/precise-data/tree/dist

Next, extract the tar to the folder of your choice. The following commands will work for the pi:

```bash
ARCH=armv7l
wget https://github.com/MycroftAI/precise-data/raw/dist/$ARCH/precise-engine.tar.gz
tar xvf precise-engine.tar.gz
```

Now, the Precise binary exists at `precise-engine/precise-engine`.

Next, install the Python wrapper with `pip3` (or `pip` if you are on Python 2):

```bash
sudo pip3 install precise-runner
```

Finally, you can write your program, passing the location of the precise binary like shown:

```python
#!/usr/bin/env python3

from precise_runner import PreciseEngine, PreciseRunner

engine = PreciseEngine('precise-engine/precise-engine', 'my_model_file.pb')
runner = PreciseRunner(engine, on_activation=lambda: print('hello'))
runner.start()

# Sleep forever
from time import sleep
while True:
    sleep(10)
```

### Source Install

Start out by cloning the repository:

```bash
git clone https://github.com/mycroftai/mycroft-precise
cd mycroft-precise
```

If you would like your models to run on an older version of precise, like the
stable version the binary install uses, check out the master branch.

Next, install the necessary system dependencies. If you are on Ubuntu, this
will be done automatically in the next step. Otherwise, feel free to submit
a PR to support other operating systems. The dependencies are:

 - python3-pip
 - libopenblas-dev
 - python3-scipy
 - cython
 - libhdf5-dev
 - python3-h5py
 - portaudio19-dev

After this, run the setup script:

```bash
./setup.sh
```

Finally, you can write your program and run it as follows:
```bash
source .venv/bin/activate  # Change the python environment to include precise library
```
Sample Python program:
```python
#!/usr/bin/env python3

from precise_runner import PreciseEngine, PreciseRunner

engine = PreciseEngine('.venv/bin/precise-engine', 'my_model_file.pb')
runner = PreciseRunner(engine, on_activation=lambda: print('hello'))
runner.start()

# Sleep forever
from time import sleep
while True:
    sleep(10)
```

In addition to the `precise-engine` executable, doing a **Source Install** gives you
access to some other scripts. You can read more about them [here][executables].
One of these executables, `precise-listen`, can be used to test a model using
your microphone:

[executables]:https://github.com/MycroftAI/mycroft-precise/wiki/Training-your-own-wake-word#how-to-train-your-own-wake-word

```bash
source .venv/bin/activate  # Gain access to precise-* executables
precise-listen my_model_file.pb
```

## How it Works

At it's core, Precise uses just a single recurrent network, specifically a GRU.
Everything else is just a matter of getting data into the right form.

![Architecture Diagram](https://images2.imgbox.com/f7/44/6N4xFU7D_o.png)

## How to use

### Activate environment
First of all, activate the precise environment.

```bash
source .venv/bin/activate  # Change the python environment to include precise library
```

### Collect data
Collect wakeword and non-wakeword audio file.

```bash
precise-collect datakit/wakeword/wakeword##
```

and the audio file will be saved to the directory you have assigned. 
There is a folder ./datakit for you to collect and save the audio file in diffirent 
folder classified by their characteristics.

### Classify the audio file into train and test set
Put the wakeword and non-wakeword audio file into the ./wake-word and ./not-wake-word folder manually
and run the python file as follows.

```bash
python3 classifier.py
```

and the file in ./wake-word and ./not-wake-word folder will be automatically classified to train set 
and test set in ./dataset directory as the content shows below.

```shell
dataset/
├── wake-word/
├── not-wake-word/
└── test/
    ├── wake-word/
    └── not-wake-word/
```

### Train
Now we can run the train process.

```bash
precise-train -e 50 wakeword.net dataset/
```

`-e` is the epoch param of training, `wakeword.net` is the output model file name
and `dataset/` is the dataset directory generated by classifying step.

### Test
We use the following instruction to test our model.

```bash
precise-test wakeword.net dataset/
```

`wakeword.net` is the dataset we want to test. `dataset/` is the dataset directory 
generated by classifying step.

and we can test it again with microphone in the real scenes.

```bash
precise-listen wakeword.net
```

### Convert
For some specific application, we have to convert the .net file to .pb file.

```bash
precise-convert wakeword.net
```

Then, we will get a `wakeword.pb` file in root directory.

## Errors solving

### Use python 3.7

If we use python version >= 3.7, we may face some problems. 
I tried python 3.8 on Ubuntu 20.04, and something went wrong.

### When running installation instruction

We may face some errors about `numpy`, what we are supposed to do is reinstalling numpy.

```bash
pip3 uninstall numpy
pip3 install numpy
```

### When running precise-convert

If there are some errors occurs when running `precise-convert` about loading .net file.
Run the instructions as follows.

```bash
pip install 'h6py==2.10.0' --force-reinstall
```

