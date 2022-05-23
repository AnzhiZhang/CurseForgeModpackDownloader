import requests


class Session:
    def __init__(self):
        self.session = requests.session()
        self.session.headers = {
            'user-agent': ''
        }

    def get(self, url):
        return self.session.get(url)

    def get_download_url(self, project_id, file_id):
        return self.get(
            f'https://addons-ecs.forgesvc.net/api/v2/addon/'
            f'{project_id}/file/{file_id}/download-url'
        ).text
