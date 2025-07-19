# JudgmentLabs MCP Server

A Model Context Protocol (MCP) server that provides seamless integration with the Judgment API for AI evaluation workflows. This server enables you to manage datasets, run evaluations, and track traces directly from your MCP-compatible environment like Claude Desktop.

## 🚀 Features

### 🎯 One-Click Installation
- **DXT Package**: Install as a single `.dxt` file in Claude Desktop
- **No Dependencies**: All Python packages are pre-bundled
- **Auto-Configuration**: Easy setup through Claude Desktop's settings UI
- **Cross-Platform**: Works on Windows, macOS, and Linux

### 📊 Dataset Management
- **Create & Manage Datasets**: Push datasets with examples and traces to the Judgment API
- **Flexible Data Handling**: Support for append and overwrite modes when updating datasets
- **Data Retrieval**: Pull existing datasets from your Judgment projects
- **Smart Example Conversion**: Automatically handles various input formats (input/question, expected_output/answer)

### Project Operations
- **Project Creation**: Create new projects in the Judgment API
- **Project Cleanup**: Delete projects and all associated data
- **Auto-Creation**: Projects are automatically created when pushing datasets if they don't exist

### Evaluation & Monitoring
- **Run Evaluations**: Execute evaluation runs via the Judgment API
- **Results Retrieval**: Fetch detailed evaluation results for analysis
- **Trace Management**: Create, fetch, and delete individual traces
- **Real-time Monitoring**: Track AI agent performance and behavior

### Developer Experience
- **Error Handling**: Comprehensive error handling with helpful suggestions
- **Debug Logging**: Built-in debugging capabilities for troubleshooting
- **Flexible Configuration**: Environment-based configuration with sensitive data protection

## 📋 Prerequisites

- Claude Desktop (latest version with DXT support)
- JudgmentLabs account with API access
- For manual installation: Python 3.8 or higher

## 🛠️ Installation

### Method 1: DXT Extension (Recommended) 🎯

The easiest way to install this MCP server is through Claude Desktop's DXT extension system:

