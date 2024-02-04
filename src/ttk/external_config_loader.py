import importlib.util
import sys
from typing import Union

from ttk.models.config_models import ConfigBaseModel, CategoryChunkConfigModel, SummaryChunkConfigModel, \
    QuestionChunkConfigModel


def load_external_config_from_file(file_path: str) -> Union[CategoryChunkConfigModel, SummaryChunkConfigModel,
QuestionChunkConfigModel, ConfigBaseModel]:
    """Load the configuration from the python file using the importlib approach"""
    # Set the name of the module
    module_name = 'config_module'
    # we need to create specs for the module
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    # Now create the module from the specs
    module = importlib.util.module_from_spec(spec)
    # Add it to sys.modules so it can be loaded
    sys.modules[module_name] = module
    # Load the module, the code should be interpreted
    spec.loader.exec_module(module)
    return module.config


def load_external_config_from_file_exec(file_path: str) -> Union[CategoryChunkConfigModel, SummaryChunkConfigModel,
QuestionChunkConfigModel, ConfigBaseModel]:
    """Load the Python code from the config file and return the configuration"""
    with open(file_path, "r") as config_file:
        config_code = config_file.read()
    execution_environment = {}
    exec(config_code, execution_environment)
    config = execution_environment['config']
    return config
