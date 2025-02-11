**Build and Deploy a Custom Dockerized ML API**

Create a custom Docker image to host your ML model and serve it through an API.
Use this image to deploy two instances (containers) of the ML API.
Configure Nginx as a load balancer to evenly distribute incoming requests between the two ML API containers.
Modify the API response to include a unique identifier, such as the container's IP address or instance ID. This will help you verify which instance handled each request and confirm the load balancer is working correctly.

**Verify Load Balancer Functionality**

Send multiple requests to the Nginx load balancer and demonstrate that the responses are served alternately by the two ML containers.
Show the API responses, highlighting the unique identifiers to verify load balancing.

**Performance Profiling with Synthetic Workload**

Use a synthetic workload generator, such as httperf, JMeter, or k6(i am using locust) to simulate ramp-up requests to the load balancer.
Monitor and profile the CPU and memory usage of all three Docker instances (Nginx and the two ML API containers) under load.
Present the resource usage results in a structured manner to analyze the performance impact of the workload.