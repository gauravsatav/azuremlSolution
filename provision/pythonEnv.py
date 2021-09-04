from azureml.core import Environment
from azureml.core.conda_dependencies import CondaDependencies
from azureml.core.environment import DEFAULT_CPU_IMAGE


def checkCreateRegisterEnvironment(currentWorkspace,
                        environmentName,
                        listOfCondaPackages,
                        listOfPipPackages,
                        registerNewEnvironment = True,
                        batchEnv=False
                        ):

    ws = currentWorkspace
    
    if environmentName not in Environment.list(workspace=ws):
        packages = CondaDependencies.create(conda_packages=listOfCondaPackages,pip_packages=listOfPipPackages)                                                                       # Returns list of registered environments as list.                                                                                                                      # All curated environments have names that begin AzureML- (you can't use this prefix for your own environments).        #            # ------ CREATE NEW ENVIRONMENT------
        
        provisionedEnvironment = Environment(name = environmentName)                                                             # Create a Python environment for the experiment
        
        provisionedEnvironment.python.user_managed_dependencies = False                                                        # Let Azure ML manage dependencies.
        provisionedEnvironment.docker.enabled = True                                                                           # Use a docker container.        
        provisionedEnvironment.python.conda_dependencies = packages                                                            # Ensure the required packages are installed (we need scikit-learn, Azure ML defaults, and Azure ML dataprep)
        
        if batchEnv:
            provisionedEnvironment.docker.base_image = DEFAULT_CPU_IMAGE
        
        addOnText=''        
        if registerNewEnvironment:
            provisionedEnvironment.register(workspace=ws)
            provisionedEnvironment = Environment.get(ws, environmentName)
            addOnText = 'and registered'

        print(f"\n Created {addOnText} a new python environment with name : {provisionedEnvironment.name}")

        return provisionedEnvironment
    
    else:
        print(f"\n Environment with name : {environmentName} already exists. \n Use it.")
        provisionedEnvironment = Environment.get(workspace=ws,name=environmentName)
        
        return provisionedEnvironment