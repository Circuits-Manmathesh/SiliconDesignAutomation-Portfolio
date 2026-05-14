# Architecture

SiliconDesignAutomation follows a spec-to-evidence flow for analog circuit development.

```text
Specification -> device-region reasoning -> sizing candidates -> generated testbenches -> verification evidence -> public report package
```

The public repository shows the reviewable structure and evidence artifacts while excluding private PDK files, raw simulator outputs, private LUT databases, and full internal optimizer implementation.
