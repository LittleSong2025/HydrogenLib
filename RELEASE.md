# HydrogenLib Core Module v0.2.1a1 Release

This release contains the core module of HydrogenLib which includes essential components for basic operations.

## Included Modules

- `_hycore`: Core functionality
- `_hyctypes`: C types support
- `_hynet_structure`: Network structure utilities
- `hycore.py`: Core module interface
- `hyctypes.py`: C types interface
- `hynet_structure.py`: Network structure interface

## Version Information

- Version: v0.2.1a1
- Type: Alpha release
- Branch: release/core-module-v0.2.1a1

## How to Use

To use this core module, you can directly import the required components from the hydrogenlib package:

```python
from hydrogenlib.hycore import SomeCoreClass
from hydrogenlib.hyctypes import SomeCType
from hydrogenlib.hynet_structure import SomeNetworkStructure
```

## Build Process

This release was built using the GitHub Actions workflow defined in `.github/workflows/build-core-module.yml`.

## Changelog

- Initial release of the core module
- Extracted essential components from the main library
- Prepared for independent distribution