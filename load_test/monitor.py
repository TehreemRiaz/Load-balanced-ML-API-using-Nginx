import requests
import time
import os
import pandas as pd
import matplotlib.pyplot as plt

# Docker API URL for Windows Docker Desktop
DOCKER_API_URL = "http://host.docker.internal:2375"
CONTAINERS = ["nginx", "ml_api_1", "ml_api_2"]
OUTPUT_DIR = "./output"
CSV_FILE = os.path.join(OUTPUT_DIR, "docker_stats.csv")
MONITOR_DURATION = 60  # Monitor duration in seconds
INTERVAL = 1           # Interval between stats


def get_container_stats(container_id):
    url = f"{DOCKER_API_URL}/containers/{container_id}/stats?stream=false"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def monitor_containers(duration):
    start_time = time.time()
    stats_data = []

    while time.time() - start_time < duration:
        for container_name in CONTAINERS:
            try:
                url = f"{DOCKER_API_URL}/containers/{container_name}/json"
                response = requests.get(url)
                response.raise_for_status()
                container_id = response.json()["Id"]

                stats = get_container_stats(container_id)
                cpu_usage = stats["cpu_stats"]["cpu_usage"]["total_usage"]
                memory_usage = stats["memory_stats"]["usage"]
                stats_data.append({
                    "timestamp": time.time(),
                    "container": container_name,
                    "cpu_usage": cpu_usage,
                    "memory_usage": memory_usage
                })
            except Exception as e:
                print(f"Error monitoring container {container_name}: {e}")
        time.sleep(INTERVAL)
    return stats_data


def save_stats_to_csv(stats):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df = pd.DataFrame(stats)
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit='s')
    df.to_csv(CSV_FILE, index=False)
    print(f"Stats saved to {CSV_FILE}")


def plot_combined_stats(stats):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df_stats = pd.DataFrame(stats)
    df_stats["timestamp"] = pd.to_datetime(df_stats["timestamp"], unit='s')



    for container_name in CONTAINERS:
        container_stats = df_stats[df_stats["container"] == container_name]

        plt.figure(figsize=(14, 8))


        # Plot CPU usage
        plt.subplot(3, 1, 2)
        plt.plot(container_stats["timestamp"], container_stats["cpu_usage"], label="CPU Usage", color="green")
        plt.ylabel("CPU Usage")
        plt.grid()
        plt.legend()

        # Plot Memory usage
        plt.subplot(3, 1, 3)
        plt.plot(container_stats["timestamp"], container_stats["memory_usage"], label="Memory Usage", color="orange")
        plt.ylabel("Memory Usage (Bytes)")
        plt.xlabel("Time")
        plt.grid()
        plt.legend()

        # Save the combined plot
        plot_file = os.path.join(OUTPUT_DIR, f"{container_name}_combined_usage.png")
        plt.tight_layout()
        plt.savefig(plot_file)
        print(f"Combined plot saved to {plot_file}")




if __name__ == "__main__":
    print(f"Monitoring Docker containers for {MONITOR_DURATION} seconds...")
    stats = monitor_containers(MONITOR_DURATION)
    save_stats_to_csv(stats)
    plot_combined_stats(stats)
    print("Monitoring complete. Outputs saved.")
