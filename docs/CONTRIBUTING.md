# Contributing Guide

Thank you for your interest in contributing to macOS AI Commander! This guide will help you get started.

## 🎯 Ways to Contribute

### 1. **Add New Tools**
Expand the tool library with new macOS automation capabilities.

### 2. **Improve Documentation**
Help others understand and use the system better.

### 3. **Fix Bugs**
Identify and resolve issues in the codebase.

### 4. **Enhance UI/UX**
Improve the web interface or CLI experience.

### 5. **Optimize Performance**
Make the system faster and more efficient.

### 6. **Write Tests**
Increase code coverage and reliability.

## 🚀 Getting Started

### Step 1: Fork & Clone

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/your-repo-name.git
cd your-repo-name

# Add upstream remote
git remote add upstream https://github.com/ORIGINAL_OWNER/your-repo-name.git
```

### Step 2: Set Up Development Environment

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies (if any)
pip install pytest black flake8 mypy
```

### Step 3: Create a Branch

```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/bug-description
```

## 📝 Development Guidelines

### Code Style

**Python Style Guide**: Follow PEP 8

```python
# Good ✅
def snap_window_left(app_name: str, screen_id: int = 0) -> dict:
    """
    Snap window to left half of screen.
    
    Args:
        app_name: Name of application
        screen_id: Which screen (default: 0)
        
    Returns:
        dict with success status and message
    """
    try:
        result = execute_snap(app_name, "left")
        return {"success": True, "result": result}
    except Exception as e:
        return {"success": False, "error": str(e)}


# Bad ❌
def snapWindowLeft(appName):
    result=execute_snap(appName,"left")
    return result
```

**Formatting**:
```bash
# Format code with black
black your_file.py

# Check linting
flake8 your_file.py

# Type checking
mypy your_file.py
```

### Tool Development

#### Creating a New Tool

**1. Choose the Right Module**

Place your tool in the appropriate category:
- `tools/window_management.py` - Window operations
- `tools/file_operations.py` - File system operations
- `tools/web_tools.py` - Web and network operations
- `tools/system_tools.py` - System control
- Or create a new module if needed

**2. Implement the Function**

```python
# tools/your_module.py

def your_tool_name(param1: str, param2: int = 10) -> dict:
    """
    Brief description of what the tool does.
    
    This tool performs [specific action] on macOS by using
    [technology/API]. It's useful for [use case].
    
    Args:
        param1: Description of first parameter
        param2: Description with default value (default: 10)
        
    Returns:
        dict: Contains the following keys:
            - success (bool): Whether operation succeeded
            - result: The actual result data
            - message (str): Human-readable status message
            - error (str, optional): Error message if failed
            
    Example:
        >>> your_tool_name("test", 20)
        {"success": True, "result": "...", "message": "Done!"}
    """
    try:
        # Input validation
        if not param1:
            raise ValueError("param1 cannot be empty")
            
        if param2 < 0:
            raise ValueError("param2 must be positive")
        
        # Your implementation here
        result = perform_operation(param1, param2)
        
        # Return success response
        return {
            "success": True,
            "result": result,
            "message": f"Successfully processed {param1}"
        }
        
    except ValueError as e:
        # Handle validation errors
        return {
            "success": False,
            "error": f"Invalid input: {str(e)}"
        }
        
    except Exception as e:
        # Handle unexpected errors
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}"
        }
```

**3. Register in Tool Registry**

```python
# tools/advanced_tool_registry.py

from tools.your_module import your_tool_name

ADVANCED_TOOLS = {
    # ... existing tools ...
    
    "your_tool_name": {
        "description": "Brief description for AI (be clear and specific)",
        "parameters": {
            "type": "object",
            "properties": {
                "param1": {
                    "type": "string",
                    "description": "What this parameter does"
                },
                "param2": {
                    "type": "integer",
                    "description": "What this parameter does"
                }
            },
            "required": ["param1"]  # Only list truly required params
        },
        "function": your_tool_name
    }
}
```

**4. Add to Config (Optional)**

```json
// config.json
{
  "tools": {
    "enabled": [
      "your_tool_name"
    ]
  }
}
```

**5. Test Your Tool**

```python
# Test manually
from tools.your_module import your_tool_name

result = your_tool_name("test", 20)
print(result)

# Test with AI
python start_cli.py
> "Use your_tool_name with test parameter"
```

#### Tool Best Practices

**✅ Do:**
- Return consistent dict format
- Handle all exceptions
- Validate inputs
- Provide clear error messages
- Document parameters thoroughly
- Use type hints
- Test edge cases
- Keep functions focused (single responsibility)
- Use descriptive parameter names
- Include usage examples in docstring

