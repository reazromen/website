"""Deterministic CMS renderer. Validate every record before changing public output."""
from cms_common import *
from datetime import datetime, timezone
from email.utils import format_datetime
from collections import defaultdict
from copy import deepcopy
import xml.etree.ElementTree as ET

SECTIONS=('writing','perspectives','music','movies','archaeology','heritage','bangla','local-cultures','world-cultures')
ASSET_VERSIONS={}
_SHARED_CHROME=None
