#!/bin/bash
# Script to update PR #30 branch with the merged changes

set -e

echo "🔄 Updating PR #30 branch..."

# Check if we're in a git repository
if [ ! -d .git ]; then
    echo "❌ Error: Not in a git repository"
    exit 1
fi

# Fetch latest changes
echo "📥 Fetching latest changes..."
git fetch origin

# Get the merge commit from our working branch
MERGE_COMMIT="7aac67b"

# Check if the merge commit exists
if ! git cat-file -e "$MERGE_COMMIT" 2>/dev/null; then
    echo "❌ Error: Merge commit $MERGE_COMMIT not found"
    echo "   Fetching from copilot/update-branch-30..."
    git fetch origin copilot/update-branch-30
fi

# Option to choose update method
echo ""
echo "Choose update method:"
echo "1. Force push the merged branch (recommended)"
echo "2. Cherry-pick the merge commit"
echo "3. Cancel"
read -p "Enter choice (1-3): " choice

case $choice in
    1)
        echo "🔄 Force pushing merged branch..."
        git push origin "$MERGE_COMMIT:refs/heads/revert-28-revert-27-fix-jwt-secrets-vulnerability" --force-with-lease
        echo "✅ Branch updated successfully!"
        ;;
    2)
        echo "🍒 Cherry-picking merge commit..."
        git checkout revert-28-revert-27-fix-jwt-secrets-vulnerability
        git cherry-pick "$MERGE_COMMIT"
        git push origin revert-28-revert-27-fix-jwt-secrets-vulnerability
        echo "✅ Branch updated successfully!"
        ;;
    3)
        echo "❌ Update cancelled"
        exit 0
        ;;
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "📝 Next steps:"
echo "1. Go to https://github.com/Mouy-leng/GenX_FX_0/pull/30"
echo "2. Verify the PR shows as updated"
echo "3. Check that all CI/CD checks pass"
echo "4. Review and merge the PR"
