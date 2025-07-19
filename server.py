#!/usr/bin/env python3
"""
Judgeval MCP Server - DXT Version
=================================
"""

import json
import sys
import os

# Debug için path bilgilerini logla
current_dir = os.path.dirname(os.path.abspath(__file__))
lib_path = os.path.join(current_dir, 'lib')

# DXT için lib path'ini ekle
if lib_path not in sys.path:
    sys.path.insert(0, lib_path)

# Current directory'yi de ekle
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Debug log
def debug_log(message):
    with open(os.path.join(current_dir, 'debug.log'), 'a') as f:
        f.write(f"{message}\n")


debug_log(f"Current dir: {current_dir}")
debug_log(f"Lib path: {lib_path}")
debug_log(f"Lib exists: {os.path.exists(lib_path)}")
debug_log(f"Python path: {sys.path}")

# Environment variables kontrolü
JUDGMENT_API_KEY = os.getenv('JUDGMENT_API_KEY')
debug_log(f"API Key exists: {bool(JUDGMENT_API_KEY)}")

# API key kontrolü - artık hemen çıkmayacak, main() fonksiyonunda kontrol edilecek


# Suppress all stdout output from imports
class SuppressStdout:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


# Import with suppressed stdout
try:
    with SuppressStdout():
        from dotenv import load_dotenv
        load_dotenv()
        
        from judgeval.judgment_client import JudgmentClient
        from judgeval.data.example import Example
        from judgeval.data.trace import Trace
        
        client = JudgmentClient()
    debug_log("Imports successful")
    
except Exception as e:
    debug_log(f"Import error: {str(e)}")
    print(json.dumps({
        "jsonrpc": "2.0",
        "id": None,
        "error": {"code": -32001, "message": f"Import error: {str(e)}"}
    }, default=str))
    sys.exit(1)


def get_tools():
    """Get all available tools"""
    return [
        {
            "name": "get_trace",
            "description": "Fetch a trace by its ID from the Judgment API",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "trace_id": {
                        "type": "string", 
                        "description": "The ID of the trace to fetch"
                    }
                },
                "required": ["trace_id"]
            }
        },
        {
            "name": "delete_trace",
            "description": "Delete a trace by its ID from the Judgment API",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "trace_id": {
                        "type": "string", 
                        "description": "The ID of the trace to delete"
                    }
                },
                "required": ["trace_id"]
            }
        },
        {
            "name": "run_evaluation",
            "description": "Run an evaluation via the Judgment API",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "evaluation_data": {
                        "type": "object", 
                        "description": ("Evaluation data matching "
                                        "EvaluationRun.model_dump()")
                    }
                },
                "required": ["evaluation_data"]
            }
        },
        {
            "name": "get_evaluation_results",
            "description": ("Fetch evaluation results for a project and "
                           "evaluation run"),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "project_name": {
                        "type": "string", 
                        "description": "Project name"
                    },
                    "eval_name": {
                        "type": "string", 
                        "description": "Evaluation run name"
                    }
                },
                "required": ["project_name", "eval_name"]
            }
        },
        {
            "name": "get_dataset",
            "description": "Pull a dataset by alias and project",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "alias": {
                        "type": "string", 
                        "description": "Dataset alias"
                    },
                    "project_name": {
                        "type": "string", 
                        "description": "Project name"
                    }
                },
                "required": ["alias", "project_name"]
            }
        },
        {
            "name": "push_dataset",
            "description": ("Push a dataset (examples + traces) "
                            "to the Judgment API"),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "alias": {
                        "type": "string", 
                        "description": "Dataset alias"
                    },
                    "project_name": {
                        "type": "string", 
                        "description": "Project name"
                    },
                    "examples": {
                        "type": "array", 
                        "items": {"type": "object"}, 
                        "description": "List of example dicts"
                    },
                    "traces": {
                        "type": "array", 
                        "items": {"type": "object"}, 
                        "description": "Optional trace dicts"
                    },
                    "overwrite": {
                        "type": "boolean", 
                        "description": "Overwrite existing dataset completely", 
                        "default": False
                    },
                    "append": {
                        "type": "boolean", 
                        "description": "Append to existing dataset", 
                        "default": False
                    }
                },
                "required": ["alias", "project_name", "examples"]
            }
        },
        {
            "name": "delete_dataset",
            "description": "Delete a dataset by alias and project",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "alias": {
                        "type": "string", 
                        "description": "Dataset alias"
                    },
                    "project_name": {
                        "type": "string", 
                        "description": "Project name"
                    }
                },
                "required": ["alias", "project_name"]
            }
        },
        {
            "name": "create_project",
            "description": "Create a new project in the Judgment API",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "project_name": {
                        "type": "string", 
                        "description": "Project name"
                    }
                },
                "required": ["project_name"]
            }
        },
        {
            "name": "delete_project",
            "description": ("Delete a project and all its data in the "
                           "Judgment API"),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "project_name": {
                        "type": "string", 
                        "description": "Project name"
                    }
                },
                "required": ["project_name"]
            }
        }
    ]


