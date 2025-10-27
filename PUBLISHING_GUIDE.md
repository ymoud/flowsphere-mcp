# Publishing Guide for FlowSphere MCP Server

This guide covers all options for distributing your MCP server to users.

## 🎯 Publishing Options Comparison

| Option | Installation Command | Discovery | Updates | Best For |
|--------|---------------------|-----------|---------|----------|
| **Smithery** | `npx @smithery/cli install flowsphere` | ✅ Excellent | ✅ Auto | MCP-specific distribution |
| **PyPI** | `pip install flowsphere-mcp-server` | ✅ Good | ✅ Manual | Python developers |
| **GitHub** | Clone + run | ❌ Limited | ❌ Manual | Current state |
| **Docker** | `docker run flowsphere-mcp` | ⚠️ Medium | ✅ Auto | Containerized environments |

---

## Option 1: Smithery (Recommended for MCP Servers)

**Smithery** is Anthropic's official MCP server registry.

### Why Smithery?
- ✅ Official Anthropic platform
- ✅ Users discover your server easily
- ✅ One-command installation
- ✅ Automatic Claude Desktop configuration
- ✅ Version management

### Steps to Publish on Smithery:

1. **Create `smithery.json` in your repo root:**

```json
{
  "name": "flowsphere-mcp-server",
  "version": "1.0.0",
  "description": "Generate production-ready test code (Python pytest/behave, JavaScript Jest) from FlowSphere configurations. Supports all 18 FlowSphere features.",
  "author": "Your Name",
  "homepage": "https://github.com/yourusername/flowsphere-mcp-server",
  "repository": {
    "type": "git",
    "url": "https://github.com/yourusername/flowsphere-mcp-server.git"
  },
  "license": "MIT",
  "tags": [
    "testing",
    "code-generation",
    "api-testing",
    "pytest",
    "jest",
    "behave",
    "bdd",
    "flowsphere"
  ],
  "runtime": "python",
  "command": "python",
  "args": ["src/flowsphere_mcp/server.py"],
  "tools": [
    {
      "name": "get_flowsphere_schema",
      "description": "Get complete FlowSphere configuration schema documentation"
    },
    {
      "name": "get_flowsphere_features",
      "description": "Get detailed documentation of all 18 FlowSphere features"
    },
    {
      "name": "get_feature_checklist",
      "description": "Get a checklist of all features that must be implemented"
    },
    {
      "name": "generate_python_pytest",
      "description": "Generate production-ready Python pytest code from FlowSphere config"
    },
    {
      "name": "generate_python_behave",
      "description": "Generate Python behave/BDD tests with Gherkin features"
    },
    {
      "name": "generate_javascript_jest",
      "description": "Generate JavaScript Jest tests with async/await"
    }
  ]
}
```

2. **Ensure your repo is public on GitHub**

3. **Test locally first:**
```bash
# Test your server works
python src/flowsphere_mcp/server.py

# Run all tests
pytest tests/ -v
```

4. **Submit to Smithery:**
   - Visit https://smithery.ai
   - Click "Submit Server"
   - Provide your GitHub repository URL
   - Wait for approval (usually 1-2 days)

5. **Users can then install:**
```bash
# Install via Smithery CLI
npx @smithery/cli install flowsphere-mcp-server

# Or add to Claude Desktop manually
# Smithery provides the config snippet
```

---

## Option 2: PyPI (Python Package Index)

Make your server installable via `pip`.

### Preparation

Files already created:
- ✅ `setup.py` - Package configuration
- ✅ `MANIFEST.in` - Include templates and docs
- ✅ `requirements.txt` - Dependencies

### Steps to Publish on PyPI:

1. **Update `setup.py` with your details:**
```python
# Edit setup.py:
author="Your Name",
author_email="your.email@example.com",
url="https://github.com/yourusername/flowsphere-mcp-server",
```

2. **Create PyPI account:**
   - Go to https://pypi.org
   - Create account
   - Verify email
   - Enable 2FA (required)

3. **Install build tools:**
```bash
pip install build twine
```

4. **Build the package:**
```bash
# Clean old builds
rm -rf dist/ build/ *.egg-info

# Build source and wheel distributions
python -m build
```

5. **Test on TestPyPI first (optional but recommended):**
```bash
# Upload to TestPyPI
python -m twine upload --repository testpypi dist/*

# Test installation
pip install --index-url https://test.pypi.org/simple/ flowsphere-mcp-server
```

