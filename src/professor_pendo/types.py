from typing import Literal

type DataEnvironmentT = Literal["io", "eu", "us1", "jpn", "au"]
"""
The Pendo signifier for the GCP data region.

Further reading:
https://support.pendo.io/hc/en-us/articles/22832528657179-Global-data-hosting
"""