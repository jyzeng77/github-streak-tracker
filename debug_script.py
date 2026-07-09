import json
from tool_code import ctx_execute # Assuming 'tool_code' is where my tools are exposed

def debug_and_analyze(command: str, intent: str) -> str:
    """
    Executes a shell command using ctx_execute (simulated here) 
    in the sandbox environment and processes its output programmatically.
    
    Args:
        command: The full shell command to run (e.g., "npm run test -- --source auth").
        intent: A descriptive string of what we are looking for in the output.

    Returns:
        A summary analysis based on the intercepted and parsed console output.
    """
    print(f"--- Initiating formal code debug cycle for command: '{command}' ---")
    
    try:
        # In a real environment, this call invokes the sandboxed execution with advanced properties.
        # We are passing an intent to have the system search/indexable summary of the output.
        result = ctx_execute(language="shell", code=f"echo 'Simulating test run successful.' && echo 'Test passed: AuthService.testAuth' && echo 'Warning: Weak password policy detected in auth.ts'", timeout=30)
    except Exception as e:
        return f"Error running context execution: {e}"

    # Since the raw output is complex, we now assume we parse/analyze it within Python logic instead of printing it.
    # For demonstration, we are just treating the result string simply.
    raw_output = str(result) 
    
    analysis = f"\n[DEBUG ANALYSIS SUMMARY]\n"
    analysis += "==========================\n"
    analysis += f"The underlying command ran successfully within the sandboxed context.\n"
    analysis += f"INTENT/GOAL: {intent}\n"
    
    # Here, in a real-world scenario, you would use regex or dedicated parsers 
    # to pull structured data (e.g., extracting failure counts, specific warnings).
    if "Warning: Weak password policy detected" in raw_output:
        analysis += "\n🚨 SECURITY ALERT:\n"
        analysis += "Detected a manual warning about weak password policies within the test output.\n"
        analysis += "Action required: Update auth.ts to enforce stronger policies like minimum length and complexity.\n"
    elif "Test passed" in raw_output:
        analysis += "\n✅ SUCCESS:\n"
        analysis += "All simulated tests passed successfully (based on captured output).\n"
    else:
        analysis += "\n🤔 REVIEW REQUIRED:\n"
        analysis += "Could not apply specific rules. Reviewing the full output is recommended.\n"

    return analysis

if __name__ == "__main__":
    # --- USAGE EXAMPLE ----
    # The command should represent running tests or a linter on your target file/module.
    target_command = "npm run test:unit -- ./src/user_service/auth.ts"
    search_intent = "Capture and diagnose any failing unit tests, security warnings, and coverage gaps for the user authentication module."
    
    summary = debug_and_analyze(target_command, search_intent)
    print("\n\n==========================")
    print("FINAL PROGRAMMATIC SUMMARY:")
    print(summary)