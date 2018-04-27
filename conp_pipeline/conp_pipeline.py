#!/usr/bin/env python

import argparse
import sys
import os
import os.path as op
import shutil
import json
from tempfile import mkdtemp
from boutiques import evaluate as bosh_evaluate
from boutiques import validate as bosh_validate
from boutiques import invocation as bosh_invocation
from datalad.distribution.dataset import Dataset
from datalad.distribution.add import Add


class CONPPipelineError(Exception):
    pass


def info(message, verbose):
    if verbose:
        print("[ INFO ] {}".format(message))


def error(message):
    print("[ ERROR ] {}".format(message))
    sys.exit(1)


def is_in_dir(dir_name, file_name):
    return op.abspath(file_name).startswith(op.abspath(dir_name))


def add_to_execution(file_name, execution_dir, to_git):
    file_in_execution_dir = op.join(op.abspath(execution_dir),
                                    op.basename(file_name))
    if op.abspath(file_name) != file_in_execution_dir:
        shutil.copy(file_name, file_in_execution_dir)
    Add.__call__(file_in_execution_dir, to_git=to_git)
    return file_in_execution_dir


def to_git_guess(file_name):
    return file_name.endswith('.json') or file_name.endswith('.txt')


def main(args=None):

    parser = argparse.ArgumentParser(description="CONP pipeline driver")
    parser.add_argument("command", action="store",
                        help="command to be executed.",
                        choices=["run"])
    parser.add_argument("dataset_path", action="store",
                        help="path to a datalad dataset.")
    parser.add_argument("descriptor_file", action="store",
                        help="the Boutiques descriptor.")
    parser.add_argument("invocation_file", action="store",
                        help="input JSON complying to invocation.")
    parser.add_argument("--slurm", action="store_true",
                        help="run on SLURM cluster.")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="increase verbosity.")
    results = parser.parse_args(args)

    # Parse arguments
    dataset_path = results.dataset_path
    descriptor_file = results.descriptor_file
    invocation_file = results.invocation_file
    slurm = results.slurm
    verbose = results.verbose

    try:
        # Check if dataset is a DataLad dataset
        dataset = Dataset(dataset_path)
        if not dataset.is_installed():
            raise CONPPipelineError("{} is not an installed DataLad"
                                    " dataset".format(dataset_path))

        # Validate descriptor and invocation files
        bosh_validate(descriptor_file)
        bosh_invocation(descriptor_file, "-i", invocation_file)

        # Create execution directory
        execution_dir = op.abspath(op.join(dataset_path, 'execution'))
        if op.exists(execution_dir):
            execution_dir = mkdtemp(dir=dataset_path, prefix='execution-')
        else:
            os.mkdir(execution_dir)
        info("Execution dir: {}".format(execution_dir), verbose)

        # Add descriptor to execution dir
        descriptor_file = add_to_execution(descriptor_file,
                                           execution_dir,
                                           to_git=True)

        # Add input data files to dataset and update invocation accordingly
        # TODO: check if it works with file lists
        invocation = json.loads(open(invocation_file).read())
        bosh_inputs = bosh_evaluate(descriptor_file,
                                    invocation_file,
                                    "inputs/type=File")

        info("Copying input files to dataset", verbose)
        for input_id in bosh_inputs.keys():
            input_file = bosh_inputs[input_id]
            if input_file is None:
                continue
            if not op.isabs(input_file):
                # Assume that path is relative to invocation file
                invocation_dir = op.dirname(op.abspath(invocation_file))
                input_file = op.join(invocation_dir, input_file)
            # Add file to the dataset and update invocation accordingly
            file_path_in_dataset = add_to_execution(input_file,
                                                    execution_dir,
                                                    to_git=False)
            bosh_inputs[input_id] = file_path_in_dataset
            invocation[input_id] = file_path_in_dataset

        # Write updated invocation to dataset
        invocation_file = op.join(execution_dir, op.basename(invocation_file))
        with open(invocation_file, 'w') as fhandle:
            fhandle.write(json.dumps(invocation, indent=4, sort_keys=True))

        # Run the execution in Clowdr
        info("Executing invocation with Clowdr", verbose)
        if slurm:
            from clowdr.driver import cluster as clowdr_exec
        else:
            from clowdr.driver import local as clowdr_exec
        cwd = os.getcwd()
        task_dir = clowdr_exec(descriptor_file,
                               invocation_file,
                               execution_dir,
                               execution_dir,
                               volumes=[op.abspath(dataset_path) +
                                        ":" + op.abspath(dataset_path)],
                               user=True)
        os.chdir(cwd)

        # Copy Clowdr files back
        info("Copying output files to dataset", verbose)
        ignored_files = ['invocation.json', task_dir]
        for file_name in os.listdir(task_dir):
            file_name = op.join(task_dir, file_name)
            if ((not op.basename(file_name).startswith("clowtask")) and
               (file_name not in ignored_files)):
                    dest_file = op.abspath(op.join(execution_dir,
                                           op.basename(file_name)))
                    shutil.move(file_name, dest_file)
                    Add.__call__(dest_file, to_git=to_git_guess(dest_file))
        # Cleanup Clowdr dir
        shutil.rmtree(op.dirname(task_dir))

        info("Done!", verbose)
# Add metadadta to descriptor so that others can find it (how?)

# Copy output files to dataset if not there already.
    except CONPPipelineError as e:
        error(e)


if __name__ == '__main__':
    main()
