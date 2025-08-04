# Play Store Deployment Guide

## Automated Deployment Options

### 1. Tag-based Release (Recommended for Alpha)
```bash
git tag v1.0.2
git push --tags
```
- Automatically deploys to **Alpha track**
- Version auto-increments
- Creates default changelog

### 2. Manual Workflow Trigger

Go to: https://github.com/murr2k/android-app-dev/actions

Select "Deploy to Play Store" → "Run workflow"

Options:
- **Release track**: 
  - `internal` - For early testing (default)
  - `alpha` - For closed testing
  - `beta` - For open testing
  - `production` - For public release
- **Submit for review**: Only for production releases

### 3. Track Progression

Recommended flow:
1. **Internal** → Test with small team
2. **Alpha** → Closed testing with selected users
3. **Beta** → Open testing (optional)
4. **Production** → Public release

## Examples

### Deploy to Alpha
```bash
# Via tag (automatic alpha)
git tag v1.0.2
git push --tags
```

### Deploy to Production
1. Go to Actions tab
2. Run workflow manually
3. Select:
   - Track: `production`
   - Submit for review: `true` (if ready for public)

### Quick Internal Test
1. Go to Actions tab
2. Run workflow with defaults (internal track)

## Version Management

- Version code: Auto-increments (34, 35, 36...)
- Version name: 
  - From tag: `v1.0.2` → version 1.0.2
  - Auto: 1.0.1 → 1.0.2 → 1.0.3

## Review Process

For production releases with review:
1. Workflow uploads AAB
2. Creates release in "completed" status
3. Google reviews (usually 2-24 hours)
4. Auto-publishes after approval

## Track-Specific Notes

### Internal Testing
- Instant availability
- Limited to internal testers list
- No review required

### Alpha/Beta Testing
- Available within 1-2 hours
- Testers must opt-in via link
- No review required

### Production
- Requires Google review (2-24 hours)
- Available to all users
- Can be phased rollout (1%, 5%, 10%...)