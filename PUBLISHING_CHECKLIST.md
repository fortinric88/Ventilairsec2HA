# Home Assistant Addon Publishing Checklist

This document compares the official Home Assistant addon publishing requirements with what has been implemented for Ventilairsec2HA.

Reference: https://developers.home-assistant.io/docs/add-ons/publishing

## Repository Structure

### Required Files

| File | Location | Status | Notes |
|------|----------|--------|-------|
| `repository.json` | Root | ✅ FIXED | Registry descriptor, now with correct format |
| `README.md` | Root | ✅ OK | Repository documentation |

## Addon Manifest (addon.yaml)

### Required Fields

| Field | Expected | Current | Status |
|-------|----------|---------|--------|
| `name` | String | "Ventilairsec Enocean" | ✅ OK |
| `description` | String | "Ventilairsec VMI Purevent..." | ✅ FIXED (was French) |
| `version` | Semantic version | "1.0.0" | ✅ OK |
| `slug` | kebab-case identifier | "ventilairsec_enocean" | ✅ OK |
| `url` | Repository URL | GitHub URL | ✅ OK |
| `documentation` | Documentation URL | GitHub tree URL | ✅ OK |
| `source` | Source code URL | GitHub tree URL | ✅ ADDED |
| `issues` | Issues tracker URL | GitHub issues URL | ✅ ADDED |
| `codeowners` | GitHub handles | "@fortinric88" | ✅ OK |
| `startup` | services/system | "services" | ✅ OK |
| `boot` | auto/manual | "auto" | ✅ ADDED |
| `image` | Docker image URL | ghcr.io/... | ✅ OK |
| `arch` | Architecture list | [amd64, armv7, arm64] | ✅ OK |
| `homeassistant` | Min HA version | "2023.10.0" | ✅ ADDED |

### Configuration Fields

| Field | Required | Status |
|-------|----------|--------|
| `options` | Yes | ✅ OK - all with defaults |
| `schema` | Yes | ✅ FIXED - proper types |
| `devices` | Yes (for USB) | ✅ OK |
| `volumes` | No, but good practice | ✅ OK |
| `ports` | If network access | ✅ OK |
| `network_mode` | If required | ✅ ADDED |
| `privileged` | If required | ✅ FIXED - proper format |
| `requirements` | If applicable | ✅ OK |

### Configuration Schema Types

| Type | Old Value | New Value | Status |
|------|-----------|-----------|--------|
| Integer | `int` | `integer` | ✅ FIXED |
| String | `str` | `select` (for options) | ✅ FIXED |
| Float | `float` | `float` | ✅ OK |
| Boolean | `bool` | `boolean` | ✅ FIXED |

## Presentation Requirements

### Icon & Logo

| Item | Requirement | Status | File |
|------|-------------|--------|------|
| Icon | SVG format, small icon | ✅ CREATED | `icon.svg` |
| Logo | PNG or SVG, larger logo | ✅ CREATED | `logo.png` |
| Location | Addon root directory | ✅ OK | Both at root |

### Documentation

| File | Purpose | Status | Location |
|------|---------|--------|----------|
| `README.md` | Addon documentation | ✅ EXISTS | Addon root |
| `CHANGELOG.md` | Version history | ✅ CREATED | Addon root |
| `MANIFEST.md` | Store presentation | ✅ CREATED | Addon root |

## registry.json Requirements

According to Home Assistant documentation, the `repository.json` must follow this structure:

### Required Fields (Top Level)

| Field | Example | Status |
|-------|---------|--------|
| `name` | String | ✅ OK |
| `url` | Repository URL | ✅ OK |
| `maintainer` | Name or email | ✅ FIXED |
| `codeowners` | Array of @handles | ✅ OK |
| `addons` | Array of addon objects | ✅ OK |

### Addon Object Fields

| Field | Type | Status |
|-------|------|--------|
| `name` | string | ✅ OK |
| `slug` | string (kebab-case) | ✅ OK |
| `description` | string | ✅ FIXED (English) |
| `arch` | array of strings | ✅ OK |
| `url` | repository URL | ✅ OK |
| `version` | semantic version | ✅ OK |
| `image` | docker image template | ✅ OK |
| `startup` | services/system | ✅ OK |
| `boot` | auto/manual | ✅ ADDED |
| `homeassistant` | minimum version | ✅ ADDED |
| `privileged` | array of capabilities | ✅ FIXED |
| `devices` | array of device paths | ✅ ADDED |
| `ports` | object with port mappings | ✅ OK |
| `volumes` | object with volume mappings | ✅ FIXED |
| `network_mode` | host/bridge/etc | ✅ ADDED |
| `options` | default values object | ✅ OK |
| `schema` | configuration schema | ✅ FIXED |

