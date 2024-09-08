import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from azureml.core import Workspace, Experiment, Environment, Dataset, Model
from azureml.core.model import InferenceConfig
from azureml.core.webservice import AksWebservice, AksCompute

# Load dataset from Blob Storage (processed by Databricks)
df = pd.read_csv("path/to/processed_network_kpis.csv")
X = df.drop("downtime", axis=1)
y = df["downtime"]

# Train the model
model = RandomForestRegressor()
model.fit(X, y)

# Save and register the model in Azure ML
workspace = Workspace.from_config()
model_path = "random_forest_model.pkl"
model.save(model_path)
Model.register(workspace=workspace, model_path=model_path, model_name="downtime_prediction_model")

# Set up inference configuration
env = Environment(name="aks-env")
env.python.conda_dependencies.add_pip_package("scikit-learn")
inference_config = InferenceConfig(entry_script="score.py", environment=env)

# Deploy model to AKS
aks_target = AksCompute(workspace, "aks-cluster")
deployment_config = AksWebservice.deploy_configuration(cpu_cores=1, memory_gb=1)
service = Model.deploy(workspace=workspace, name="downtime-prediction-service", models=[model], inference_config=inference_config, deployment_config=deployment_config, deployment_target=aks_target)

service.wait_for_deployment(show_output=True)
print(f"Service deployed at: {service.scoring_uri}")
