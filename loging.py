#!/usr/bin/env python
import logging

#basic configuration and instancing
LOG_FILENAME = 'logfajl.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO)

logger = logging.getLogger(__name__)
logger.info('start logging')
logger.info('Reading...')
logger.info('Done')

