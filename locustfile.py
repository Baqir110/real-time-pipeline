from locust import HttpUser, between, task


class PipelineUser(HttpUser):

  wait_time = between(1, 3)

  @task(3)
  def test_health(self):
    self.client.get("/health")

  @task(2)
  def get_metrics(self):
    self.client.get("/api/v1/metrics")

  @task(1)
  def trigger_etl(self):
    self.client.post("/api/v1/trigger-etl")