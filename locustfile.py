from locust import HttpUser, task, between


class PipelineUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def get_metrics(self):
        self.client.get("/api/v1/metrics")

    @task(1)
    def trigger_etl(self):
        self.client.post("/api/v1/trigger-etl")
