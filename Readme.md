     _ __ ___  ___ _ __   ___  _ __  ___  ___   _ __  _   _ 
    | '__/ _ \/ __| '_ \ / _ \| '_ \/ __|/ _ \ | '_ \| | | |
    | | |  __/\__ \ |_) | (_) | | | \__ \  __/_| |_) | |_| |
    |_|  \___||___/ .__/ \___/|_| |_|___/\___(_) .__/ \__, |
                  |_|                          |_|    |___/ 

# Introduction

Response builds on top of the excelent Requests library by Kenneth Reitz and makes it look a bit DSL-ish.

# Features

* Pythonic DSL-like interface
* Thread safe

# Example

```python
from response import get, response

api = lambda path: 'https://api.github.com' + path

with get(api('/repos/gsamokovarov/frames.py/contributors')):
for metadata in response.json:
    print '%(login)s: %(contributions)d commits' % metadata
```

# License

Copyright 2011 Genadi Samokovarov

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
