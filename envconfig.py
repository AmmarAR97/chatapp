import environ
ROOT_DIR = environ.Path(__file__) - 1
env = environ.Env()
env_file = str(ROOT_DIR.path('.env'))
env.read_env(env_file)


def fetch_env_variable(variable_name):
    """
    to fetch all the env variables from .env file
    variable_name: env variable specified in the .env file
    """
    return env(variable_name)
