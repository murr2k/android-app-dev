# Automatic Version Management

## How It Works

1. **Version Storage**: Versions are stored in `version.properties`:
   ```properties
   versionCode=33
   versionName=1.0.1
   ```

2. **Auto-Increment Logic**:
   - Version code: Always increments by 1 (33 → 34 → 35...)
   - Version name: 
     - If you use a tag like `v1.0.2`, it uses that version
     - Otherwise, it auto-increments the patch version (1.0.1 → 1.0.2)

3. **Automatic Changelog**: Creates a default changelog if none exists

4. **Auto-Commit**: After successful deployment, commits the new version back to the repo

## Usage

### Option 1: Tag with specific version
```bash
git tag v1.0.2
git push --tags
```
This will deploy version 1.0.2 with version code 34

### Option 2: Manual trigger (auto-increment)
- Go to Actions tab → "Deploy to Play Store" → "Run workflow"
- This will auto-increment: 1.0.1 → 1.0.2

### Option 3: Edit changelog before release
```bash
# Create changelog for next version (34)
echo "Version 1.0.2 (34)

• New feature X
• Fixed bug Y
• Improved performance" > fastlane/metadata/android/en-US/changelogs/34.txt

# Commit and deploy
git add fastlane/metadata/android/en-US/changelogs/34.txt
git commit -m "Add changelog for v1.0.2"
git push
git tag v1.0.2
git push --tags
```

## Benefits

- ✅ No manual version editing
- ✅ Version history tracked in git
- ✅ Automatic changelog creation
- ✅ Version code always increments (no Play Store errors)
- ✅ Version name can be controlled via tags

## Version File Location

The `version.properties` file is in the root of your repo, making it easy to check current version:
```bash
cat version.properties
```