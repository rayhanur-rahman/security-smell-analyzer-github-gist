# Share but Beware: Security Smells in Python Gists
This work has been published in ICSME 2019 hosted at Cleveland, Ohio, USA. This work finds out security smell in Python Gists available in Github. You can find the draft version of the paper in `others/ICSME19_paper_202.pdf`.

You need python 3.7 and some other pip packages. 

In `./gist-src`, you will find the python gists we have used as dataset.
Use Bandit tools from https://github.com/PyCQA/bandit on this dataset to generate security smells listed in Bandit.
In `./src/smellDetector.py`, our own custom static analyzer will find out a few more security smells.
in `./src/author2.csv`, author metrics from the gists are collected.
In `./src/getStatistics.py`, you will get the final statistics which is already available in `./RQs.txt`.

Feel free to ask anything...!!!
