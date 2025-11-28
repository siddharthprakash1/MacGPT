#!/bin/bash

# MacGPT Installer
# One-liner: curl -fsSL https://raw.githubusercontent.com/siddharthprakash1/MacGPT/main/install.sh | bash

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo ""
echo -e "${BLUE}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║${NC}           ${GREEN}🤖 MacGPT Installer${NC}                            ${BLUE}║${NC}"
echo -e "${BLUE}║${NC}           AI Assistant for macOS                         ${BLUE}║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo -e "${RED}❌ Error: MacGPT only works on macOS${NC}"
    exit 1
fi

# Check for Ollama
echo -e "${YELLOW}📋 Checking prerequisites...${NC}"

if ! command -v ollama &> /dev/null; then
    echo -e "${RED}❌ Ollama not found!${NC}"
    echo ""
    echo "Please install Ollama first:"
    echo -e "${GREEN}  curl -fsSL https://ollama.com/install.sh | sh${NC}"
    echo ""
    echo "Then run this installer again."
    exit 1
fi
echo -e "${GREEN}  ✓ Ollama installed${NC}"

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found!${NC}"
    echo "Please install Python 3.9+ from https://python.org"
    exit 1
fi
echo -e "${GREEN}  ✓ Python 3 installed${NC}"

# Set install directory
INSTALL_DIR="$HOME/.macgpt"

# Clone or update repository
echo ""
echo -e "${YELLOW}📦 Installing MacGPT...${NC}"

if [ -d "$INSTALL_DIR" ]; then
    echo "  Updating existing installation..."
    cd "$INSTALL_DIR"
    git pull --quiet
else
    echo "  Cloning repository..."
    git clone --quiet https://github.com/siddharthprakash1/MacGPT.git "$INSTALL_DIR"
    cd "$INSTALL_DIR"
fi

# Create virtual environment
echo -e "${YELLOW}🐍 Setting up Python environment...${NC}"
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate

# Install dependencies
echo "  Installing dependencies..."
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt

# Pull default model if not exists
echo ""
echo -e "${YELLOW}🧠 Checking Ollama model...${NC}"
if ! ollama list | grep -q "mistral"; then
    echo "  Pulling mistral model (this may take a few minutes)..."
    ollama pull mistral
else
    echo -e "${GREEN}  ✓ Model ready${NC}"
fi

# Create launch script
echo ""
echo -e "${YELLOW}🔧 Creating launch command...${NC}"

LAUNCH_SCRIPT="/usr/local/bin/macgpt"
sudo mkdir -p /usr/local/bin

sudo tee "$LAUNCH_SCRIPT" > /dev/null << 'EOF'
#!/bin/bash
cd "$HOME/.macgpt"
source venv/bin/activate
python start_web.py
EOF

sudo chmod +x "$LAUNCH_SCRIPT"
echo -e "${GREEN}  ✓ Command 'macgpt' created${NC}"

# Done!
echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║${NC}           ${GREEN}✅ Installation Complete!${NC}                       ${GREEN}║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "  To start MacGPT, run:"
echo -e "    ${BLUE}macgpt${NC}"
echo ""
echo -e "  Or manually:"
echo -e "    ${BLUE}cd ~/.macgpt && source venv/bin/activate && python start_web.py${NC}"
echo ""
echo -e "  Then open: ${BLUE}http://localhost:7889${NC}"
echo ""
echo -e "${YELLOW}💡 Tip: Grant Accessibility permissions when prompted for full functionality${NC}"
echo ""

