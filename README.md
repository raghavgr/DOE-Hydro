# DOE-Hydro

## Dependencies

 - Python 3.6.5
 - Anaconda: https://docs.anaconda.com/anaconda/install/mac-os, link for setting up Anaconda in macOS

 
## Conda virtual environment

> "Virtual environmets make it easy to cleanly separate different projects and avoid problems with different dependencies and version requiremetns across components."

### Using existing environment

- Go to your working directory and clone this repository
- Use the existing `environment.yml` to create your environment
	- `conda env create -f environment.yml` 
    - This command will install all the dependencies required for your project

### Setting up virtual environment from scratch 


 - `conda create -n test-env python=3.6.5 anaconda`  replace `test-env` with your own name
 - move to your working directory
 - run `source activate test-env` to start the environment
 - use `conda list --export` to list the libraries installed so far in your environment. Similar to `pip freeze`
	 - use `conda list --export > requirements.txt ` to save the packages listed. 
	 - use `conda export env -n envName > envName.yml` to share your Conda environment with someone else. Choose your own `envName`. 	
 - To install packages in this environment, use the following command:
 		`conda install -n test-env xarray dask netCDF4 bottleneck`