**❌ Don't:**
- Return different types (always dict)
- Let exceptions bubble up
- Assume inputs are valid
- Use generic error messages
- Leave parameters undocumented
- Skip type hints
- Create multi-purpose functions
- Use cryptic parameter names
- Forget about edge cases

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```bash
# Feature
git commit -m "feat: add window tiling tool for grid layouts"

# Bug fix
git commit -m "fix: resolve clipboard history memory leak"

# Documentation
git commit -m "docs: update ARCHITECTURE.md with voice flow"

# Performance
git commit -m "perf: optimize tool registry loading time"

# Refactor
git commit -m "refactor: simplify window management code"

# Style
git commit -m "style: format web_tools.py with black"

# Test
git commit -m "test: add unit tests for file operations"
```

**Format**:
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `perf`: Performance improvement
- `test`: Tests
- `chore`: Maintenance

### Testing

#### Manual Testing Checklist

Before submitting a PR, test:

- [ ] Tool executes without errors
- [ ] Error handling works correctly
- [ ] Parameters validate properly
- [ ] Return format is consistent
- [ ] AI can understand and use the tool
- [ ] Documentation is clear
- [ ] No breaking changes to existing tools
- [ ] Works on latest macOS version

#### Unit Tests (Recommended)

```python
# tests/test_your_module.py

import pytest
from tools.your_module import your_tool_name


def test_your_tool_success():
    """Test successful execution"""
    result = your_tool_name("valid_input", 10)
    assert result["success"] is True
    assert "result" in result
    

def test_your_tool_invalid_input():
    """Test error handling"""
    result = your_tool_name("", 10)
    assert result["success"] is False
    assert "error" in result
    

def test_your_tool_default_params():
    """Test default parameter values"""
    result = your_tool_name("test")
    assert result["success"] is True
```

Run tests:
```bash
pytest tests/
```

## 📤 Submitting Changes

### Step 1: Update Your Branch

```bash
# Fetch latest changes
git fetch upstream

# Rebase on main
git rebase upstream/main

# Resolve any conflicts
```

### Step 2: Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### Step 3: Create Pull Request

1. Go to your fork on GitHub
2. Click "New Pull Request"
3. Fill out the PR template

**PR Title Format**:
```
[Type] Brief description

Examples:
[Feature] Add window grid tiling tool
[Fix] Resolve clipboard history crash
[Docs] Update tool development guide
```

**PR Description Template**:
```markdown
## What does this PR do?
Brief description of changes

## Why is this needed?
Explanation of the problem or use case

## How was it tested?
- [ ] Manual testing
- [ ] Unit tests added/updated
- [ ] Tested on macOS [version]

## Screenshots (if applicable)
[Add screenshots or GIFs]

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Tests pass
- [ ] No breaking changes (or documented)
- [ ] Commit messages follow convention
```

## 🔍 Code Review Process

### What Reviewers Look For

1. **Functionality**: Does it work as intended?
2. **Code Quality**: Is it clean and maintainable?
3. **Documentation**: Is it well-documented?
4. **Testing**: Is it adequately tested?
5. **Performance**: Is it efficient?
6. **Security**: Are there any security concerns?

### Addressing Feedback

```bash
# Make requested changes
# Commit changes
git commit -m "refactor: address review feedback"

# Push updates
git push origin feature/your-feature-name
```

The PR will update automatically.

## 📚 Documentation

### When to Update Docs

Update documentation when you:
- Add new tools
- Change existing behavior
- Add new features
- Fix bugs that weren't documented

### Which Files to Update

- `docs/README.md` - If changing setup/overview
- `docs/GETTING_STARTED.md` - If changing installation
- `docs/EXAMPLES.md` - Add examples for new tools
- `docs/ARCHITECTURE.md` - If changing architecture
- `README.md` - Major features only
- Inline code comments - Always

## 🐛 Reporting Bugs

### Bug Report Template

```markdown
## Bug Description
Clear description of what's wrong

## Steps to Reproduce
1. Start the application
2. Execute command "..."
3. See error

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- macOS version: 
- Python version:
- Ollama version:
- Model:

## Error Output
```
Paste error messages or logs here
```

## Additional Context
Any other relevant information
```

## 💡 Feature Requests

### Feature Request Template

```markdown
## Feature Description
Clear description of the feature

## Use Case
Why is this needed? What problem does it solve?

## Proposed Solution
How should it work?

## Alternatives Considered
Other approaches you've thought about

## Additional Context
Mockups, examples, references
```

## 🏆 Recognition

Contributors will be:
- Listed in `CONTRIBUTORS.md`
- Mentioned in release notes
- Credited in the project

## 📞 Getting Help

- **Questions**: Open a GitHub Discussion
- **Issues**: Open a GitHub Issue
- **Chat**: iamsid0011@gmail.com


## 📜 License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT).

---

**Thank you for contributing!** Every contribution, big or small, makes a difference. 🚀

