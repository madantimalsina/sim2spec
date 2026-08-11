## Slurm Options

Sources: Slurm Documentation

Here's a guide to (some) of the sbatch flags you've seen in the scripts. If there are any options missing, let me know!

You can also use the following command for reference:

```
sbatch -help
```
Format:
```
#SBATCH <flag>
```
I do want to point out a common mistake when typing/pasting the sbash commands. There is some confusion with the brackets([], <>), hopefully the examples clear the confusion. 

| Option/Flag  | Function | Example |
| ------------- |-------------|-------------|
| -A or --account=account      | specifies the computation project for our job, in our case **m4388** | ``` #SBATCH -A m4388 ``` |
| -C or --constraint=\<list>      | request certain types of nodes (gpu in our case) | ``` #SBATCH -C gpu ``` |
| -J or --job-name=name    | sets job name (like day1_smoke) | ``` #SBATCH -J day1_smoke ``` |
| -n or --ntasks=\<number>   | sets total number of tasks (processes) to run   | ``` #SBATCH --ntasks 1 ``` |
| -t or --time=time    | max walltime limit of the job    | ``` #SBATCH -t 00:10:00 ``` |
| -q or --qos=<qos>    | request quality of service for the job | ``` #SBATCH -q regular ``` |
| -G or --gpus=[type:]\<number>    | total number of GPUs requested | ``` #SBATCH --gpus 1 ``` |
| -c or --cpus-per-task=\<ncpus>    | CPU cores assigned for each task required for the job | ``` #SBATCH --cpus-per-task 8 ``` |
| -o or --output=\<filename_pattern> | path for standard output log | ``` #SBATCH --output=day1_smoke_%j.out ``` |
| -e or --error=\<filename_pattern> | path for standard error log | ``` #SBATCH --error=day1_smoke_%j.err ``` |




