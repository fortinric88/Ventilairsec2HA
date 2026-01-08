# ❌ Why Addon Doesn't Appear in Store - Solution Guide

## Problem Summary

Your Ventilairsec Enocean addon is correctly structured but may not appear in the Home Assistant store due to missing prerequisites or configuration issues.

## Requirements for Store Visibility

### 1. ✅ Repository Configuration
- **Status**: READY
- Your `repository.json` is properly configured
- All required fields are present

### 2. ✅ Addon Structure  
- **Status**: READY
- addon.yaml is valid and compliant
- All required files present
- Configuration schema matches standards

### 3. ⚠️ Docker Images Must Be Pre-Built

**CRITICAL**: Home Assistant store requires pre-built Docker images on GHCR (GitHub Container Registry).

The addon uses this image reference:
```
ghcr.io/fortinric88/ventilairsec-enocean-{BUILD_ARCH}
```

These images must be **pre-built and published** on GHCR for architectures:
- `amd64` → `ghcr.io/fortinric88/ventilairsec-enocean-amd64:latest`
- `armv7` → `ghcr.io/fortinric88/ventilairsec-enocean-armv7:latest`  
- `arm64` → `ghcr.io/fortinric88/ventilairsec-enocean-arm64:latest`

### 4. ⚠️ Repository Must Be Public

The repository must be **public** on GitHub for the store to access it.

## Solution: Building and Publishing Images

### Step 1: Set Up GitHub Container Registry Access

1. Go to your GitHub repository: https://github.com/fortinric88/Ventilairsec2HA
2. Navigate to **Settings** → **Developer settings** → **Personal access tokens** → **Tokens (classic)**
3. Generate a new token with `write:packages` scope
4. Save the token securely

### Step 2: Create GitHub Actions Workflow

Create `.github/workflows/build-addon.yml`:

```yaml
name: Build and Publish Addon

on:
  push:
    branches:
      - main
    paths:
      - 'addons/ventilairsec_enocean/**'
      - '.github/workflows/build-addon.yml'

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ventilairsec-enocean

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    strategy:
      matrix:
        include:
          - arch: amd64
            build_arch: linux/amd64
          - arch: armv7
            build_arch: linux/arm/v7
          - arch: arm64
            build_arch: linux/arm64
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2
      
      - name: Log in to Container Registry
        uses: docker/login-action@v2
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Build and push Docker image
        uses: docker/build-push-action@v4
        with:
          context: ./addons/ventilairsec_enocean
          platforms: ${{ matrix.build_arch }}
          push: true
          tags: |
            ${{ env.REGISTRY }}/${{ github.repository_owner }}/${{ env.IMAGE_NAME }}-${{ matrix.arch }}:latest
            ${{ env.REGISTRY }}/${{ github.repository_owner }}/${{ env.IMAGE_NAME }}-${{ matrix.arch }}:${{ github.sha }}
```

### Step 3: Push to Trigger Build

```bash
git add .github/workflows/build-addon.yml
git commit -m "Add GitHub Actions workflow for building addon images"
git push
```

The workflow will automatically build and push images to GHCR.

### Step 4: Verify Images Are Published

Check that images are available:
```bash
docker pull ghcr.io/fortinric88/ventilairsec-enocean-amd64:latest
docker pull ghcr.io/fortinric88/ventilairsec-enocean-armv7:latest
docker pull ghcr.io/fortinric88/ventilairsec-enocean-arm64:latest
```

## Checklist for Store Submission

- [x] addon.yaml is valid and properly formatted
- [x] repository.json is properly configured
- [x] All required files present (addon.yaml, Dockerfile, run.sh, requirements.txt, README.md)
- [x] Configuration schema defined with proper types
- [x] MQTT configuration included
- [ ] **Docker images built and published to GHCR** ← THIS IS THE KEY
- [ ] Repository is public
- [ ] Images are accessible from GHCR

## Troubleshooting

### Images Don't Build
- Check the `.github/workflows/build-addon.yml` file
- Verify the Dockerfile syntax
- Check that all base images are available

### Images Build But Store Still Doesn't Show Addon
- Verify repository.json references correct image tags
- Check that repository is public
- Wait 24 hours for store cache to update
- Contact Home Assistant community for store debugging

### Manual Building (Alternative)

If you want to build images locally:

```bash
# For amd64
docker build -t ghcr.io/fortinric88/ventilairsec-enocean-amd64:latest addons/ventilairsec_enocean
docker push ghcr.io/fortinric88/ventilairsec-enocean-amd64:latest

# For armv7 (cross-compilation)
docker buildx build --platform linux/arm/v7 -t ghcr.io/fortinric88/ventilairsec-enocean-armv7:latest -o type=registry addons/ventilairsec_enocean

# For arm64
docker buildx build --platform linux/arm64 -t ghcr.io/fortinric88/ventilairsec-enocean-arm64:latest -o type=registry addons/ventilairsec_enocean
```

## Additional Resources

- [Home Assistant Add-ons Documentation](https://developers.home-assistant.io/docs/add-ons)
- [Home Assistant Store Publishing](https://developers.home-assistant.io/docs/add-ons/publishing)
- [GitHub Container Registry Guide](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)

## Next Steps

1. **Set up GitHub Actions** - Create the build workflow
2. **Push changes** - Trigger automatic builds
3. **Verify images** - Confirm images appear on GHCR
4. **Test addon** - Install from your repository
5. **Wait for store update** - Store should recognize addon within 24 hours