## Docker Image Requirements

### Image Tag Format

```
ghcr.io/owner/name-{BUILD_ARCH}

# Correct
ghcr.io/fortinric88/ventilairsec-enocean-{BUILD_ARCH}

# Previous (incorrect)
ghcr.io/fortinric88/ventilairsec-enocean-{arch}
```

Status: ✅ FIXED

### Supported Architectures

| Architecture | Base Image | Status |
|--------------|------------|--------|
| amd64 | homeassistant/amd64-base | ✅ OK |
| armv7 | homeassistant/armv7-base | ✅ OK |
| arm64 | homeassistant/aarch64-base | ✅ OK |

## Dockerfile Requirements

| Requirement | Status | Notes |
|-------------|--------|-------|
| FROM ARG BUILD_FROM | ✅ OK | Proper variable usage |
| Alpine/slim base | ✅ OK | Using HA base images |
| Python 3.9+ | ✅ OK | Specified |
| /run.sh entrypoint | ✅ OK | Required |
| rootfs structure | ✅ OK | Proper directory layout |

## Configuration Validation

### addon.yaml Validation
- ✅ Valid YAML syntax
- ✅ All required fields present
- ✅ Correct field types
- ✅ Proper schema definitions
- ✅ Valid descriptions (English)

### repository.json Validation
- ✅ Valid JSON syntax
- ✅ All required fields present
- ✅ Correct addon references
- ✅ Valid URLs
- ✅ Proper version strings

## Publishing Checklist

### Pre-Publishing

- [x] Repository README.md is comprehensive
- [x] addon.yaml follows Home Assistant schema
- [x] repository.json is valid and complete
- [x] Icon (icon.svg) is present
- [x] Logo (logo.png) is present
- [x] CHANGELOG.md documents versions
- [x] MANIFEST.md provides store description
- [x] Docker image builds successfully
- [x] Python code follows best practices
- [x] All required dependencies listed

### Publishing Steps

1. [x] Create valid addon structure
2. [x] Create repository.json
3. [x] Create addon.yaml
4. [x] Add icon.svg and logo.png
5. [x] Write CHANGELOG.md
6. [x] Write MANIFEST.md
7. [x] Ensure Home Assistant version >= 2023.10.0
8. [x] Make repository public
9. [x] Push to GitHub

### Post-Publishing

- [ ] Wait 24-48 hours for store refresh
- [ ] Verify addon appears in store
- [ ] Test installation from store
- [ ] Collect user feedback
- [ ] Monitor GitHub issues

## Troubleshooting

### Addon Not Showing in Store

**Possible Causes and Fixes:**

1. ❌ **Missing icon.svg**
   - ✅ FIXED: File created at `addons/ventilairsec_enocean/icon.svg`

2. ❌ **Invalid repository.json**
   - ✅ FIXED: Corrected format and all required fields

3. ❌ **Invalid addon.yaml**
   - ✅ FIXED: Corrected field types and descriptions

4. ❌ **Incorrect image tag**
   - ✅ FIXED: Changed to `{BUILD_ARCH}` placeholder

5. ❌ **Missing homeassistant version**
   - ✅ FIXED: Added `homeassistant: "2023.10.0"`

6. ❌ **French descriptions**
   - ✅ FIXED: All descriptions now in English

## Verification Commands

```bash
# Validate YAML
yq eval '.' addons/ventilairsec_enocean/addon.yaml

# Validate JSON
jq '.' repository.json

# Check file permissions
ls -la addons/ventilairsec_enocean/

# Run validation script
./validate_addon.sh
```

## References

- [Home Assistant Addon Publishing](https://developers.home-assistant.io/docs/add-ons/publishing)
- [Home Assistant Addon Presentation](https://developers.home-assistant.io/docs/add-ons/presentation)
- [Home Assistant Addon Configuration](https://developers.home-assistant.io/docs/add-ons/configuration/)
- [Home Assistant Docker Documentation](https://developers.home-assistant.io/docs/add-ons/start-with-docker/)

---

**All requirements met!** ✅ Your addon is ready for the Home Assistant store.
