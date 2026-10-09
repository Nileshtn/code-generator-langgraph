
from llm_sandbox import SandboxSession
from code_generator.core.state import codeState
from code_generator import logger
import re


def _extract_imports(code: str) -> list[str]:
    """Extract import statements from Python code."""
    imports = re.findall(r'^import\s+(\w+)|^from\s+(\w+)', code, re.MULTILINE)
    packages_to_install = []
    
    # Map common import names to pip package names
    package_mapping = {
        'pandas': 'pandas',
        'numpy': 'numpy',
        'requests': 'requests',
        'matplotlib': 'matplotlib',
        'scikit-learn': 'scikit-learn',
        'sklearn': 'scikit-learn',
        'PIL': 'Pillow',
        'seaborn': 'seaborn',
        'scipy': 'scipy',
    }
    
    for imp in imports:
        package_name = imp[0] if imp[0] else imp[1]
        if package_name in package_mapping:
            packages_to_install.append(package_mapping[package_name])
    
    return list(set(packages_to_install))


def execute_in_sandbox(state: codeState) -> dict:
    """Executes the generated code in a Docker sandbox and returns results."""
    logger.info("executing code in sandbox...")
    
    with SandboxSession(lang="python") as session:
        # Extract required packages
        packages_to_install = _extract_imports(state["code"])
        
        # Install packages using pip before running code
        if packages_to_install:
            logger.info(f"installing packages: {packages_to_install}")
            try:
                for package in packages_to_install:
                    session.run_pip(package)
            except Exception as e:
                logger.warning(f"failed to install packages: {e}")
        
        # Run the code
        result = session.run(state["code"])
        
        if result.stderr:
            logger.warning(f"sandbox execution error: {result.stderr}")
            return {
                "feedback_type": "error",
                "feedback": f"Sandbox Error:\n{result.stderr}",
                "execution_result": result.stdout
            }
        
        logger.info("sandbox execution successful")
        return {
            "feedback_type": "",
            "feedback": "",
            "execution_result": result.stdout
        }


def sandbox_route(state: codeState):
    return "write" if state["feedback_type"] == "" else state["feedback_type"]