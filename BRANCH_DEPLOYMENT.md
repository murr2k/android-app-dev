# Branch-based Deployment

Deploy by creating branches with specific naming patterns:

## Branch Patterns

### Testing Tracks
```bash
# Deploy to internal testing
git checkout -b release/internal/fix-123
git push origin release/internal/fix-123

# Deploy to alpha testing  
git checkout -b release/alpha/v1.0.2
git push origin release/alpha/v1.0.2

# Deploy to beta testing
git checkout -b release/beta/v1.0.2
git push origin release/beta/v1.0.2
```

### Production
```bash
# Deploy to production as DRAFT (manual review needed)
git checkout -b release/production/v1.0.2
git push origin release/production/v1.0.2

# Deploy to production and AUTO-SUBMIT for review
git checkout -b release/production/v1.0.2/submit
git push origin release/production/v1.0.2/submit
```

## How It Works

1. Create a branch matching the pattern
2. Push to GitHub
3. Workflow automatically:
   - Detects the track from branch name
   - Increments version
   - Builds and deploys
   - Commits version changes back to main

## Examples in github.dev

1. Open github.dev
2. Create new branch:
   - Click branch dropdown
   - Type: `release/alpha/v1.0.2`
   - Create branch
3. Make any changes (optional)
4. Commit and push
5. Deployment starts automatically!

## Version in Branch Name

Include version in branch name (optional):
- `release/alpha/v1.0.2` → Uses version 1.0.2
- `release/alpha/new-feature` → Auto-increments version

## Benefits

- ✅ Works in github.dev, VS Code, any editor
- ✅ No manual workflow triggers needed
- ✅ Track visible in branch name
- ✅ Can review changes before deploy
- ✅ Branch history shows all deployments