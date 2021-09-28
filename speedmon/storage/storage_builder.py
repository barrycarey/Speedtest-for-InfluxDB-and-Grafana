import logging
import os
from configparser import ConfigParser
from typing import List, Optional

from pydantic import ValidationError

from speedmon.storage.constants import STORAGE_CONFIG_MAP, ValidHandlerNames
from speedmon.storage.storage_config import StorageConfig
from speedmon.storage.storage_handler_base import StorageHandlerBase

log = logging.getLogger(__name__)


def filter_dead_storage_handlers(handler: StorageHandlerBase) -> bool:
    handler.validate_connection()
    return handler.active


def init_storage_handlers_from_cfg(config: ConfigParser) -> List[StorageHandlerBase]:
    """
    Create all storage handlers available in config file.
    :rtype: List[StorageHandlerBase]
    """
    handlers = []
    for section in config.sections():
        if 'storage' in section.lower():
            storage_handler_name = section.split('_')[1].lower()
            if storage_handler_name not in STORAGE_CONFIG_MAP:
                log.error('Handler %s is not mapped, skipping', storage_handler_name)
                continue

            try:
                hndlr_cfg = STORAGE_CONFIG_MAP[storage_handler_name]['config'](**dict(config.items(section)))
            except ValidationError as e:
                log.error(e)
                continue
            handlers.append(
                STORAGE_CONFIG_MAP[storage_handler_name]['handler'](hndlr_cfg)
            )
            log.info('Storage Handler %s created', storage_handler_name)

    return list(filter(filter_dead_storage_handlers, handlers))


def init_storage_handlers_from_env() -> List[StorageHandlerBase]:
    handlers = []
    for key in STORAGE_CONFIG_MAP.keys():
        try:
            hndlr_cfg = storage_handler_conf_from_env(key)
        except ValidationError:
            log.debug('No ENV config found for %s', key)
            continue

        handlers.append(
            STORAGE_CONFIG_MAP[key]['handler'](hndlr_cfg)
        )
        log.info('Storage Handler %s created', key)

    return handlers

def init_storage_handler_from_env(handler_name: str) -> Optional[StorageHandlerBase]:
    pass

def init_storage_handler_from_ini(handler_name: str, cfg: ConfigParser) -> Optional[StorageHandlerBase]:
    pass

def init_storage_handlers(config: ConfigParser ) -> List[StorageHandlerBase]:
    storage_handlers = []
    for handler_name in STORAGE_CONFIG_MAP.keys():
        storage_config = None
        try:
            if config:
                storage_config = storage_handler_config_from_config_obj(config)
            storage_config = storage_handler_conf_from_env(handler_name)  # Takes priority if both are defined
        except (ValidationError, ValueError):
            pass

        if storage_config:
            storage_handlers.append(
                STORAGE_CONFIG_MAP[handler_name]['handler'](storage_config)
            )
            continue

    return storage_handlers



def storage_handler_config_from_config_obj(handler_name: str, config: ConfigParser) -> StorageConfig:
    """
    Take a ConfigParser object and built a storage config from the sections
    :param handler_name: Name of handler to try and build config for
    :param config: ConfigParser Object
    :return: StorageConfig
    :rtype: StorageConfig
    """
    if handler_name not in STORAGE_CONFIG_MAP.keys():
        raise ValueError(
            f'{handler_name} is not a valid storage handler name.  Valid options are {STORAGE_CONFIG_MAP.keys}')

    if handler_name.upper() not in config.sections():
        raise ValueError(f'No {handler_name.upper()} section in config')

    return STORAGE_CONFIG_MAP[handler_name]['config'](**dict(config.items(handler_name.upper())))

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
            f'{handler_name} is not a valid storage handler name.  Valid options are {STORAGE_CONFIG_MAP.keys}')

    config_vals = {}
    for key, value in os.environ.items():
        if handler_name.upper() in key:
            new_key = key.replace(f'{handler_name.upper()}_', '').lower()
            config_vals[new_key] = value
    return STORAGE_CONFIG_MAP[handler_name]['config'](**config_vals)
