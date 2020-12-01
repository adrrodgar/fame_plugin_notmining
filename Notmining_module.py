try:
    import requests
    HAVE_REQUESTS = True
except ImportError:
    HAVE_REQUESTS = False

from fame.common.utils import tempdir
from fame.common.exceptions import ModuleInitializationError, ModuleExecutionError
from fame.core.module import ProcessingModule

class Polyswarm_module(ProcessingModule):

    name = "notmining"
    description = "Get report from Notmining platform."
    config = [
        {
            'name': 'api_key',
            'type': 'string',
            'description': 'API Key needed to use the Notmining API',
        },
        {
            'name': 'notmining_url',
            'type': 'string',
            'description': 'URL needed to use the Notmining API',
        }
    ]

    def initialize(self):
        if not HAVE_REQUESTS:
            raise ModuleInitializationError(self, 'Missing dependency: requests')

        return True

    def each_with_type(self, target, file_type):
        # Set root URLs
        self.results = dict()
        if file_type == 'url':
            if not "http://" in target and not "https://" in target:
                target = "http://" + target

            try:
                params = {'api': self.api_key, 'domain': target}
                response = requests.post(url=self.notmining_url, data=params)
                if response.status_code == 200:
                    report = response.text
                    if "Positive" in report:
                        self.results['verdict'] = "Suspicious"
                    elif "Negative" in report:
                        self.results['verdict'] = "Clean"
                    else:
                        raise ModuleExecutionError(self, "Report error")
                else:
                    raise ModuleExecutionError(self, "Network error")

                return True
            except Exception:
                return False