1. **Download the Extension**: 
   - Get the latest `judgmentlabs-mcp-server.dxt` file from the [releases page](https://github.com/suysoftware/judgmentlabs-mcp-server/releases)
   - No Python installation required!

2. **Install in Claude Desktop**:
   - Open Claude Desktop
   - Go to **Settings → Extensions**
   - Click **"Install Extension"** 
   - Select the downloaded `.dxt` file
   - The extension will be automatically installed

3. **Configure API Credentials**:
   - In Claude Desktop, go to **Settings → Extensions**
   - Find **"JudgmentLabs MCP"** and click **Configure**
   - Enter your credentials:
     - **JUDGMENT_API_KEY**: Your API key from [JudgmentLabs Dashboard](https://app.judgmentlabs.ai/)
     - **JUDGMENT_ORG_ID**: Your organization ID from the dashboard

4. **Enable and Test**:
   - Toggle the extension to **"Enabled"**
   - Restart Claude Desktop
   - Test by asking: *"Create a new project called 'test-project'"*

### Method 2: Build Your Own DXT Package (Advanced Users) ⚙️

For developers who want to build the DXT package from source:

#### Prerequisites
- Python 3.8 or higher
- Node.js and npm

#### Build Steps
```bash
# 1. Clone the repository
git clone https://github.com/suysoftware/judgmentlabs-mcp-server.git

# 2. Install DXT CLI
npm install -g @anthropic-ai/dxt

# 3. Navigate to project directory
cd judgmentlabs-mcp-server

# 4. Install and bundle Python dependencies
pip install -t lib/ judgeval python-dotenv

# 5. Create the DXT package
dxt pack
```

This will generate `judgmentlabs-mcp-server.dxt` in your project directory.

#### Install Your Built Package
```bash
# Install in Claude Desktop:
# 1. Open Claude Desktop
# 2. Go to Settings → Extensions
# 3. Click "Install Extension"
# 4. Select the generated judgmentlabs-mcp-server.dxt file
# 5. Configure your API credentials
# 6. Restart Claude Desktop
# 7. Your MCP server is ready!
```

## 🔧 Available Tools

### Dataset Operations
- **`push_dataset`**: Upload datasets with examples and traces
- **`get_dataset`**: Retrieve existing datasets from projects
- **`delete_dataset`**: Remove datasets from projects

### Project Management
- **`create_project`**: Create new projects
- **`delete_project`**: Delete projects and all data

### Evaluation & Traces
- **`run_evaluation`**: Execute evaluation runs
- **`get_evaluation_results`**: Fetch evaluation results
- **`get_trace`**: Retrieve individual traces
- **`delete_trace`**: Remove specific traces


## 🔒 Security

- **API Keys**: Credentials are securely stored in Claude Desktop's extension configuration
- **No Local Storage**: API keys are not stored in plain text files when using DXT installation
- **Environment Isolation**: Each extension runs in its own secure environment
- **Data Privacy**: All data is transmitted securely to the Judgment API

## 🐛 Troubleshooting

### Common Issues

#### Extension Not Loading
```
Extension failed to load
```
**Solution**: 
1. Make sure you have the latest version of Claude Desktop
2. Check that the `.dxt` file is not corrupted
3. Try reinstalling the extension

#### API Key Configuration Issues
```
Error: No API key provided
```
**Solution**: 
1. Go to Claude Desktop Settings → Extensions
2. Find "JudgmentLabs MCP" and click Configure
3. Ensure both `JUDGMENT_API_KEY` and `JUDGMENT_ORG_ID` are properly set
4. Restart Claude Desktop after configuration changes

#### Connection Issues
```
HTTP 500: API server error
```
**Solution**: Check the JudgmentLabs status page or try again later.

#### Python Path Issues (Build Process)
```
Command not found: dxt
```
**Solution**: 
1. Install Node.js and npm first
2. Install DXT CLI: `npm install -g @anthropic-ai/dxt`
3. Ensure npm global bin is in your PATH

#### Dependencies Bundle Issues
```
Import error: No module named 'judgeval'
```
**Solution**: 
1. Make sure you ran: `pip install -t lib/ judgeval python-dotenv`
2. Check that `lib/` folder contains the packages
3. Rebuild the DXT package: `dxt pack`

### Debug Mode
Enable debug logging by checking the `debug.log` file in the project directory for detailed error information.

## 📈 Performance & Limits

- **Dataset Size**: Supports datasets with thousands of examples
- **Batch Operations**: Efficiently handles bulk operations
- **Rate Limiting**: Respects API rate limits with proper error handling

## 🤝 Contributing

### For Contributors

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test locally with manual installation method
5. Create a new DXT package:
   ```bash
   pip install -t lib/ judgeval python-dotenv
   dxt pack
   ```
6. Test the `.dxt` file in Claude Desktop
7. Commit your changes (`git commit -m 'Add some amazing feature'`)
8. Push to the branch (`git push origin feature/amazing-feature`)
9. Open a Pull Request

### Release Process

1. Update version in `manifest.json`
2. Create and test the DXT package
3. Create a GitHub release
4. Attach the `.dxt` file to the release
5. Update README if needed

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- [JudgmentLabs Website](https://judgmentlabs.ai/)
- [JudgmentLabs Documentation](https://docs.judgmentlabs.ai/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Claude Desktop](https://claude.ai/desktop)

## 👨‍💻 Author

**Sezer Ufuk Yavuz**
- Email: s.ufukyavuz@gmail.com
- GitHub: [@suysoftware](https://github.com/suysoftware)

## 🙏 Acknowledgments

- [Anthropic](https://anthropic.com/) for the Model Context Protocol
- [JudgmentLabs](https://judgmentlabs.ai/) for the evaluation platform
- The open-source community for their valuable contributions

---

For more detailed documentation and examples, visit our [GitHub repository](https://github.com/suysoftware/judgmentlabs-mcp-server).