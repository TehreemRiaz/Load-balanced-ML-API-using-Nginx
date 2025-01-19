from locust import HttpUser, task, between

class LoadTester(HttpUser):
    wait_time = between(1, 2)

    @task
    def predict(self):
        # Example input data
        input_data = {
            "inputs": [[5.1, 3.5, 1.4, 0.2]]
        }
        
        # Send POST request to the /predict endpoint
        response = self.client.post("/predict", json=input_data)
        
        if response.status_code == 200:
            print("Response:", response.json())
        else:
            print("Failed request with status code:", response.status_code)
