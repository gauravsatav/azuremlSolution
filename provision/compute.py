'''
This module is to provision compute.
'''

from azureml.core.compute import ComputeTarget, AmlCompute
from azureml.core.compute_target import ComputeTargetException


def listComputeTargets(currentWorkspace):
    ws = currentWorkspace
    existingComputeTargets = ws.compute_targets
    
    if len(existingComputeTargets)==0:
        print(f"\n There are no compute targets found within the workspace : {ws.name} ")

    else:
        for compute_name in existingComputeTargets:
            compute = ws.compute_targets[compute_name]
            print(compute.name, ":", compute.type)


def checkCreateComputeCluster(currentWorkspace,
                                myClusterName,
                                myVmSizeConfig = 'STANDARD_DS11_V2',
                                minNodeConfig = 0,
                                maxNodeConfig = 4,
                                vmPriorityConfig = 'dedicated'
                                ):
    ws = currentWorkspace
    try:                                                                                                 # Check for existing compute target.
        provisionedCluster = ComputeTarget(workspace=ws, name=myClusterName)
        print('Found existing cluster, use it.')
        return provisionedCluster
    except ComputeTargetException:                                                                       # If it doesn't already exist, create it
        print(f'\nDid not find compute cluster with name {myClusterName}')                                
        try:
            compute_config = AmlCompute.provisioning_configuration(vm_size=myVmSizeConfig,           # Define compute configuration
                                                                    min_nodes=minNodeConfig,
                                                                    max_nodes=maxNodeConfig,
                                                                    vm_priority=vmPriorityConfig
                                                                )
            provisionedCluster = ComputeTarget.create(ws, myClusterName, compute_config)                    # Create Compute Target in given Workspace with given name and configuration.
            provisionedCluster.wait_for_completion(show_output=True)                                       # Wait for Completion.
            return provisionedCluster
        except Exception as ex:
            print(f'An exception occured:\n{ex}')




