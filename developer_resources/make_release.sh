# Release script for py-bugger.
# 
# To make a new release:
# - Update changelog
# - Bump version
# - Push to main
# - Tag release: git tag vA.B.C, git push origin vA.B.C
# - Run this script from the project root:
#   $ ./developer_resources/make_release.sh

echo "\nMaking a new release of py-bugger..."

echo "  Working directory:"
pwd

# Remove previous build, and build new version.
rm -rf dist/
python -m build

# Push to PyPI.
python -m twine upload dist/*

# Open PyPI page in browser to verify push was successful.
open "https://pypi.org/project/python-bugger/"