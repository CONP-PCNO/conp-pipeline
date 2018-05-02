[![PyPI](https://img.shields.io/pypi/v/conp-pipeline.svg)](https://pypi.python.org/pypi/conp-pipeline)
[![PyPI](https://img.shields.io/pypi/pyversions/conp-pipeline.svg)](https://pypi.python.org/pypi/conp-pipeline)
[![Build Status](https://travis-ci.org/CONP-PCNO/conp-pipeline.svg?branch=master)](https://travis-ci.org/CONP-PCNO/conp-pipeline)
[![Coverage Status](https://coveralls.io/repos/github/CONP-PCNO/conp-pipeline/badge.svg?branch=master)](https://coveralls.io/github/CONP-PCNO/conp-pipeline?branch=master)

# conp-pipeline

`conp-pipeline` is a tool that runs pipelines and commits their inputs and 
results to a DataLad dataset.

## Installation

* Install [`git-annex`](http://git-annex.branchable.com/install)
* `pip install git+https://github.com/datalad/datalad.git`
* `pip install conp-pipeline`

## Syntax

`conp-pipeline run <dataset> <descriptor> <invocation>` 

## Example

The following commands create a test DataLad dataset, 
run FSL bet on a test image and commit the results to the dataset.
```
datalad create test-dataset
conp-pipeline run test-dataset tests/fsl_bet.json tests/invocation.json
```

## Metadata

`conp-pipeline run` adds the following metadata to the pipeline inputs and 
outputs:
* `<descriptor>`:
   - `conp-pipeline-role`: `pipeline-description`
   - various fields extracted from the Boutiques descriptor
including `name`, `description`, `tags`, `container-type`, etc. 
* `<invocation>`: `conp-pipeline-role`: `invocation-description`.
* Pipeline input files: `conp-pipeline-role`: `input-file`.
* Pipeline results: `conp-pipeline-role`: `result-file`.
