# Overview
Azure Databricks is an Apache Spark-based environment in the Azure cloud. It can be used as a compute target with an Azure Machine Learning pipeline.

Azure Databricks provides data science and engineering teams with a single platform for Big Data processing and Machine Learning.

Azure Databricks is a fully-managed version of the open-source Apache Spark analytics and data processing engine. Azure Databricks is an enterprise-grade and secure cloud-based big data and machine learning platform.

Set up an Azure Databricks workspace
 create an Azure Databricks workspace
 create an Azure Databricks cluster
 create and run notebooks in Azure Databricks
 link and Azure Databricks workspace to an Azure Machine Learning workspace

## Attach databricks Compute
https://docs.microsoft.com/en-gb/azure/machine-learning/how-to-attach-compute-targets#databricks

## Architecture
* When you create an Azure Databricks service, a "Databricks appliance" is deployed as an Azure resource in your subscription. 
* two aspects of the Databricks architecture: the Azure Databricks service and Apache Spark clusters.
* At the time of cluster creation, you specify the types and sizes of the virtual machines (VMs) to use for both the Driver and Worker nodes, but Azure Databricks manages all other aspects of the cluster.
* ADB Service orchestrates clusters
* In cluster there are 2 types of nodes:
    * Driver Node : the master node (notebook node) controls
    * worker nodes

* Understand the architecture of spark job
    * Spark is a Distributed computing environment. The unit of distribution is a Spark Cluster. Every Cluster has a Driver and one or more executors.
    * Driver
        * Executors run (jobs)
            * Slots run (task) 
    * [We parallelize at two levels]https://docs.microsoft.com/en-us/learn/modules/spark-architecture-fundamentals/3-understand-architecture-of-spark-job 
        * The first level of parallelization is the Executor - a Java virtual machine running on a node, typically, one instance per node.
        * The second level of parallelization is the Slot - the number of which is determined by the number of cores and CPUs of each node.
        * Consequently, the Driver is assigning a Partition of data to each task - in this way each Task knows which piece of data it is to process.

## Read and write data 

* Read data with and without schema for following file formats:
    * List files in fs
        * `%fs ls /my-file-path`
    * JSON : infer the data types and column names when you read a JSON file
    `spark.read.option("inferSchema", "true").json(jsonFile)`
    
    * PARQUET
    
    * CSV

## Working with Dataframes
*  Use the count() method to count rows in a DataFrame
*  Use the display() function to display a DataFrame in the Notebook
*  Cache a DataFrame for quicker operations if the data is needed a second time
*  Use the limit function to display a small set of rows from a larger DataFrame
*  Use select() to select a subset of columns from a DataFrame
*  Use distinct() and dropDuplicates to remove duplicate data
*  Use drop() to remove columns from a DataFrame
* Learn the transformations...
    * limit(..)
    * select(..)
    * drop(..)
    * distinct()
    * dropDuplicates(..)
* show(..)
* display(..)

*  create a temporary view
`createOrReplaceTempView()`

* create a DataFrame object
`Introduce a variable name and equate it to something like myDataFrameDF =`


* cache data into the memory of the local executor for instant access
`.cache()`

* Python syntax for defining a DataFrame in Spark from an existing Parquet file in DBFS
`IPGeocodeDF = spark.read.parquet("dbfs:/mnt/training/ip-geocode.parquet")`

## User defined function
 * What is the correct syntax to register the UDF, f, as my_function in SQL namespace?
`spark.udf.register("my_function", f)`

 * 2. What is the correct syntax for specifying the return type for an UDF?
`my_udf = udf(f, "long")`

 * 3. What is one of the drawbacks of UDFs?
`The function has to be serialized and sent out to the executors.`


## [Delta Lake](https://docs.microsoft.com/en-us/learn/modules/build-query-delta-lake/2-describe-open-source)

* It stores your data as Apache Parquet files in DBFS and maintains a transaction log that efficiently tracks changes to the table.
* Delta Lake is a transactional storage layer designed specifically to work with Apache Spark and Databricks File System (DBFS). At the core of Delta Lake is an optimized Spark table.

*    ```python
    CREATE TABLE ...
    USING delta
    ...

    dataframe
        .write
        .format("delta")
        .save("/data")
    ```
* ```python
    CONVERT TO DELTA parquet.`path/to/table` [NO STATISTICS]
    [PARTITIONED BY (col_name1 col_type1, col_name2 col_type2, ...)]
    ```

1. What is the Databricks Delta command to display metadata?
DESCRIBE DETAIL tableName


2. How do you perform UPSERT in a Delta dataset?
Use MERGE INTO my-table USING data-to-upsert

3. What optimization does the following command perform: OPTIMIZE Students ZORDER BY Grade?
Ensures that all data backing, for example, Grade=8 is colocated, then rewrites the sorted data into new Parquet files

4. What size does OPTIMIZE compact small files to?
Around 1 GB


## Perform ML Tasks

*  Define machine learning
*  Differentiate supervised and unsupervised tasks
*  Identify regression and classification tasks
*  Train a model, interpret the results, and create predictions
*  Identify the main objectives of exploratory analysis
*  Calculate statistical moments to determine the center and spread of data
*  Create plots of data including histograms and scatterplots
*  Calculate correlations between variables
*  Explore more advanced plots to visualize the relation between variables
*  Define the data analytics development cycle
*  Motivate and perform a split between training and test data
*  Train a baseline model
*  Evaluate a baseline model's performance and improve it

1. What method is used in Python cells to display the results as a formatted table or chart visualization?
* display(df)


2. What method is used to calculate the correlation between two columns in a dataframe (df)?
* df.stat.corr('col1', 'col2')


3. Which of these best describes the purpose of training data?
* A subset of the data used to "teach" the algorithm. This is the data that the algorithm will learn from.


4. Mean Squared Error (MSE) is a common evaluation metric in regression tasks. Select the option that apply for MSE?
* Lower the MSE, the better the model is performing.


## MLFLOW
1. What is the correct method to log model performance metrics, _rmse, in MLflow?
* mlflow.log_metric("rmse", _rmse)

2. What is the typical usage for mlflow.log_artifact method?
* Log file or directory contents

## Describe model selection and hyperparameter tuning
1. What is the likely cause when a supervised model makes predictions perfectly against all the training data, but fails against new data?
* Overfitting

2. Which of the following statements best describes how the k-fold cross-validation splits the training data into the various folds?
* In k-fold cross-validation, each observation from the original training dataset has a chance to appear in both the training subset and the validation subset.


3. Which of the following is always true when using k-fold cross-validation?
* In k-fold cross-validation, the best performing fold only identifies the winning pipeline.

## Horovod
1. What is the size, rank, and local rank when using Horovod to train a deep learning model on two servers, each with two GPUs?
* Size = 4, Rank: [0, 1, 2, 3], and Local Rank: [0, 1]
* Size is total number of GPUs, that is 4. Rank is 0 to Size-1, that is [0, 1, 2, 3]. Local Rank is 0 to number of local GPUs - 1, that is [0, 1].


3. In the Horovod training script, what is the primary purpose of hvd.callbacks.BroadcastGlobalVariablesCallback(0) callback?
* To ensure consistent initialization of all workers when training is started with random weights or restored from a checkpoint.
* It is important to start all workers with the same initial state.

