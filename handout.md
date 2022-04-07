<!-- <style>
    .tasks{
        color: #000099
    }
    @media print {
        *,
        *:before,
        *:after {
        background: transparent !important;
        color: #000 !important;
        box-shadow: none !important;
        text-shadow: none !important;
    }

    a,
    a:visited {
        text-decoration: underline;
    }

    a[href]:after {
        content: " (" attr(href) ")";
    }

    abbr[title]:after {
        content: " (" attr(title) ")";
    }

    a[href^="#"]:after,
    a[href^="javascript:"]:after {
        content: "";
    }

    pre,
    blockquote {
        border: 1px solid #999;
        page-break-inside: avoid;
    }

    thead {
        display: table-header-group;
    }

    tr,
    img {
        page-break-inside: avoid;
    }

    img {
        max-width: 100% !important;
    }

    p,
    h2,
    h3 {
        orphans: 3;
        widows: 3;
    }

    h2,
    h3 {
        page-break-after: avoid;
    }
    }

    pre,
    code {
        font-family: Menlo, Monaco, "Courier New", monospace;
    }

    pre {
        padding: .5rem;
        line-height: 1.25;
        overflow-x: scroll;
    }

    a,
    a:visited {
        color: #3498db;
    }

    a:hover,
    a:focus,
    a:active {
        color: #2980b9;
    }

    .modest-no-decoration {
        text-decoration: none;
    }

    html {
        font-size: 12px;
    }

    @media screen and (min-width: 32rem) and (max-width: 48rem) {
    html {
        font-size: 15px;
    }
    }

    @media screen and (min-width: 48rem) {
    html {
        font-size: 16px;
    }
    }

    body {
        line-height: 1.85;
    }

    p,
    .modest-p {
        font-size: 1rem;
        margin-bottom: 1.3rem;
    }

    h1,
    .modest-h1,
    h2,
    .modest-h2,
    h3,
    .modest-h3,
    h4,
    .modest-h4 {
        margin: 1.414rem 0 .5rem;
        font-weight: inherit;
        line-height: 1.42;
    }

    h1,
    .modest-h1 {
        margin-top: 0;
        font-size: 3.998rem;
    }

    h2,
    .modest-h2 {
        font-size: 2.827rem;
    }

    h3,
    .modest-h3 {
        font-size: 1.999rem;
    }

    h4,
    .modest-h4 {
        font-size: 1.414rem;
    }

    h5,
    .modest-h5 {
        font-size: 1.121rem;
    }

    h6,
    .modest-h6 {
        font-size: .88rem;
    }

    small,
    .modest-small {
        font-size: .707em;
    }

    img,
    canvas,
    iframe,
    video,
    svg,
    select,
    textarea {
        max-width: 100%;
    }

    @import url(http://fonts.googleapis.com/css?family=Open+Sans+Condensed:300,300italic,700);

    @import url(http://fonts.googleapis.com/css?family=Arimo:700,700italic);

    html {
        font-size: 18px;
        max-width: 100%;
    }

    body {
        color: #444;
        font-family: 'Open Sans Condensed', sans-serif;
        font-weight: 300;
        margin: 0 auto;
        max-width: 48rem;
        line-height: 1.45;
        padding: .25rem;
    }

    h1,
    h2,
    h3,
    h4,
    h5,
    h6 {
        font-family: Arimo, Helvetica, sans-serif;
    }

    h1,
    h2,
    h3 {
        border-bottom: 2px solid #fafafa;
        margin-bottom: 1.15rem;
        padding-bottom: .5rem;
        text-align: center;
    }

    blockquote {
        border-left: 8px solid #fafafa;
        padding: 1rem;
    }

    pre,
    code {
        background-color: #fafafa;
    }
</style> -->

# Handout – The Full Machine Learning Lifecycle – How to use Machine Learning in Production (MLOps)

Welcome to our tutorial about Machine Learning in Production. We provide three separate hands-on exercises. Through the first two exercises, you will be guided with a Jupyter notebook. For the third exercise, there is a series of tasks for you to complete on your own.

--- 

#### Configuration 
|||
| --- | --- |
| Workdir| <pre>./</pre>|
| Data location| <pre>./data</pre>|
| Jupyter Lab| <pre>localhost:8888</pre>|
| Airflow Webserver| <pre>localhost:8080</pre>|
| MLflow Tracking Server| <pre>localhost:5000</pre>|

--- 
## The Story
You received engine data from several wind turbines in various wind turbine parks. You are asked to develop, deploy, monitor, and update a machine learning model to predict  if an engine is malfunctioning. Every month you receive new data and you need to update the model and validate it is “good enough” and outperforms the previous model. If successful, you need to deploy the updated model. The whole process needs to be fully reproducible.

You have decided not to rely on one of the major cloud providers but to use three open source tools instead:
1. DVC for data versioning
2. MLFlow for experiment and model tracking
3. Apache Airflow for process automatization

---
## Agenda
The workshop is structured into three hands-on parts. During the first two sessions on DVC and MLflow, you will be guided. For the last session on building the full pipeline, there is a series of tasks to complete on your own. (Of course you can reach out to us at any time). 


---
## Tasks


#### <span class="tasks">Introduction to Pipelines (get familiar with airflow/pipeline) ★</span>
Please open the ci_dag.py (continuous integration) in `/dags/ci_dag.py`. In the import section you can find all the functions we use in our Airflow DAG. Now try to do the following:
- [ ] Understand what the `default_args` do. 
- [ ] Find in the ``with dag: `` block a `PythonOperator`  
    ```
    data_split = PythonOperator(
            task_id='data_split',
            python_callable=split_train_test,
            op_kwargs={'data_dir': _data_dir, 'n_days_test': 30}
        )
    ```
    and try to understand what `python_callable` and `op_kwargs` is for
- [ ] Open the `train_model` function and see what the impact of the argument `experiment_name` is. Hint: mlflow.
- [ ] Change the variable `_experiment_name` in the `ci_dag.py` file to `<your_name>` (such that you can later find your experiments on the mlflow tracking server). 
- [ ] Find at the very end of the `ci_dag.py` file the expressions, which build the DAG and try to understand how this works. 
- [ ] Start port forwarding for port `8080` (if not already done during the introduction) and open `localhost:8080` in your web browser. You should now see the Airflow web interface. If you click on ci_pipeline you should see the entire dag and old runs. 
- [ ] On the top right you can start a new run with the play button. 
- [ ] Play around with the UI. How can you reset the running DAG from a specific stage and continue from there?
- [ ] Where do you find the logs of your run?

---
#### <span class="tasks">Move to another day ★</span>
You ran the pipeline in the previous task and everything should work fine. In the real world at some point you will get new data. We simulate this new data ingestion by uncomenting the line 
```
_raw_data_dir = '/data/day2'
```
- [ ] Go to the ci_dag.py file and uncomment the line `_raw_data_dir = '/data/day2'`, then save the file.
- [ ] Go to the web interface and run the pipeline again. 
- [ ] OHHH NOO, what happened? The model_validation step crashed and is red now? Try to find the logs and figure out what happened. 
- [ ] Investigate the code of the validate_model function and find the assertion. What could be the problem?

---
#### <span class="tasks">Improve the Machine Learning Model ★★</span>
Apparently there is some improvement required. Your baseline model doesn’t perform well enough. Let’s try to make this better!
- [ ] Go to the `tune_model.ipynb`  jupyter notebook and play with the ML model to improve it
- [ ] If you found a better model, replace it in the `get_model()` function in `plugins/cd4ml//model_training/train_model.py` and run your pipeline again. Does the pipeline still crash? 

---
#### <span class="tasks">Add DVC Support in the Airflow Pipeline ★★</span>
Earlier in this workshop we saw the power of DVC. In your pipeline everything is fully automatized. But what happens if the upstream data is for some reason not available anymore or changed and you cannot reproduce your results anymore? One solution is to add DVC to your pipeline and track the data.csv dataset.
- [ ] Have a look at the script `plugins/cd4ml/data_processing/track_data.py`.
- [ ] Understand how the track_data method can be used to track your data.csv file.
- [ ] Add the data tracking to your pipeline between the data ingestion and data split. 


    *Hint: the Airflow PythonOperator might be suitable and think about some keyword arguments to pass to the function.* 

---
#### <span class="tasks"> Implement a Hyperparameter Optimization 	(Bonus) ★★★</span>
Finding a good model can be quite tedious. In general there are three approaches to optimize your model selection and hyperparameters:
- Grid search: You just define a set of hyper parameters and models and just try every combination. 
- Random search: You sample both, models and hyperparameters until you find a good combination. 
- Bayesian Optimization: You follow a Bayesian approach to find a promising configuration. 
While grid and random search is quite straightforward to implement, the Bayesian approach needs some additional logic, which is e.g. implemented in ``skopt.BayesSearchCV``. 

In this task you should enhance the train method with a hyperparameter optimization. You can return in the train method later on only the best performing model (meaning the mlflow ID of it). 
