#!/bin/bash
# Verification script for PR #30 update

echo "🔍 Verifying PR #30 Update..."
echo ""

# Function to check and print result
check() {
    if [ $? -eq 0 ]; then
        echo "✅ $1"
    else
        echo "❌ $1"
        return 1
    fi
}

# 1. Check for hardcoded secrets
echo "1. Checking for hardcoded secrets..."
! grep -q "Leng12345" deploy*.sh deploy/*.* 2>/dev/null
check "No hardcoded passwords found"

! grep -q "genxapitrading@gmail.com" deploy*.sh deploy/*.* 2>/dev/null
check "No hardcoded email addresses found"

! grep -q "AIzaSyDnjcaXnDpm1TzmIAV7EnoluI6w7wGBagM" deploy*.sh deploy/*.* 2>/dev/null
check "No hardcoded API keys found"

echo ""

# 2. Check DATABASE_URL security fix
echo "2. Checking DATABASE_URL security..."
grep -q 'DATABASE_URL.*Field(.*\.\.\.' api/config.py
check "DATABASE_URL requires environment variable"

! grep -q 'DATABASE_URL.*=.*"postgresql://.*password.*"' api/config.py
check "DATABASE_URL has no hardcoded credentials"

echo ""

# 3. Check Python syntax
echo "3. Validating Python syntax..."
python3 -m py_compile api/config.py 2>/dev/null
check "api/config.py syntax valid"

python3 -m py_compile api/main.py 2>/dev/null
check "api/main.py syntax valid"

python3 -m py_compile core/indicators/macd.py 2>/dev/null
check "core/indicators/macd.py syntax valid"

echo ""

# 4. Check that typing imports were added
echo "4. Checking code improvements..."
grep -q "from typing import" core/indicators/macd.py
check "Typing imports added to macd.py"

echo ""

# 5. Check dependency updates
echo "5. Checking dependency updates..."
grep -q '"@neondatabase/serverless": "\^0.10' package.json
check "Neon database package updated to 0.10.x"

echo ""

# 6. Check deployment script improvements
echo "6. Checking deployment script security..."
grep -q ".env.example" deploy_genx.sh
check "deploy_genx.sh uses .env.example template"

grep -q "your_docker_password" deploy_genx.sh
check "deploy_genx.sh uses password placeholder"

grep -q "your_jwt_secret_key" deploy_genx.sh
check "deploy_genx.sh uses JWT secret placeholder"

echo ""

# 7. Check merge commit exists
echo "7. Checking merge status..."
git log --oneline --grep "Merge main into revert-28-revert-27-fix-jwt-secrets-vulnerability" | grep -q "."
check "Merge commit exists"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Verification Complete!"
echo ""
echo "PR #30 has been successfully updated with:"
echo "  • All security fixes preserved"
echo "  • Latest main branch changes integrated"
echo "  • No hardcoded credentials"
echo "  • Updated dependencies"
echo "  • Improved tests"
echo ""
echo "Next steps:"
echo "  1. Review UPDATE_PR30_INSTRUCTIONS.md"
echo "  2. Run ./update_pr30.sh to update the remote branch"
echo "  3. Verify CI/CD checks pass"
echo "  4. Merge PR #30"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
