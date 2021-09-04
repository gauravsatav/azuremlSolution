Manage data in an Azure Machine Learning workspace
 select Azure storage resources
 register and maintain datastores
 create and manage datasets


# Labelling
Configure incremental refresh
The check for new data stops when the project contains the maximum 500,000 files.

Export the labels
* Text labels can be exported as: AvCSV file
* Image labels can be exported as: COCO format

Read Datasets as 
* Pandas dataframe : Dataset.get_by_name(workspace, 'animal_labels').to_pandas_dataframe()
* Torchvision datasets : Dataset.get_by_name(workspace, 'animal_labels').to_torchvision()

# Get and prepare data
https://docs.microsoft.com/en-gb/azure/machine-learning/how-to-data-ingest-adf#compare-azure-data-factory-data-ingestion-pipelines

* MLOPS for data ingestion pipeline
    * Azure Data Factory: Reads the raw data and orchestrates data preparation.
    * Azure Databricks: Runs a Python notebook that transforms the data.
    * Azure Pipelines: Automates a continuous integration and development process.
    * There are two ways you can import data into the designer:
        * Azure Machine Learning datasets - Register datasets
        * Import Data module - Use the Import Data module

* Data Factory (SPARK BASED DATA PREPARATION) + 
    * Azure Funtions
    * custom Components
    * Databricks

    * To consume
        * The Data Factory pipeline saves the prepared data to your cloud storage (such as Azure Blob or Azure Datalake).
            * Invoking an Azure Machine Learning pipeline from your Data Factory pipeline.
            * OR
            * Creating an Azure Machine Learning datastore and Azure Machine Learning dataset for use at a later time.
        * `Datastore.register_azure_data_lake_gen2({ws,rg,stogare accunt})`
        * Generally while registering blob storage we use `Datastore.register_azure_blob_container({ws,rg,stogare accunt})`

* Azure Synapse (SPARK BASED DATA EXPLORATION)
    * The Azure Synapse Analytics integration with Azure Machine Learning (preview) allows you to attach an Apache Spark pool backed by Azure Synapse for interactive data exploration and preparation
    
    * If you are ready to automate and productionize your data wrangling tasks, you can submit an experiment run to an attached Synapse Spark pool with the ScriptRunConfig object.


# Access Data
To only way to access data in AZ ML workspace is to register your storage solution via `Datastore`.
* Datastore.register_azure_blob_container()

* Datastore.register_azure_file_share()

* Datastore.register_azure_data_lake_gen2()

* If you're using unsupported data solutions with Azure ML then use Azure Data Factory to transform then into supported ones

# Consume Datasets

* Create Tabular/File Datasets using many methods
* ```python
    web_path ='https://dprepdata.blob.core.windows.net/demo/Titanic.csv'
    titanic_ds = Dataset.Tabular.from_delimited_files(path=web_path)
  ```

* Only Datasets can be mounted to computes, otherwise to make the data availabe on the compute target of your choice you'll have to download it

* Datasets can be created using any of the above storage solutions

* Mounting is supported for linux based computes (both azure computes, Linux VM, HD Insight)

* [For unstructured data create `FileDataset` and Mount file to remote compute targets ](https://docs.microsoft.com/en-gb/azure/machine-learning/how-to-train-with-datasets#configure-the-training-run-1)
    * Register a File dataset
    * `input= mnist_ds.as_named_input('input').as_mount()`
    * With `output = OutputFileDatasetConfig(destination={})` object you can set a conf that can be pased to 
    * ```python
        ScriptRunConfig(arguments=[input,output],
                        compute_target = "",
                        environment=""
                        )
        ```
* Mount vs download
    * mounts dataset to the temp directory at mounted_path

    * When you mount a dataset, you attach the files referenced by the dataset to a directory (mount point) and make it available on the compute target. Mounting is supported for Linux-based computes, including Azure Machine Learning Compute, virtual machines, and HDInsight.

    * When you download a dataset, all the files referenced by the dataset will be downloaded to the compute target. Downloading is supported for all compute types.

# Data drifts

* Dataset monitors depend on the following Azure services.
    * Datasets
    * Azureml pipeline and compute	
    * Application insights
    * Azure blob storage

* Create baseline Dataset : usually the training dataset for a model.

* Data drift magnitude	A percentage of drift between the baseline and target dataset over time. Ranging from 0 to 100, 0 indicates identical datasets and 100 indicates the Azure Machine Learning data drift model can completely tell the two datasets apart. Noise in the precise percentage measured is expected due to machine learning techniques being used to generate this magnitude.
    
* Target dataset - usually model input data - is compared over time to your baseline dataset. This comparison means that your target dataset must have a timestamp column specified.
    * https://docs.microsoft.com/en-gb/azure/machine-learning/how-to-monitor-datasets?tabs=python#create-dataset-monitor
    
    * OPTIONAL : define partition format (if the files are stored under subfolders that have year-month-date format)
    
    * Create a Tabular Dataset. If the partition format is use then pass it here
    
    * Set a timestamp column for this Tabular Dataset (if there was subfolder structure mentioned above then pass the name of the column that has date time)
    
    * Register the Dataset on workspace
    
    * Create a `DatadriftMonitor`
    
    * Metrics: Metrics can be queried in the Azure Application Insights
        * Wasserstein distance	: Minimum amount of work to transform baseline distribution into the target distribution.
    
    *   ```python
        features = ['Pregnancies', 'Age', 'BMI']
        alertConf = AlertConfiguration(['gausatav@in.ibm.com'])
        monitor = DataDriftDetector.create_from_datasets(ws, 'mslearn-diabates-drift', 
                                                            baseline_data_set,target_data_set,
                                                            compute_target=cluster_name,
                                                            frequency='Week',
                                                            feature_list=features,
                                                            drift_threshold=.3,
                                                            latency=24,  # # SLA in hours for target data to arrive in the dataset
                                                            alert_config=alertConf)
        # ============================== (5). BACKFILL DATA DRIFT MONITOR ==============================
        backfillDurationWeeks = 6

        startTime = dt.datetime.now() - dt.timedelta(weeks=backfillDurationWeeks)
        stopTime = dt.datetime.now()

        backfill = monitor.backfill(startTime, stopTime)
        # ============================== (6). ANALYZE DATA DRIFT MONITOR ==============================
        drift_metrics = backfill.get_metrics()
        for metric in drift_metrics:
            print(metric, drift_metrics[metric])
        ```



# Differential Privacy