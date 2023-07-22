# Smoking_Cessation_Training
Training Model - Smoking Cessation

This is the first training model the ASDM framework https://github.com/wzh1895/ASDM to get people used to coding SD models in Python using ASDM. 

### Model Purpose

The model imagines a health system where a decision has to be made about re-investment rates from a smoking cessation program:

![Smoking_Cessation_Model](https://github.com/ReallyUsefulModels/Smoking_Cessation_Training/blob/main/Smoking_Cessation_Model.PNG)

### Model Demo

You can start playing with the model here: https://smokingcessation.streamlit.app/

### Notebooks

To help new users get used to python and SD notebooks are best because they allow users to iterate line-by-line as they get their head around what the code is doing. 

In this tutorial we have used a juptyer notebook or .ipynb file to guide new users through the process step by step. 

### Installing python and generally getting things working

If you are totally new to all of this please check out: https://mattstammers.github.io/hdruk_avoidable_admissions_collaboration_docs/how_to_guides/new_to_python/ where we will take you through how to set everything up from scratch. If you need help from your hospital to install python we recommend talking to the IT team and perhaps even directing them to this website. Particularly hospital BI teams are likely to be interested in it!

### Quickstart

If you are ready to go straight away then from the point of having git and the python packaging tool 'pip' installed you can be up and running in only 6 steps as listed below running each in series.

```bat
1. git clone https://github.com/ReallyUsefulModels/Smoking_Cessation_Training.git
2. cd Smoking_Cessation_Training
3. pip install pipenv
4. pipenv install
5. pipenv shell
6. juptyer-lab
```

It doesn't matter where you run the above set of instructions. As long as you have the right permissions on the machine it should launch a browser from the kernel and you will be into the notebook. If you would rather use VS-code instead you just need to select the correct kernel and it should work.

We have made sure that ASDM works in any python distribution above 3.9 in both Windows and Linux. However, if you experience a new problem please let us know!

Now you should be able to follow the notebook.

### Streamlit App

The source code for the Smoking Cessation Streamlit App is included. We have deliberately kept this as simple as possible so others can use it as a boilerplate for their own apps.