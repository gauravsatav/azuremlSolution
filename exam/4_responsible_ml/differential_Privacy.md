# Differential Privacy Concept
Differential privacy is the gold-standard definition of privacy. Systems that adhere to this definition of privacy provide strong assurances against a wide range of data reconstruction and reidentification attacks, including attacks by adversaries who possess auxiliary information.

When someone queries the database for the info regarding the statistics, in a differentially private system, this query goes through a dp module which fetches the data and before returning the query, it adds noise to the returned data


* To prepare a differentially private release you need to choose:
    * a data source
    * a statistic [sn.dp_mean, sn.dp_histogram, sn.dp_covariance, sn.dp_variance, sn.dp_count, sn.dp_ sum, sn.dp_quantile]
    * some privacy parameters, indicating the level of privacy protection.

* In differentially private systems, data is shared through requests called queries.
* When a user submits a query for data, operations known as privacy mechanisms add noise to the requested data.
* Privacy mechanisms return an approximation of the data instead of the raw data.
* This privacy-preserving result appears in a report.
* Reports consist of two parts, the actual data computed and a description of how the data was created.

# Metric
* 0 < epsilon < 1. This should be the range if we are maintain plausible deniability.
* epsilon close to 0 means more private (more noise is added)
* epsilon > 1 come with risk of exposure

# Limit Query Metric
* Privacy budgets prevent data from being recreated through multiple queries.
* Privacy budgets are allocated an epsilon amount, typically between 1 and 3 to limit the risk of reidentification. 
* As reports are generated, privacy budgets keep track of the epsilon value of individual reports as well as the aggregate for all reports. 
* After a privacy budget is spent or depleted, users can no longer access data.
* [How to spread budget](https://docs.microsoft.com/en-gb/azure/machine-learning/how-to-differential-privacy#perform-data-analysis)

# Reliability on data
* A higher level of added noise or privacy translates to data that has a lower epsilon, accuracy, and reliability.

# How to integrate with Datasets?
Don't know

# Libraries
https://docs.microsoft.com/en-gb/azure/machine-learning/how-to-differential-privacy

## SmartNoise Core

## SmartNoise SDK

## Example
```python
with sn.Analysis() as analysis:
    # load data
    data = sn.Dataset(path = data_path, column_names = var_names)

    # get mean of age
    age_mean = sn.dp_mean(data = sn.cast(data['age'], type="FLOAT"),
                          privacy_usage = {'epsilon': .65},
                          data_lower = 0.,
                          data_upper = 100.,
                          data_n = 1000
                         )
    # get variance of age
    age_var = sn.dp_variance(data = sn.cast(data['age'], type="FLOAT"),
                             privacy_usage = {'epsilon': .35},
                             data_lower = 0.,
                             data_upper = 100.,
                             data_n = 1000
                            )
analysis.release()
```