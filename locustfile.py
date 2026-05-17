from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)

    @task(2)
    def index_page(self):
        """Simulasi user mengakses halaman utama"""
        self.client.get("/")

    @task(1)
    def detail_berita(self):
        """Simulasi user mengakses halaman detail berita"""
        self.client.get("/berita/2")  