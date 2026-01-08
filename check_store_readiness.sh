#!/bin/bash

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}"
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║     Home Assistant Addon Store Publishing Status Check         ║"
echo "║         Ventilairsec2HA - Enocean Integration                 ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo -e "${NC}\n"

ADDON_DIR="addons/ventilairsec_enocean"
TOTAL_CHECKS=0
PASSED_CHECKS=0
FAILED_CHECKS=0

# Function to print check
print_check() {
    local status=$1
    local title=$2
    local details=$3
    
    ((TOTAL_CHECKS++))
    
    if [ "$status" = "pass" ]; then
        echo -e "${GREEN}[✓]${NC} $title"
        ((PASSED_CHECKS++))
    elif [ "$status" = "warn" ]; then
        echo -e "${YELLOW}[⚠]${NC} $title"
    else
        echo -e "${RED}[✗]${NC} $title"
        ((FAILED_CHECKS++))
    fi
    
    if [ -n "$details" ]; then
        echo -e "    ${details}"
    fi
}

# Function to check file content
check_yaml_field() {
    local file=$1
    local field=$2
    local value=$3
    
    if grep -q "^${field}:" "$file"; then
        if grep -q "^${field}:.*$value" "$file"; then
            echo -e "${GREEN}✓${NC}"
            return 0
        else
            echo -e "${YELLOW}⚠${NC} (present but value differs)"
            return 1
        fi
    else
        echo -e "${RED}✗${NC}"
        return 2
    fi
}

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}1. REPOSITORY ROOT FILES${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

if [ -f "repository.json" ]; then
    print_check "pass" "repository.json exists" "✓ Registry file present"
    
    # Check JSON validity
    if command -v jq &> /dev/null; then
        if jq '.' repository.json > /dev/null 2>&1; then
            print_check "pass" "repository.json is valid JSON" ""
        else
            print_check "fail" "repository.json has invalid JSON" ""
        fi
    fi
else
    print_check "fail" "repository.json exists" ""
fi

if [ -f "README.md" ]; then
    print_check "pass" "README.md exists" "Repository documentation present"
else
    print_check "fail" "README.md exists" ""
fi

echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}2. ADDON MANIFEST (addon.yaml)${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

if [ ! -f "$ADDON_DIR/addon.yaml" ]; then
    print_check "fail" "$ADDON_DIR/addon.yaml exists"
    exit 1
fi

print_check "pass" "$ADDON_DIR/addon.yaml exists" ""

# Validate YAML
if command -v yq &> /dev/null; then
    if yq eval '.' "$ADDON_DIR/addon.yaml" > /dev/null 2>&1; then
        print_check "pass" "addon.yaml is valid YAML" ""
    else
        print_check "fail" "addon.yaml has YAML syntax errors" ""
    fi
fi

# Check required fields
echo ""
echo -e "  ${CYAN}Required Fields:${NC}"

for field in "name" "description" "version" "slug" "url" "documentation" "codeowners" "startup" "arch"; do
    printf "    • %-20s ... " "$field:"
    check_yaml_field "$ADDON_DIR/addon.yaml" "$field"
done

# Check critical fixes
echo ""
echo -e "  ${CYAN}Critical Fixes Applied:${NC}"

echo -n "    • English descriptions ... "
if grep -q "Ventilairsec VMI Purevent integration" "$ADDON_DIR/addon.yaml"; then
    echo -e "${GREEN}✓${NC}"
    ((PASSED_CHECKS++))
else
    echo -e "${RED}✗${NC}"
    ((FAILED_CHECKS++))
fi

((TOTAL_CHECKS++))

echo -n "    • Correct schema types ... "
if grep -q "type: integer" "$ADDON_DIR/addon.yaml" && grep -q "type: boolean" "$ADDON_DIR/addon.yaml"; then
    echo -e "${GREEN}✓${NC}"
    ((PASSED_CHECKS++))
else
    echo -e "${RED}✗${NC}"
    ((FAILED_CHECKS++))
fi

((TOTAL_CHECKS++))

echo -n "    • homeassistant version ... "
if grep -q "homeassistant:" "$ADDON_DIR/addon.yaml"; then
    echo -e "${GREEN}✓${NC}"
    ((PASSED_CHECKS++))
else
    echo -e "${YELLOW}⚠${NC}"
fi

((TOTAL_CHECKS++))

echo -n "    • NET_ADMIN privileges ... "
if grep -q "NET_ADMIN" "$ADDON_DIR/addon.yaml"; then
    echo -e "${GREEN}✓${NC}"
    ((PASSED_CHECKS++))
else
    echo -e "${RED}✗${NC}"
    ((FAILED_CHECKS++))
fi

((TOTAL_CHECKS++))

echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}3. PRESENTATION FILES (Icon & Logo)${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

echo -n "    • icon.svg exists ... "
if [ -f "$ADDON_DIR/icon.svg" ]; then
    echo -e "${GREEN}✓${NC}"
    ((PASSED_CHECKS++))
else
    echo -e "${RED}✗${NC}"
    ((FAILED_CHECKS++))
fi
((TOTAL_CHECKS++))

echo -n "    • logo.png exists ... "
if [ -f "$ADDON_DIR/logo.png" ]; then
    echo -e "${GREEN}✓${NC}"
    ((PASSED_CHECKS++))
else
    echo -e "${RED}✗${NC}"
    ((FAILED_CHECKS++))
fi
((TOTAL_CHECKS++))

echo -n "    • icon.svg is SVG format ... "
if [ -f "$ADDON_DIR/icon.svg" ] && file "$ADDON_DIR/icon.svg" | grep -q -E "(XML|SVG|text)"; then
    echo -e "${GREEN}✓${NC}"
    ((PASSED_CHECKS++))
else
    echo -e "${YELLOW}⚠${NC}"
fi
((TOTAL_CHECKS++))

echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}4. DOCUMENTATION FILES${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

echo -n "    • README.md exists ... "
if [ -f "$ADDON_DIR/README.md" ]; then
    echo -e "${GREEN}✓${NC}"
    ((PASSED_CHECKS++))
else
    echo -e "${RED}✗${NC}"
    ((FAILED_CHECKS++))
fi
((TOTAL_CHECKS++))

echo -n "    • CHANGELOG.md exists ... "
if [ -f "$ADDON_DIR/CHANGELOG.md" ]; then
    echo -e "${GREEN}✓${NC}"
    ((PASSED_CHECKS++))
else
    echo -e "${RED}✗${NC}"
    ((FAILED_CHECKS++))
fi
((TOTAL_CHECKS++))

echo -n "    • MANIFEST.md exists ... "
if [ -f "$ADDON_DIR/MANIFEST.md" ]; then
    echo -e "${GREEN}✓${NC}"
    ((PASSED_CHECKS++))
else
    echo -e "${RED}✗${NC}"
    ((FAILED_CHECKS++))
fi
((TOTAL_CHECKS++))

echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}5. APPLICATION FILES${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

for file in "Dockerfile" "requirements.txt" "run.sh" "validate.sh" "config.ini.example"; do
    echo -n "    • $file exists ... "
    if [ -f "$ADDON_DIR/$file" ]; then
        echo -e "${GREEN}✓${NC}"
        ((PASSED_CHECKS++))
    else
        echo -e "${RED}✗${NC}"
        ((FAILED_CHECKS++))
    fi
    ((TOTAL_CHECKS++))
done

echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}6. ROOTFS STRUCTURE${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

for dir in "rootfs" "rootfs/app" "rootfs/etc/cont-init.d"; do
    echo -n "    • $dir/ exists ... "
    if [ -d "$ADDON_DIR/$dir" ]; then
        echo -e "${GREEN}✓${NC}"
        ((PASSED_CHECKS++))
    else
        echo -e "${RED}✗${NC}"
        ((FAILED_CHECKS++))
    fi
    ((TOTAL_CHECKS++))
done

for file in "rootfs/run.sh" "rootfs/app/main.py" "rootfs/app/enocean/enocean_daemon.py"; do
    echo -n "    • $file exists ... "
    if [ -f "$ADDON_DIR/$file" ]; then
        echo -e "${GREEN}✓${NC}"
        ((PASSED_CHECKS++))
    else
        echo -e "${RED}✗${NC}"
        ((FAILED_CHECKS++))
    fi
    ((TOTAL_CHECKS++))
done

echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}7. FILE PERMISSIONS${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

for file in "run.sh" "validate.sh" "rootfs/run.sh"; do
    echo -n "    • $ADDON_DIR/$file is executable ... "
    if [ -x "$ADDON_DIR/$file" ]; then
        echo -e "${GREEN}✓${NC}"
        ((PASSED_CHECKS++))
    else
        echo -e "${YELLOW}⚠${NC} (not executable, will fix)"
        chmod +x "$ADDON_DIR/$file"
    fi
    ((TOTAL_CHECKS++))
done

echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}SUMMARY${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

echo ""
echo -e "  Total Checks: ${CYAN}$TOTAL_CHECKS${NC}"
echo -e "  Passed:       ${GREEN}$PASSED_CHECKS${NC}"
echo -e "  Failed:       ${RED}$FAILED_CHECKS${NC}"

if [ $FAILED_CHECKS -eq 0 ]; then
    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║  ✓ All checks passed!                                         ║${NC}"
    echo -e "${GREEN}║  Your addon is ready for the Home Assistant store!            ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "  ${CYAN}Next steps:${NC}"
    echo -e "    1. Commit changes: git add -A && git commit -m \"Fix: Store publishing\""
    echo -e "    2. Push to GitHub: git push origin main"
    echo -e "    3. Wait 24-48 hours for store index refresh"
    echo -e "    4. Users can add repository: https://github.com/fortinric88/Ventilairsec2HA"
    echo ""
else
    echo ""
    echo -e "${RED}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║  ✗ Some checks failed                                         ║${NC}"
    echo -e "${RED}║  Please review the issues above                               ║${NC}"
    echo -e "${RED}╚════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
fi
