# -*- coding: utf-8 -*-
import subprocess as sp
import time

def new_job(commands: list, args: dict, environment: str = None):
    """
    This function ask for the creation of a slurm job with the given commands
    and the given slurm arguments. It can also take a conda environment to run
    the commands in it. It return the job output and its ID, only when it's finished.
    """
    # Write the sbatch script
    with open("tmpjob.sh", "w") as file:
        file.write('#!/bin/bash\n')
        for arg, value in args.items():
            file.write(f'\n#SBATCH {arg}={value}')
        if environment is not None:
            file.write(f'\neval "$(conda shell.bash hook)"\nconda activate {environment}')
        for command in commands:
            file.write(f'\nsrun {command}')

    # Launch the job and save the ID
    job = sp.run([f'sbatch tmpjob.sh'], shell=True, capture_output=True, encoding="UTF-8").stdout
    jobId = job.split("job ")[1].replace("\n", "")
    while True:
        time.sleep(3)
        if "COMPLETED" in sp.run([f'seff {jobId}'], shell=True, capture_output=True, encoding="UTF-8").stdout:
            break
        if "FAILED" in sp.run([f'seff {jobId}'], shell=True, capture_output=True, encoding="UTF-8").stdout:
            print(f"Warning : job {jobId} failed.")
            break

    # Get the standard output of the job
    with open(f"slurm-{jobId}.out", "r") as stdoutFile:
        stdout = stdoutFile.read()

    # Clean the directory
    sp.run([f'rm tmpjob.sh && rm slurm-{jobId}.out'], shell=True)

    return stdout, int(jobId)

def seff(jobId : int):
    """
    Return a dictionary containing the information given by the slurm command seff <job id>
    """
    seff =  sp.run([f'seff {jobId}'], shell=True, capture_output=True, encoding="UTF-8").stdout
    dict = {}
    for line in seff.split("\n") :
        if ":" in line :
            stat = line.split(": ")
            dict[stat[0]] = stat[1]
    return dict

def sacct(jobId : int, stepsIds : list = None) :
    """
    Return a dictionnary {stepID : subdictionnary...} where the subdictionnaries contain for each step the information given by the slurm command sacct <job id>
    """
    sacct =  sp.run([f'sacct -o ALL --jobs={jobId} -p'], shell=True, capture_output=True, encoding="UTF-8").stdout
    steps = []
    for l in range(2, len(sacct.split("\n"))-1) :
        step = {}
        for f in range(len(sacct.split("\n")[0].split("|"))) :
            step[sacct.split("\n")[0].split("|")[f]] = sacct.split("\n")[l].split("|")[f]
        steps.append(step)

    dict = {}
    for step in steps :
        dict[step["JobID"].replace(f"{jobId}.", "")] = step

    return dict
