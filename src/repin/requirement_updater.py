import pkg_resources


class RequirementUpdater:
    def __init__(self, requirement, latest_version_finder):
        self._requirement = list(pkg_resources.parse_requirements(requirement))[0]
        self._find_latest_version = latest_version_finder

    @property
    def _package_name(self):
        return self._requirement.name

    def update(self):
        major_version = self._find_latest_version(self._requirement).split(".")[0]
        next_major_version = int(major_version) + 1
        spec = f"{self._minimum_version_spec},<{next_major_version}".lstrip(",")
        return f"{self._package_name}{spec}"

    @property
    def _minimum_version_spec(self):
        for op, version in self._requirement.specs:
            if op in (">", ">="):
                return f"{op}{version}"
            elif op == "~=":
                return f">={version}"
        return ""
