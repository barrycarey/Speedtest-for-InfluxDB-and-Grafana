import logging
import os
from configparser import ConfigParser
from typing import List, Optional

from pydantic import ValidationError

from speedmon.storage.constants import STORAGE_CONFIG_MAP
from speedmon.storage.storage_config import StorageConfig
from speedmon.storage.storage_handler_base import StorageHandlerBase

log = logging.getLogger(__name__)


def filter_dead_storage_handlers(handler: StorageHandlerBase) -> bool:
    handler.validate_connection()
    return handler.active


def init_storage_handlers(ini: ConfigParser = None) -> List[StorageHandlerBase]:
    """
    Attempt to build each type of storage handler from both an ini file (if provided) and from ENV.
    If we successfully build the same handler from each source, take the ENV handler
    :param ini: Optional ConfigParser object
    :return: List of storage handlers
    :rtype: List[StorageHandlerBase]
    """
    storage_handlers = []
    for handler_name in STORAGE_CONFIG_MAP.keys():
        storage_handler_from_ini = None
        storage_handler_from_env = init_storage_handler_from_env(handler_name)
        if ini:
            storage_handler_from_ini = init_storage_handler_from_ini(handler_name, ini)
        if storage_handler_from_env:
            storage_handlers.append(storage_handler_from_env)
        elif storage_handler_from_ini:
            storage_handlers.append(storage_handler_from_ini)

    return storage_handlers


def init_storage_handlers_from_ini(ini: ConfigParser) -> List[StorageHandlerBase]:
    """
    Returns all possible storage handlers with valid configs from ini
    :rtype: List[StorageHandlerBase]
    """
    storage_handlers = []
    for key in STORAGE_CONFIG_MAP.keys():
        storage_handler = init_storage_handler_from_ini(key, ini)
        if storage_handler:
            storage_handlers.append(storage_handler)

    return storage_handlers


def init_storage_handler_from_ini(handler_name: str, ini: ConfigParser) -> Optional[StorageHandlerBase]:
    """
    Take a handler name and construct the handler from ENV variables
    :param handler_name: Name of handler to build
    :return: StorageHandlerBase
    :rtype: Optional[StorageHandlerBase]
    """
    if handler_name.upper() not in ini.sections():
        log.info('No config section defined for %s in INI', handler_name.upper())
        return None

    try:
        storage_config = storage_handler_config_from_ini(handler_name, ini)
    except ValidationError:
        log.error('Unable to build valid config from ENV for handler %s', handler_name)
        return
    except ValueError as e:
        log.error('%s is not a valid storage handler name. Valid options are %s', handler_name, ", ".join(list(STORAGE_CONFIG_MAP.keys())))
        return

    return STORAGE_CONFIG_MAP[handler_name]['handler'](storage_config)


def storage_handler_config_from_ini(handler_name: str, ini: ConfigParser) -> StorageConfig:
    """
    Take a ConfigParser object and built a storage config from the sections
    :param handler_name: Name of handler to try and build config for
    :param ini: ConfigParser Object
    :return: StorageConfig
    :rtype: StorageConfig
    """
    if handler_name not in STORAGE_CONFIG_MAP.keys():
        raise ValueError(
            f'{handler_name} is not a valid storage handler name.  Valid options are {", ".join(list(STORAGE_CONFIG_MAP.keys()))}')

    if handler_name.upper() not in ini.sections():
        raise ValueError(f'No {handler_name.upper()} section in config')

    return STORAGE_CONFIG_MAP[handler_name]['config'](**dict(ini.items(handler_name.upper())))


def init_storage_handlers_from_env() -> List[StorageHandlerBase]:
    """
    Returns all possible storage handlers with valid configs from ENV Variables
    :rtype: List[StorageHandlerBase]
    """
    storage_handlers = []
    for key in STORAGE_CONFIG_MAP.keys():
        storage_handler = init_storage_handler_from_env(key)
        if storage_handler:
            storage_handlers.append(storage_handler)

    return storage_handlers


def init_storage_handler_from_env(handler_name: str) -> Optional[StorageHandlerBase]:
    """
    Take a handler name and construct the handler from ENV variables
    :param handler_name: Name of handler to build
    :return: StorageHandlerBase
    :rtype: Optional[StorageHandlerBase]
    """
    if not storage_handler_name_in_env_vars(handler_name):
        return
    try:
        storage_config = storage_handler_conf_from_env(handler_name)
    except ValidationError:
        log.error('Unable to build valid config from ENV for handler %s', handler_name)
        return
    except ValueError as e:
        log.error('%s is not a valid storage handler name. Valid options are %s', handler_name,
                  ", ".join(list(STORAGE_CONFIG_MAP.keys())))
        return

    return STORAGE_CONFIG_MAP[handler_name]['handler'](storage_config)


def storage_handler_conf_from_env(handler_name: str) -> StorageConfig:
    """
    Take a name of a storage handler and scan ENV variables looking for any prefixed with the name.

    If no ENV Vars are found, pydantic will throw a validation error when attempting to create

    :param handler_name: Name of handler to look for config items
    :return: A Storage config
    :rtype: StorageConfig
    """
    if handler_name not in STORAGE_CONFIG_MAP.keys():
        raise ValueError(
            f'{handler_name} is not a valid storage handler name.  Valid options are {", ".join(list(STORAGE_CONFIG_MAP.keys()))}')

    config_vals = {}
    for key, value in os.environ.items():
        if handler_name.upper() in key:
            new_key = key.replace(f'{handler_name.upper()}_', '').lower()
            config_vals[new_key] = value
    return STORAGE_CONFIG_MAP[handler_name]['config'](**config_vals)


def storage_handler_name_in_env_vars(handler_name: str) -> bool:
    for key in os.environ.keys():
        if handler_name in key.lower():
            return True
    return False