[![Build Status](https://travis-ci.org/CONP-PCNO/conp-pipeline.svg?branch=master)](https://travis-ci.org/CONP-PCNO/conp-pipeline)
[![Coverage Status](https://coveralls.io/repos/github/CONP-PCNO/conp-pipeline/badge.svg?branch=master)](https://coveralls.io/github/CONP-PCNO/conp-pipeline?branch=master)

# conp-pipeline

`conp-pipeline` is a tool that runs pipelines and commit their inputs and 
results to aDataLad dataset.

Syntax: `conp-pipeline <dataset> <descriptor> <invocation>` 

Example: the following commands create a test DataLad dataset, 
run FSL bet on a test image and commit the results to the dataset.
```
datalad create test-dataset
conp-pipeline test-dataset tests/fsl_bet.json tests/invocation.json
```
