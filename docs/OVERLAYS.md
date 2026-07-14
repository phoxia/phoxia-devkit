# DevKit overlays

An overlay may add profiles, layers, plugins and local policy without copying or replacing public DevKit source.

Set `PHOXIA_DEVKIT_OVERLAY` to an absolute overlay directory containing `manifest.json`. The manifest must identify the public package and its exact compatible version. Existing public paths cannot be overridden. Overlay component references resolve locally first and may then reuse public components.

This environment variable is an internal composition interface for installer wrappers. Installing an overlay keeps its files under the installed package's `overlay/` directory; it does not make private material public or publishable. The public DevKit works without an overlay.