def create_project_if_not_exists(project_name):
    """Helper function to create project if it doesn't exist"""
    try:
        client.create_project(project_name)
        return {"status": "created", "project_name": project_name}
    except Exception as e:
        error_str = str(e)
        if "already exists" in error_str.lower() or "400" in error_str:
            return {"status": "already_exists", "project_name": project_name}
        elif ("500" in error_str or 
              "internal server error" in error_str.lower()):
            return {
                "status": "api_error", 
                "project_name": project_name, 
                "error": "HTTP 500: API server error"
            }
        else:
            raise e


def execute_tool(name, arguments):
    """Execute a tool by name with given arguments"""
    # Suppress stdout during tool execution
    original_stdout = sys.stdout
    sys.stdout = open(os.devnull, 'w')
    
    try:
        if name == "get_trace":
            result = client.api_client.fetch_trace(arguments["trace_id"])
            return {
                "content": [{
                    "type": "text", 
                    "text": json.dumps(result, default=str)
                }]
            }
        
        elif name == "delete_trace":
            result = client.api_client.delete_trace(arguments["trace_id"])
            return {
                "content": [{
                    "type": "text", 
                    "text": json.dumps(result, default=str)
                }]
            }
        
        elif name == "run_evaluation":
            result = client.api_client.run_evaluation(
                arguments["evaluation_data"]
            )
            return {
                "content": [{
                    "type": "text", 
                    "text": json.dumps(result, default=str)
                }]
            }
        
        elif name == "get_evaluation_results":
            result = client.api_client.fetch_evaluation_results(
                arguments["project_name"], 
                arguments["eval_name"]
            )
            return {
                "content": [{
                    "type": "text", 
                    "text": json.dumps(result, default=str)
                }]
            }
        
        elif name == "get_dataset":
            try:
                result = client.pull_dataset(
                    arguments["alias"], 
                    arguments["project_name"]
                )
                # Dataset nesnesini JSON-serializable formata çevir
                dataset_dict = {
                    "alias": arguments["alias"],
                    "project_name": arguments["project_name"],
                    "examples": [],
                    "traces": []
                }
                
                if result and hasattr(result, 'examples') and result.examples:
                    for ex in result.examples:
                        example_dict = {
                            "example_id": getattr(ex, 'example_id', None),
                            "input": getattr(ex, 'input', None),
                            "expected_output": getattr(
                                ex, 'expected_output', None
                            ),
                            "actual_output": getattr(
                                ex, 'actual_output', None
                            ),
                            "context": getattr(ex, 'context', None),
                            "name": getattr(ex, 'name', None),
                            "created_at": str(getattr(ex, 'created_at', None))
                        }
                        dataset_dict["examples"].append(example_dict)
                
                if result and hasattr(result, 'traces') and result.traces:
                    for trace in result.traces:
                        trace_dict = {
                            "trace_id": getattr(trace, 'trace_id', None),
                            "input": getattr(trace, 'input', None),
                            "output": getattr(trace, 'output', None)
                        }
                        dataset_dict["traces"].append(trace_dict)
                
                return {
                    "content": [{
                        "type": "text", 
                        "text": json.dumps(dataset_dict, default=str)
                    }]
                }
            except Exception as e:
                return {
                    "content": [{
                        "type": "text", 
                        "text": json.dumps(
                            {"error": f"Failed to get dataset: {str(e)}"}, 
                            default=str
                        )
                    }]
                }
        
        elif name == "push_dataset":
            try:
                # Önce projenin var olduğundan emin ol
                project_status = create_project_if_not_exists(
                    arguments["project_name"]
                )
                
                # Mevcut dataset'i kontrol et
                existing_examples = []
                try:
                    existing_dataset = client.pull_dataset(
                        arguments["alias"], 
                        arguments["project_name"]
                    )
                    if (existing_dataset and 
                            hasattr(existing_dataset, 'examples')):
                        for ex in existing_dataset.examples:
                            # Sadece dolu example'ları say
                            if ex.input is not None:
                                existing_examples.append(ex)
                except Exception:
                    # Dataset yok, sorun değil
                    pass
                
                # Append mode kontrolü
                overwrite = arguments.get("overwrite", False) 
                append_mode = arguments.get("append", False)
                
                # Eğer hiçbiri belirtilmemişse ve mevcut data varsa, append yap
                if not overwrite and not append_mode and existing_examples:
                    append_mode = True
                
                ds = client.create_dataset()
                
                # Mevcut example'ları ekle (append mode'da)
                all_examples = []
                if append_mode and existing_examples:
                    all_examples.extend(existing_examples)
                
                # Yeni example'ları ekle
                for ex in arguments["examples"]:
                    try:
                        # Judgment Example için doğru alanları kullan
                        example_data = {}
                        
                        # Input alanı
                        if "input" in ex:
                            example_data["input"] = str(ex["input"])
                        elif "question" in ex:
                            example_data["input"] = str(ex["question"])
                        
                        # Expected output alanı  
                        if "expected_output" in ex:
                            example_data["expected_output"] = str(
                                ex["expected_output"]
                            )
                        elif "expected" in ex:
                            example_data["expected_output"] = str(
                                ex["expected"]
                            )
                        elif "answer" in ex:
                            example_data["expected_output"] = str(
                                ex["answer"]
                            )
                        
                        # Opsiyonel alanlar
                        if "actual_output" in ex:
                            example_data["actual_output"] = str(
                                ex["actual_output"]
                            )
                        if "context" in ex:
                            example_data["context"] = str(ex["context"])
                        if "name" in ex:
                            example_data["name"] = str(ex["name"])
                        
                        # Example oluştur
                        new_example = Example(**example_data)
                        all_examples.append(new_example)
                        
                    except Exception as ex_error:
                        return {
                            "content": [{
                                "type": "text", 
                                "text": json.dumps({
                                    "status": "error",
                                    "error": (f"Failed to create example: "
                                             f"{str(ex_error)}"),
                                    "example_data": ex,
                                    "suggestion": "Check example format"
                                }, default=str)
                            }]
                        }
                
                ds.examples = all_examples
                
                if "traces" in arguments and arguments["traces"]:
                    ds.traces = [Trace(**t) for t in arguments["traces"]]
                else:
                    ds.traces = []
                
                result = client.push_dataset(
                    arguments["alias"], 
                    ds, 
                    arguments["project_name"], 
                    overwrite  # append mode'da overwrite=False
                )
                
                operation_type = ("overwritten" if overwrite 
                                else ("appended" if append_mode 
                                      else "created"))
                
                return {
                    "content": [{
                        "type": "text", 
                        "text": json.dumps({
                            "status": "success",
                            "operation": operation_type,
                            "alias": arguments["alias"],
                            "project_name": arguments["project_name"],
                            "new_examples_added": len(arguments["examples"]),
                            "existing_examples_count": len(existing_examples),
                            "total_examples_count": len(all_examples),
                            "project_status": project_status["status"],
                            "append_mode": append_mode,
                            "overwrite_mode": overwrite,
                            "result": bool(result)
                        }, default=str)
                    }]
                }
                
            except Exception as e:
                error_msg = str(e)
                return {
                    "content": [{
                        "type": "text", 
                        "text": json.dumps({
                            "status": "error", 
                            "error": error_msg,
                            "suggestion": ("Verify: 1) Project exists "
                                         "2) Example format: {input: 'question', "
                                         "expected_output: 'answer'}")
                        }, default=str)
                    }]
                }
        
        elif name == "delete_dataset":
            result = client.delete_dataset(
                arguments["alias"], 
                arguments["project_name"]
            )
            return {
                "content": [{
                    "type": "text", 
                    "text": json.dumps(result, default=str)
                }]
            }
        
        elif name == "create_project":
            try:
                client.create_project(arguments["project_name"])
                result = {
                    "status": "created", 
                    "project_name": arguments["project_name"]
                }
            except Exception as e:
                error_str = str(e)
                if "already exists" in error_str.lower() or "400" in error_str:
                    result = {
                        "status": "already_exists", 
                        "project_name": arguments["project_name"], 
                        "message": "Project already exists"
                    }
                elif ("500" in error_str or 
                      "internal server error" in error_str.lower()):
                    result = {
                        "status": "error", 
                        "project_name": arguments["project_name"], 
                        "error": ("HTTP 500: Internal Server Error - "
                                "Judgment API is experiencing issues"),
                        "suggestion": ("Try again in a few minutes or "
                                     "check API status")
                    }
                else:
                    result = {
                        "status": "error", 
                        "project_name": arguments["project_name"], 
                        "error": error_str
                    }
            return {
                "content": [{
                    "type": "text", 
                    "text": json.dumps(result, default=str)
                }]
            }
        
        elif name == "delete_project":
            client.delete_project(arguments["project_name"])
            result = {
                "status": "deleted", 
                "project_name": arguments["project_name"]
            }
            return {
                "content": [{
                    "type": "text", 
                    "text": json.dumps(result, default=str)
                }]
            }
        
        else:
            return {
                "content": [{
                    "type": "text", 
                    "text": f"Unknown tool: {name}"
                }]
            }
            
    except Exception as e:
        return {"content": [{"type": "text", "text": f"Error: {str(e)}"}]}
    finally:
        # Restore stdout
        sys.stdout.close()
        sys.stdout = original_stdout


