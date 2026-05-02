"""
Hermes Integration — Operación legal via Hermes Agent.

Modo dual: funciona tanto por Telegram (Hermes) como por Dashboard.
"""

from .commands import HermesLegalCommands
from .session_manager import LegalSessionManager

__all__ = ["HermesLegalCommands", "LegalSessionManager"]
__version__ = "1.0.0"
