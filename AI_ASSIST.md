# AI Assist Report

## The prompt I gave

 i am trying to switch from print() to info.logging on python but its not showing anything, i am working on a different file than main and logger is configured there 
## The code it suggested

```python
import logging

# __name__ evaluates to the module name (e.g., 'helper'), 
# which correctly links it as a child of the root logger.
logger = logging.getLogger(__name__)

def do_something():
    # Note: It's 'logging.info()', or 'logger.info()' if using an instance
    logger.info("This is an info message from the sub-file!")```

## What I changed and why

<!-- i kept logger = logging.getlogger(__name__)
and i threw away all the rest of the stuff around it because the response was far too long and llm listed all options which i dont need in this instance -->

## Did it work?

<!-- Yes / i learned to use logger in a different file than original and how to link config  from main to the rest of the project -->
