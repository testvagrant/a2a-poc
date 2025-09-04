#!/bin/bash

# UTA Real Agent Setup Script
# This script helps set up real chatbot agents for testing with UTA

echo "🤖 UTA Real Agent Setup Script"
echo "================================"

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install Ollama
install_ollama() {
    echo "📦 Installing Ollama..."
    
    if command_exists ollama; then
        echo "✅ Ollama is already installed"
    else
        echo "⬇️ Downloading and installing Ollama..."
        curl -fsSL https://ollama.ai/install.sh | sh
        
        if [ $? -eq 0 ]; then
            echo "✅ Ollama installed successfully"
        else
            echo "❌ Failed to install Ollama"
            return 1
        fi
    fi
    
    # Start Ollama server
    echo "🚀 Starting Ollama server..."
    ollama serve &
    OLLAMA_PID=$!
    echo "✅ Ollama server started (PID: $OLLAMA_PID)"
    
    # Wait for server to start
    sleep 5
    
    # Pull a model
    echo "📥 Pulling Llama2 model..."
    ollama pull llama2
    
    if [ $? -eq 0 ]; then
        echo "✅ Llama2 model pulled successfully"
    else
        echo "❌ Failed to pull Llama2 model"
        return 1
    fi
    
    echo "🎉 Ollama setup complete!"
    echo "   Server running on: http://localhost:11434"
    echo "   Available models: $(ollama list | grep -v 'NAME' | awk '{print $1}' | tr '\n' ' ')"
}

# Function to test Ollama integration
test_ollama() {
    echo "🧪 Testing Ollama integration..."
    
    if command_exists ollama; then
        # Check if server is running
        if curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
            echo "✅ Ollama server is running"
            
            # Test with UTA
            echo "🔄 Testing with UTA..."
            python3 examples/ollama_integration.py
            
            if [ $? -eq 0 ]; then
                echo "✅ Ollama integration test passed!"
            else
                echo "❌ Ollama integration test failed"
            fi
        else
            echo "❌ Ollama server is not running"
            echo "   Please start it with: ollama serve"
        fi
    else
        echo "❌ Ollama is not installed"
    fi
}

# Function to test HuggingChat integration
test_huggingchat() {
    echo "🧪 Testing HuggingChat integration..."
    
    # Check internet connectivity
    if curl -s https://huggingface.co >/dev/null 2>&1; then
        echo "✅ HuggingChat is accessible"
        
        # Test with UTA
        echo "🔄 Testing with UTA..."
        python3 examples/huggingchat_integration.py
        
        if [ $? -eq 0 ]; then
            echo "✅ HuggingChat integration test passed!"
        else
            echo "❌ HuggingChat integration test failed"
        fi
    else
        echo "❌ HuggingChat is not accessible (check internet connection)"
    fi
}

# Function to run UTA tests with real agents
run_uta_tests() {
    echo "🚀 Running UTA tests with real agents..."
    
    # Test with Ollama
    if curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
        echo "📊 Testing core scenarios with Ollama..."
        python3 -m runner.run --suite scenarios/core --report out_ollama_test --http-url http://localhost:11434/api/generate --seed 42
        
        if [ $? -eq 0 ]; then
            echo "✅ Ollama UTA test completed successfully!"
            echo "   Report available at: out_ollama_test/report.html"
        else
            echo "❌ Ollama UTA test failed"
        fi
    else
        echo "⚠️ Ollama server not running, skipping Ollama tests"
    fi
    
    # Test with HuggingChat
    if curl -s https://huggingface.co >/dev/null 2>&1; then
        echo "📊 Testing core scenarios with HuggingChat..."
        python3 -m runner.run --suite scenarios/core --report out_huggingchat_test --http-url https://huggingface.co/chat/api --seed 42
        
        if [ $? -eq 0 ]; then
            echo "✅ HuggingChat UTA test completed successfully!"
            echo "   Report available at: out_huggingchat_test/report.html"
        else
            echo "❌ HuggingChat UTA test failed"
        fi
    else
        echo "⚠️ HuggingChat not accessible, skipping HuggingChat tests"
    fi
}

# Main menu
show_menu() {
    echo ""
    echo "🎯 What would you like to do?"
    echo "1. Install and setup Ollama"
    echo "2. Test Ollama integration"
    echo "3. Test HuggingChat integration"
    echo "4. Run UTA tests with real agents"
    echo "5. Run all tests"
    echo "6. Exit"
    echo ""
    read -p "Enter your choice (1-6): " choice
    
    case $choice in
        1)
            install_ollama
            ;;
        2)
            test_ollama
            ;;
        3)
            test_huggingchat
            ;;
        4)
            run_uta_tests
            ;;
        5)
            install_ollama
            test_ollama
            test_huggingchat
            run_uta_tests
            ;;
        6)
            echo "👋 Goodbye!"
            exit 0
            ;;
        *)
            echo "❌ Invalid choice. Please try again."
            show_menu
            ;;
    esac
}

# Check if running in interactive mode
if [ $# -eq 0 ]; then
    show_menu
else
    case $1 in
        "install")
            install_ollama
            ;;
        "test-ollama")
            test_ollama
            ;;
        "test-huggingchat")
            test_huggingchat
            ;;
        "run-tests")
            run_uta_tests
            ;;
        "all")
            install_ollama
            test_ollama
            test_huggingchat
            run_uta_tests
            ;;
        *)
            echo "Usage: $0 [install|test-ollama|test-huggingchat|run-tests|all]"
            echo "Or run without arguments for interactive menu"
            exit 1
            ;;
    esac
fi

