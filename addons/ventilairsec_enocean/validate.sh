#!/bin/bash
# Addon validation script for Home Assistant
# Ensures the addon follows HA standards and can appear in store

set -e

echo "=== Validating Ventilairsec Enocean Addon ==="
echo ""

# Check required files
echo "✓ Checking required files..."
required_files=(
    "addon.yaml"
    "Dockerfile"
    "README.md"
    "requirements.txt"
    "rootfs/run.sh"
)

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ MISSING: $file"
        exit 1
    fi
done

echo ""
echo "✓ Validating addon.yaml..."
# Check if addon.yaml is valid YAML
if python3 -c "import yaml; yaml.safe_load(open('addon.yaml'))" 2>/dev/null; then
    echo "  ✅ addon.yaml is valid YAML"
else
    echo "  ❌ addon.yaml is invalid YAML"
    exit 1
fi

echo ""
echo "✓ Validating Dockerfile..."
if grep -q "FROM" Dockerfile && grep -q "ENTRYPOINT\|CMD" Dockerfile; then
    echo "  ✅ Dockerfile is valid"
else
    echo "  ❌ Dockerfile missing FROM or ENTRYPOINT/CMD"
    exit 1
fi

echo ""
echo "✓ Checking addon structure..."
if [ -d "rootfs/app" ]; then
    echo "  ✅ Application directory exists"
else
    echo "  ❌ Missing rootfs/app directory"
    exit 1
fi

echo ""
echo "✓ Checking configuration schema..."
# Validate that schema has required fields
if grep -q "serial_port" addon.yaml && grep -q "mqtt_broker" addon.yaml; then
    echo "  ✅ Configuration schema has required fields"
else
    echo "  ❌ Missing required configuration fields"
    exit 1
fi

echo ""
echo "✅ All validations passed! Addon should appear in Home Assistant store."

fi

echo ""
echo "=== ✅ Validation complétée avec succès ==="
echo ""
echo "L'addon respecte les standards Home Assistant et peut être publié."
