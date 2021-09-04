from azureml.core import Workspace

ws = Workspace.create(name='myworkspace',
               subscription_id='c169cb72-e23c-46d5-a6c3-2aa14f2f8cef',
               resource_group='localResourceGroup',
               create_resource_group=True,
               location='centralindia'
               )
