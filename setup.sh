#!/bin/bash

# Jekyll Cybersecurity Blog Setup Script
# This script sets up the complete automated Jekyll blog project

set -e

echo "🚀 Setting up Jekyll Cybersecurity Blog..."
echo "======================================="

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Error: This script must be run in a git repository"
    echo "Please run: git init"
    exit 1
fi

# Create directory structure
echo "📁 Creating directory structure..."
mkdir -p _posts
mkdir -p blog
mkdir -p .github/workflows

# Create _posts directory with a placeholder if empty
if [ ! "$(ls -A _posts)" ]; then
    echo "📝 _posts directory is empty - will be populated automatically"
fi

# Create blog directory if it doesn't exist
if [ ! -f "blog/index.html" ]; then
    echo "📄 Blog index.html will be created"
fi

# Install Ruby dependencies if Gemfile exists
if [ -f "Gemfile" ]; then
    echo "💎 Installing Ruby dependencies..."
    if command -v bundle &> /dev/null; then
        bundle install
        echo "✅ Ruby dependencies installed"
    else
        echo "⚠️  Bundler not found. Install with: gem install bundler"
        echo "   Then run: bundle install"
    fi
fi

# Install Python dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "🐍 Installing Python dependencies..."
    if command -v pip &> /dev/null; then
        pip install -r requirements.txt
        echo "✅ Python dependencies installed"
    else
        echo "⚠️  pip not found. Please install Python and pip first"
    fi
fi

# Set up git configuration for the project
echo "🔧 Setting up git configuration..."
git config user.name "Blog Generator" 2>/dev/null || true
git config user.email "blog@adamrivers.com" 2>/dev/null || true

# Test content generation script
if [ -f "generate_content.py" ]; then
    echo "🧪 Testing content generation script..."
    if command -v python &> /dev/null; then
        echo "Python found, content generator is ready"
    elif command -v python3 &> /dev/null; then
        echo "Python3 found, content generator is ready"
    else
        echo "⚠️  Python not found. Install Python to use automated content generation"
    fi
fi

# Check for GitHub CLI
if command -v gh &> /dev/null; then
    echo "🐙 GitHub CLI detected"
    echo "You can use 'gh repo create' to create a new repository"
else
    echo "💡 Consider installing GitHub CLI for easier repository management"
fi

# Add all files to git
echo "📦 Adding files to git..."
git add .

# Create initial commit if no commits exist
if ! git log --oneline -n 1 &> /dev/null; then
    echo "🎯 Creating initial commit..."
    git commit -m "Initial setup: Jekyll cybersecurity blog with automated content generation"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "🔥 Next Steps:"
echo "1. Update _config.yml with your information"
echo "2. Customize generate_content.py with your expertise"
echo "3. Push to GitHub: git push origin main"
echo "4. Enable GitHub Pages in repository settings"
echo "5. Your blog will be available at: https://yourusername.github.io"
echo ""
echo "🤖 The automated workflow will:"
echo "- Generate new blog posts daily at 1 AM UTC"
echo "- Build and deploy your Jekyll site automatically"
echo "- Keep your blog updated with fresh cybersecurity content"
echo ""
echo "📚 Documentation:"
echo "- Jekyll: https://jekyllrb.com/docs/"
echo "- GitHub Pages: https://docs.github.com/en/pages"
echo "- GitHub Actions: https://docs.github.com/en/actions"
echo ""
echo "🚀 Happy blogging!"