6. **Upload to PyPI:**
```bash
python -m twine upload dist/*
```

7. **Users can then install:**
```bash
# Install from PyPI
pip install flowsphere-mcp-server

# Run the server
flowsphere-mcp
# or
python -m flowsphere_mcp.server
```

### Updating Your Package

When you make changes:

1. Update version in `setup.py`
2. Rebuild: `python -m build`
3. Upload: `python -m twine upload dist/*`

---

## Option 3: GitHub Releases (Current State)

Best for: Early access, beta testing, or if you don't want to maintain on registries.

### Steps:

1. **Create a release on GitHub:**
```bash
# Tag your version
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

2. **Create release on GitHub:**
   - Go to your repo → Releases → Create new release
   - Select tag `v1.0.0`
   - Title: "FlowSphere MCP Server v1.0.0"
   - Description: Copy from your commit messages
   - Attach files (optional): ZIP of source code

3. **Users install by cloning:**
```bash
# Clone the repo
git clone https://github.com/yourusername/flowsphere-mcp-server.git
cd flowsphere-mcp-server

# Install dependencies
pip install -r requirements.txt

# Run the server
python src/flowsphere_mcp/server.py
```

4. **Update README with installation instructions**

---

## Option 4: Docker Container (Advanced)

For users who prefer containers.

### Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/
COPY tests/ ./tests/

# Run server
CMD ["python", "src/flowsphere_mcp/server.py"]
```

### Publish to Docker Hub:

```bash
# Build image
docker build -t yourusername/flowsphere-mcp-server:1.0.0 .

# Test locally
docker run -it yourusername/flowsphere-mcp-server:1.0.0

# Push to Docker Hub
docker login
docker push yourusername/flowsphere-mcp-server:1.0.0
```

### Users install:
```bash
docker pull yourusername/flowsphere-mcp-server:1.0.0
docker run -it yourusername/flowsphere-mcp-server:1.0.0
```

---

## Recommended Approach: Multi-Platform

**Best practice:** Publish on multiple platforms for maximum reach.

### Suggested order:

1. **Start with GitHub** (you're already here)
   - Create good README ✅
   - Add examples ✅
   - Create releases
   - Get initial users

2. **Add PyPI** (for Python developers)
   - Easy `pip install`
   - Version management
   - Wide Python community reach

3. **Submit to Smithery** (for MCP users)
   - Best MCP-specific discovery
   - Automatic Claude Desktop integration
   - Official Anthropic platform

4. **Optional: Docker** (for enterprise users)
   - Isolated environments
   - Easy deployment
   - Cloud-friendly

---

## Pre-Publishing Checklist

Before publishing anywhere:

- [ ] All tests passing (98/98 ✅)
- [ ] README is comprehensive ✅
- [ ] LICENSE file exists ✅
- [ ] Version number is correct
- [ ] Author info is updated
- [ ] No sensitive data in code
- [ ] Examples work
- [ ] Documentation is clear
- [ ] GitHub repo is public
- [ ] Release notes written

---

## After Publishing

### 1. Announce it!
- Social media (Twitter, LinkedIn)
- Reddit (r/Python, r/programming, r/Claude)
- Dev.to blog post
- Hacker News

### 2. Monitor usage
- GitHub stars/forks
- PyPI download stats
- Smithery usage metrics
- Issue reports

### 3. Maintain
- Respond to issues
- Review PRs
- Keep dependencies updated
- Add new features (TypeScript, C#)

---

## Next Steps

**Quick start (choose one):**

1. **Just want it on GitHub?**
   ```bash
   git tag -a v1.0.0 -m "Release v1.0.0"
   git push origin v1.0.0
   # Create release on GitHub web interface
   ```

2. **Want pip install?**
   ```bash
   # Update setup.py with your info
   python -m build
   python -m twine upload dist/*
   ```

3. **Want Smithery discovery?**
   - Create `smithery.json` (see above)
   - Submit at https://smithery.ai
   - Wait for approval

---

## Resources

- **Smithery:** https://smithery.ai
- **PyPI:** https://pypi.org
- **Python Packaging Guide:** https://packaging.python.org
- **MCP Documentation:** https://modelcontextprotocol.io
- **GitHub Releases:** https://docs.github.com/en/repositories/releasing-projects-on-github

---

## Support

Need help publishing? Check:
- MCP Discord community
- Python Packaging Discord
- Stack Overflow
- GitHub Discussions