def main():
    """Main MCP server function"""
    # API key kontrolü
    if not JUDGMENT_API_KEY:
        debug_log("ERROR: No API key provided")
        # API key olmadığında tüm mesajlara hata döndür
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
                
            try:
                message = json.loads(line)
                method = message.get("method")
                message_id = message.get("id", 1)
                
                response = {
                    "jsonrpc": "2.0",
                    "id": message_id,
                    "error": {
                        "code": -32000, 
                        "message": "No API key provided"
                    }
                }
                try:
                    print(json.dumps(response))
                    sys.stdout.flush()
                except BrokenPipeError:
                    # Client bağlantıyı kapattı, server'ı kapat
                    break
                except Exception as e:
                    # Diğer hataları logla ama devam et
                    debug_log(f"Error sending response: {str(e)}")
                    break
                    
            except Exception as e:
                error_response = {
                    "jsonrpc": "2.0",
                    "id": (message.get("id", 1) if 'message' in locals() 
                           else 1),
                    "error": {
                        "code": -32603, 
                        "message": f"Internal error: {str(e)}"
                    }
                }
                try:
                    print(json.dumps(error_response))
                    sys.stdout.flush()
                except BrokenPipeError:
                    break
                except Exception as ex:
                    debug_log(f"Error sending error response: {str(ex)}")
                    break
    
    # Client'ı oluştur
    try:
        client = JudgmentClient()
    except Exception as e:
        debug_log(f"Client creation error: {str(e)}")
        # Client oluşturulamadığında tüm mesajlara hata döndür
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
                
            try:
                message = json.loads(line)
                method = message.get("method")
                message_id = message.get("id", 1)
                
                response = {
                    "jsonrpc": "2.0",
                    "id": message_id,
                    "error": {
                        "code": -32001, 
                        "message": f"Client creation error: {str(e)}"
                    }
                }
                try:
                    print(json.dumps(response))
                    sys.stdout.flush()
                except BrokenPipeError:
                    # Client bağlantıyı kapattı, server'ı kapat
                    break
                except Exception as ex:
                    # Diğer hataları logla ama devam et
                    debug_log(f"Error sending response: {str(ex)}")
                    break
                    
            except Exception as ex:
                error_response = {
                    "jsonrpc": "2.0",
                    "id": (message.get("id", 1) if 'message' in locals() 
                           else 1),
                    "error": {
                        "code": -32603, 
                        "message": f"Internal error: {str(ex)}"
                    }
                }
                try:
                    print(json.dumps(error_response))
                    sys.stdout.flush()
                except BrokenPipeError:
                    break
                except Exception as e:
                    debug_log(f"Error sending error response: {str(e)}")
                    break
    
    tools = get_tools()
    
    # Suppress stdout during execution to prevent JSON parse errors
    original_stdout = sys.stdout
    sys.stdout = open(os.devnull, 'w')
    
    try:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
                
            try:
                message = json.loads(line)
                method = message.get("method")
                message_id = message.get("id", 1)
                params = message.get("params", {})
                
                if method == "initialize":
                    response = {
                        "jsonrpc": "2.0",
                        "id": message_id,
                        "result": {
                            "protocolVersion": "2024-11-05",
                            "capabilities": {"tools": {}},
                            "serverInfo": {
                                "name": "judgeval", 
                                "version": "1.0.0"
                            }
                        }
                    }
                
                elif method == "tools/list":
                    response = {
                        "jsonrpc": "2.0",
                        "id": message_id,
                        "result": {"tools": tools}
                    }
                
                elif method == "tools/call":
                    tool_name = params.get("name")
                    arguments = params.get("arguments", {})
                    
                    if not tool_name:
                        response = {
                            "jsonrpc": "2.0",
                            "id": message_id,
                            "error": {
                                "code": -32602, 
                                "message": "Invalid params: missing tool name"
                            }
                        }
                    else:
                        result = execute_tool(tool_name, arguments)
                        response = {
                            "jsonrpc": "2.0",
                            "id": message_id,
                            "result": result
                        }
                
                elif method in ["resources/list", "prompts/list"]:
                    key = ("resources" if method == "resources/list" 
                           else "prompts")
                    response = {
                        "jsonrpc": "2.0",
                        "id": message_id,
                        "result": {key: []}
                    }
                
                else:
                    response = {
                        "jsonrpc": "2.0",
                        "id": message_id,
                        "error": {
                            "code": -32601, 
                            "message": f"Method not found: {method}"
                        }
                    }
                
                # Restore stdout temporarily to print response
                sys.stdout.close()
                sys.stdout = original_stdout
                try:
                    print(json.dumps(response))
                    sys.stdout.flush()
                except BrokenPipeError:
                    # Client bağlantıyı kapattı, server'ı kapat
                    break
                except Exception as e:
                    # Diğer hataları logla ama devam et
                    debug_log(f"Error sending response: {str(e)}")
                    break
                # Suppress stdout again
                sys.stdout = open(os.devnull, 'w')
                
            except Exception as e:
                # Restore stdout temporarily to print error
                sys.stdout.close()
                sys.stdout = original_stdout
                error_response = {
                    "jsonrpc": "2.0",
                    "id": (message.get("id", 1) if 'message' in locals() 
                           else 1),
                    "error": {
                        "code": -32603, 
                        "message": f"Internal error: {str(e)}"
                    }
                }
                try:
                    print(json.dumps(error_response))
                    sys.stdout.flush()
                except BrokenPipeError:
                    # Client bağlantıyı kapattı, server'ı kapat
                    break
                except Exception as ex:
                    # Diğer hataları logla ama devam et
                    debug_log(f"Error sending error response: {str(ex)}")
                    break
                # Suppress stdout again
                sys.stdout = open(os.devnull, 'w')
    finally:
        # Restore stdout
        sys.stdout.close()
        sys.stdout = original_stdout


if __name__ == "__main__":
    main()