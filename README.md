# PySlurmJob

PySlurmJob is a dirty small script that can be used to run commands within a slurm job and to access job information once the job has finished. 

## Installation

As PySlurmJob is really tiny, you can just copy it into your script or clone it directly in your `modules` directory. It only requires `time` and `subprocess`.

## Usage

This script can be used very simply. 

    import pyslurmjob

### Create a Slurm job with specific commands

It's possible to launch commands into a Slurm job thanks to the function `new_job`, which return the job output and its ID **ONLY** when it's finished.

    output, id = pyslurm.new_job(["echo Sorry to the cluster administrator for this questionable allocation", "echo it is the last time, I promise"], args: slurmArgs)

where `slurmArgs` is a dictionnary containing the [desired Slurm Batch options](https://slurm.schedmd.com/sbatch.html#SECTION_OPTIONS).

    slurmArgs = {"--time": "12:00:00", 
				 "-J": "UselessTask", 
				 "--mem": "4G",
				 "--ntasks": 1,
				 "--cpus-per-task": 2,
				 "--nodes":1}

Note that you can also precise the name of a conda environment with the `new_job` argument  `environment`, which can be useful if you want to launch an environment-specific command.  

### Get information about finished job (Seff & Sacct)

PySlurmJob also provides two functions to get information concerning a finished job, returning the output of the Slurm [seff](https://docs.hpc.shef.ac.uk/en/latest/referenceinfo/scheduler/SLURM/Common-commands/seff.html#gsc.tab=0) and [sacct](https://slurm.schedmd.com/sacct.html) commands.

#### Seff

The `seff` function return a dictionnary containing the seff data :

    pyslurm.seff(id)

The dictionary is basically build like that :

    {'Job ID': '0000001', 
    'Cluster': 'clusterName', 
    'User/Group': 'user/root', 
    'State': 'COMPLETED (exit code 0)', 
    'Nodes': '1', 
    'Cores per node': '2', 
    'CPU Utilized': '00:00:00', 
    'CPU Efficiency': '0.00% of 00:00:00 core-walltime', 
    'Job Wall-clock time': '00:00:00', 
    'Memory Utilized': '132.00 KB', 
    'Memory Efficiency': '0.00% of 4.00 GB'}


#### Sacct

The `sacct` function return a list of ditionnary containing, for each step of the job, all the [job accouting fields](https://slurm.schedmd.com/sacct.html#SECTION_Job-Accounting-Fields) and the associated values. 

    pyslurm.sacct(id)

For example, the above example `new_job` runs two commands with default IDs of 0 and 1. It is then possible to access to the field *Average Virtual Memory size* of the previously launched command `echo it is the last time, I promise` by typing the following code :

`pyslurm.sacct(id)["1"]["AveVMSize"]`

## More complex needs

Although this script can be used easily and integrated directly into your scripts, it's still pretty primitive. If your needs are more consistent, take a look at the [PySlurm](https://github.com/PySlurm/pyslurm) and [SlurmPy](https://github.com/brentp/slurmpy) repositories.
