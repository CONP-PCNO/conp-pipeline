#!/usr/bin/env python

from unittest import TestCase
import shutil
import os
import subprocess


class TestImport(TestCase):

    def test_conp_pipeline(self):
        command = "chmod 777 test_dataset/.git -R"
        os.system(command)
        shutil.rmtree("test_dataset", ignore_errors=True)
        command = ("datalad create test_dataset")
        process = subprocess.Popen(command, shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        process.communicate()
        print(process.stdout)
        print(process.stderr)
        self.assertFalse(process.returncode)

        command = ("conp-pipeline test_dataset tests/fsl_bet.json "
                   "tests/invocation.json")
        process = subprocess.Popen(command, shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        process.communicate()
        print(process.stdout)
        print(process.stderr)
        self.assertFalse(process.returncode)
