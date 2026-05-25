"""
Example Calculator Plugin — LLM Studio Plugin SDK Demo.

This plugin demonstrates the plugin SDK by implementing a simple
calculator tool that agents can use.

Drop this entire directory into the `plugins/` folder to activate.
Enable it in the Plugin Manager panel.

Features demonstrated:
  - ToolDefinition: a callable tool for agents
  - CommandDefinition: a /calc slash command in chat
  - on_load / on_unload lifecycle hooks
  - Configuration schema
"""

import math
import operator
import re
from typing import Any, Dict

from app.plugin_sdk.base_plugin import (
    BasePlugin, ToolDefinition, CommandDefinition,
)


class CalculatorPlugin(BasePlugin):
    PLUGIN_ID      = "example_calculator"
    PLUGIN_NAME    = "Calculator"
    PLUGIN_DESC    = "Provides math computation tools and /calc command."
    PLUGIN_VERSION = "1.0.0"
    PLUGIN_AUTHOR  = "LLM Studio"

    def on_load(self):
        import logging
        logging.getLogger(__name__).info("Calculator plugin loaded.")

    def on_unload(self):
        import logging
        logging.getLogger(__name__).info("Calculator plugin unloaded.")

    def get_tools(self):
        return [
            ToolDefinition(
                name="calculate",
                description=(
                    "Evaluate a mathematical expression. "
                    "Supports: +, -, *, /, **, sqrt, sin, cos, tan, "
                    "log, abs, round, pi, e."
                ),
                parameters={
                    "expression": {
                        "type": "string",
                        "description": "Math expression to evaluate, e.g. '2 * pi * 5'",
                    }
                },
                required=["expression"],
                handler=self._calculate,
            ),
            ToolDefinition(
                name="unit_convert",
                description="Convert between common units.",
                parameters={
                    "value": {"type": "number", "description": "Numeric value"},
                    "from_unit": {"type": "string", "description": "Source unit"},
                    "to_unit": {"type": "string", "description": "Target unit"},
                },
                required=["value", "from_unit", "to_unit"],
                handler=self._unit_convert,
            ),
        ]

    def get_commands(self):
        return [
            CommandDefinition(
                name="calc",
                description="Evaluate a math expression",
                usage="/calc <expression>",
                handler=self._calc_command,
            ),
        ]

    def _calculate(self, expression: str) -> str:
        """Safe math evaluator using a whitelist."""
        safe_globals = {
            "__builtins__": {},
            "sqrt": math.sqrt, "sin": math.sin, "cos": math.cos,
            "tan": math.tan, "log": math.log, "log10": math.log10,
            "log2": math.log2, "abs": abs, "round": round,
            "pi": math.pi, "e": math.e, "inf": math.inf,
            "floor": math.floor, "ceil": math.ceil,
            "pow": pow, "factorial": math.factorial,
        }
        # Whitelist characters
        allowed = re.compile(r"^[0-9\s\+\-\*\/\(\)\.\,\_\^a-zA-Z]+$")
        cleaned = expression.strip()
        cleaned = cleaned.replace("^", "**")   # allow ^ for exponentiation

        if not allowed.match(cleaned):
            return f"Error: Invalid expression '{expression}'"

        try:
            result = eval(cleaned, safe_globals)  # noqa: S307
            if isinstance(result, float):
                if result.is_integer():
                    return str(int(result))
                return str(round(result, 10))
            return str(result)
        except ZeroDivisionError:
            return "Error: Division by zero"
        except Exception as e:
            return f"Error: {e}"

    def _unit_convert(self, value: float, from_unit: str, to_unit: str) -> str:
        """Simple unit conversion for common units."""
        conversions = {
            # Length (to meters)
            "km": 1000, "m": 1, "cm": 0.01, "mm": 0.001,
            "mi": 1609.344, "yd": 0.9144, "ft": 0.3048, "in": 0.0254,
            # Weight (to kg)
            "kg": 1, "g": 0.001, "lb": 0.453592, "oz": 0.0283495,
            # Temperature handled separately
        }
        temp_units = {"c", "f", "k"}
        fu, tu = from_unit.lower(), to_unit.lower()

        if fu in temp_units or tu in temp_units:
            return self._temp_convert(value, fu, tu)

        if fu not in conversions or tu not in conversions:
            return (f"Error: Unknown unit(s). "
                    f"Supported: {', '.join(sorted(conversions))}")

        base = value * conversions[fu]
        result = base / conversions[tu]
        return f"{value} {from_unit} = {round(result, 6)} {to_unit}"

    def _temp_convert(self, v: float, f: str, t: str) -> str:
        # Convert to Celsius first
        if f == "f":
            celsius = (v - 32) * 5 / 9
        elif f == "k":
            celsius = v - 273.15
        else:
            celsius = v
        # Convert to target
        if t == "f":
            result = celsius * 9 / 5 + 32
        elif t == "k":
            result = celsius + 273.15
        else:
            result = celsius
        return f"{v}°{f.upper()} = {round(result, 4)}°{t.upper()}"

    def _calc_command(self, args: str, session=None) -> str:
        if not args.strip():
            return "Usage: /calc <expression>"
        return f"= {self._calculate(args.strip())}"

    def get_config_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "precision": {
                    "type": "integer",
                    "default": 10,
                    "description": "Decimal places for results",
                }
            }
        }
