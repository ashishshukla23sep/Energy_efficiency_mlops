## Building Heating and cooling load capacity

1. [Github Account](https://github.com/ashishshukla23sep/Energy_efficiency_mlops)
2. [Heroku Account](https://buildingloadestimator.herokuapp.com/)
3. [Dataset Link](https://archive.ics.uci.edu/ml/datasets/energy+efficiency)


## Dataset information

```
We perform energy analysis using 12 different building shapes simulated in Ecotect. The buildings differ with respect to the glazing area, the glazing area distribution, and the orientation, amongst other parameters. We simulate various settings as functions of the afore-mentioned characteristics to obtain 768 building shapes. The dataset comprises 768 samples and 8 features, aiming to predict two real valued responses. It can also be used as a multi-class classification problem if the response is rounded to the nearest integer.


```

## Problem Statement

```
The effect of eight input variables (relative compactness, surface area, wall area, roof
area, overall height, orientation, glazing area, glazing area distribution) on two output
variables, namely heating load (HL) and cooling load (CL), of residential buildings is
investigated using a statistical machine learning framework. We have to use a number
of classical and non-parametric statistical analytic tools to carefully analyse the strength
of each input variable's correlation with each of the output variables in order to discover
the most strongly associated input variables. We need to estimate HL and CL, we can
compare a traditional linear regression approach to a sophisticated state-of-the-art
nonlinear non-parametric method, random forests.

```
## Observations
```
1. we observed HL and CL are highly correlated 
2. Roof Area is negatively correlated with HL AND CL
3. Since HL AND CL are possively correlated we will first predict y1 and then y1 will be used as input to predict y2
4 .We will have 2 models ,one for predicting HL and other for Predicting CL
```
## Refer flowchart.svg to understand the model flow

```
conda create -p venv python==3.7 -y
```
```
conda activate venv
```
```
pip install -r requirements.txt
```

