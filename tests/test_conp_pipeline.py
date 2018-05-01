#!/usr/bin/env python

from unittest import TestCase
import shutil
import os
import subprocess


class TestImport(TestCase):

    def run_command_test(self, command):
        process = subprocess.Popen(command, shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        print(process.stdout.read())
        print(process.stderr.read())
        process.communicate()
        self.assertFalse(process.returncode)

    def search(self, key, file_name):
        command = ("datalad -C test_dataset -c datalad.search.index-e"
                   "grep-documenttype=all search -f {} |"
                   " grep {}".format(key, file_name))
        self.run_command_test(command)


    def test_conp_pipeline(self):
        # Test dataset creation with DataLad
        command = "chmod 777 test_dataset/.git -R"
        os.system(command)
        shutil.rmtree("test_dataset", ignore_errors=True)

        command = ("datalad create test_dataset")
        self.run_command_test(command)

        # Test pipeline execution
        command = ("conp-pipeline run test_dataset tests/fsl_bet.json "
                   "tests/invocation.json")
        self.run_command_test(command)

        self.assertTrue(os.path.exists('test_dataset/execution/'
                                       'sub-01_T1w_brain.nii.gz'))

        # Test that some metadata was added
        self.search('boutiques', 'fsl_bet')
        self.search('result-file', 'sub-01_T1w_brain.nii.gz')
        self.search('invocation', 'invocation.json')
