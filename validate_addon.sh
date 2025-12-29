#!/bin/bash

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}=== Home Assistant Addon Validation ===${NC}\n"

ADDON_DIR="addons/ventilairsec_enocean"
PASSED=0
FAILED=0

# Function to check file exists
check_file() {
    local file=$1
    local description=$2
    
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} $description"
        ((PASSED++))
    else
        echo -e "${RED}✗${NC} $description - MISSING: $file"
        ((FAILED++))
    fi
}

# Function to check directory exists
check_dir() {
    local dir=$1
    local description=$2
    
    if [ -d "$dir" ]; then
        echo -e "${GREEN}✓${NC} $description"
        ((PASSED++))
    else
        echo -e "${RED}✗${NC} $description - MISSING: $dir"
        ((FAILED++))
    fi
}

echo -e "${BLUE}Required Root Files:${NC}"
check_file "repository.json" "repository.json (addon registry)"
check_file "README.md" "README.md (repository documentation)"

echo -e "\n${BLUE}Addon Structure:${NC}"
check_dir "$ADDON_DIR" "Addon directory"
check_file "$ADDON_DIR/addon.yaml" "addon.yaml (addon manifest)"
check_file "$ADDON_DIR/Dockerfile" "Dockerfile (container definition)"
check_file "$ADDON_DIR/README.md" "README.md (addon documentation)"
check_file "$ADDON_DIR/CHANGELOG.md" "CHANGELOG.md (version history)"
check_file "$ADDON_DIR/MANIFEST.md" "MANIFEST.md (presentation info)"
check_file "$ADDON_DIR/icon.svg" "icon.svg (addon icon)"
check_file "$ADDON_DIR/logo.png" "logo.png (addon logo)"
check_file "$ADDON_DIR/requirements.txt" "requirements.txt (Python dependencies)"

echo -e "\n${BLUE}Script Files:${NC}"
check_file "$ADDON_DIR/run.sh" "run.sh (startup script)"
check_file "$ADDON_DIR/validate.sh" "validate.sh (validation script)"

echo -e "\n${BLUE}rootfs Structure:${NC}"
check_dir "$ADDON_DIR/rootfs" "rootfs directory"
check_file "$ADDON_DIR/rootfs/run.sh" "rootfs/run.sh (container startup)"
check_dir "$ADDON_DIR/rootfs/app" "rootfs/app (application code)"
check_dir "$ADDON_DIR/rootfs/etc/cont-init.d" "rootfs/etc/cont-init.d (init scripts)"

echo -e "\n${BLUE}Python Application Files:${NC}"
check_file "$ADDON_DIR/rootfs/app/main.py" "main.py (entry point)"
check_file "$ADDON_DIR/rootfs/app/homeassistant_bridge.py" "homeassistant_bridge.py"
check_file "$ADDON_DIR/rootfs/app/homeassistant_entities.py" "homeassistant_entities.py"
check_file "$ADDON_DIR/rootfs/app/device_config.py" "device_config.py"
check_file "$ADDON_DIR/rootfs/app/enocean/enocean_daemon.py" "enocean_daemon.py"

echo -e "\n${BLUE}Configuration Files:${NC}"
check_file "$ADDON_DIR/config.ini.example" "config.ini.example"

echo -e "\n${BLUE}YAML Validation:${NC}"

# Check if yq is available
if command -v yq &> /dev/null; then
    if yq eval '.' "$ADDON_DIR/addon.yaml" > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} addon.yaml is valid YAML"
        ((PASSED++))
    else
        echo -e "${RED}✗${NC} addon.yaml has YAML syntax errors"
        ((FAILED++))
    fi
else
    echo -e "${YELLOW}⚠${NC} yq not installed, skipping YAML validation"
fi

# Check if jq is available
if command -v jq &> /dev/null; then
    if jq '.' repository.json > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} repository.json is valid JSON"
        ((PASSED++))
    else
        echo -e "${RED}✗${NC} repository.json has JSON syntax errors"
        ((FAILED++))
    fi
else
    echo -e "${YELLOW}⚠${NC} jq not installed, skipping JSON validation"
fi

echo -e "\n${BLUE}File Permissions:${NC}"

if [ -x "$ADDON_DIR/run.sh" ]; then
    echo -e "${GREEN}✓${NC} run.sh is executable"
    ((PASSED++))
else
    echo -e "${YELLOW}⚠${NC} run.sh is not executable (fixing...)"
    chmod +x "$ADDON_DIR/run.sh"
fi

if [ -x "$ADDON_DIR/validate.sh" ]; then
    echo -e "${GREEN}✓${NC} validate.sh is executable"
    ((PASSED++))
else
    echo -e "${YELLOW}⚠${NC} validate.sh is not executable (fixing...)"
    chmod +x "$ADDON_DIR/validate.sh"
fi

echo -e "\n${BLUE}Summary:${NC}"
echo -e "${GREEN}Passed:${NC} $PASSED"
echo -e "${RED}Failed:${NC} $FAILED"

if [ $FAILED -eq 0 ]; then
    echo -e "\n${GREEN}✓ All checks passed!${NC}"
    exit 0
else
    echo -e "\n${RED}✗ Some checks failed. Please review the issues above.${NC}"
    exit 1
fi
