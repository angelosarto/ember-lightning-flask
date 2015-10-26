import os
import json
import enum

class ConfigSource(enum.Enum):
    NOT_LOADED = 0
    ENV_VARS = 1
    CLOUD_FOUNDRY = 2
    LOCAL_FILE = 3

class Configuration:
    def __init__(self):
        self.config_source = ConfigSource.NOT_LOADED

        self.application_port = None
        self.instance_id = None
        self.redis_host = None
        self.redis_port = None
        self.redis_secret = None
        self.this_app_name = 'local'

        self.lightning_app_map = None
        self.lightning_app_name = None
        self.lightning_url = ""
        self.lightning_app_automatic = False

    def load(self):
        # Try to load environment from Direct environment variables (e.g. Docker, standalone), then CloudFoundry
        # then locally from the config/active directory
        if os.getenv('PORT'):
            self.config_source = ConfigSource.ENV_VARS
        elif os.getenv('VCAP_APP_PORT'):
            self.config_source = ConfigSource.CLOUD_FOUNDRY
        else:
            try:
                from config.envutils import source_bash_file

                source_bash_file('config/active/env.sh')
            except ImportError:
                pass
            if os.getenv('PORT'):
                self.config_source = ConfigSource.LOCAL_FILE

        if self.config_source in [ConfigSource.LOCAL_FILE, ConfigSource.ENV_VARS]:
            self.application_port = int(os.getenv("PORT", 0))
            self.instance_id = int(os.getenv("INSTANCE", 0))
            self.redis_host = os.getenv("REDIS_HOST", "redis")
            self.redis_port = int(os.getenv("REDIS_PORT", 6379))
            self.redis_secret = os.getenv("REDIS_SECRET", "")

        elif self.config_source == ConfigSource.CLOUD_FOUNDRY:
            self.application_port = int(os.getenv("VCAP_APP_PORT") or 0)
            self.instance_id = int(os.getenv("CF_INSTANCE_INDEX") or 0)
            if os.environ.get('VCAP_SERVICES'):
                json_services = json.loads(os.environ['VCAP_SERVICES'])

                if json_services.get('rediscloud'):
                    self.redis_host = json_services['rediscloud'][0]['credentials']['hostname']
                    self.redis_port = json_services['rediscloud'][0]['credentials']['port']
                    self.redis_secret = json_services['rediscloud'][0]['credentials']['password']
                else:
                    print("No Redis Server Configured in CLoud Foundry")
                    return False

            if os.environ.get('VCAP_APPLICATION'):
                self.this_app_name = json.loads(os.environ['VCAP_APPLICATION'])['application_name']

        else:
            # Couldn't load a config -- Stop loading
            return False

        # Load Common Environment Variables
        self.lightning_app_map = os.getenv("APP_MAP", None)
        if self.lightning_app_map is not None:
            self.lightning_app_map = json.loads(self.lightning_app_map)
        else:
            self.lightning_app_name = os.getenv("APP_NAME", None)
            self.lightning_url = os.getenv("URL_PREFIX", "")
            if self.lightning_app_name == "AUTO":
                self.lightning_app_automatic = True

        if self.lightning_app_map is None and self.lightning_app_name is None:
            print("No Lightning application name(s) specified, set APP_NAME or APP_MAP environment variables")
            return False
        return True

