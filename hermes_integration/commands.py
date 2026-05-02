#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hermes Legal Commands — Parser de comandos Telegram para operación legal.

Uso:
    from hermes_integration.commands import HermesLegalCommands
    cmd = HermesLegalCommands()
    result = cmd.crear_matter("Innovatech Digital")
    print(result["mensaje"])
"""

import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime


class HermesLegalCommands:
    """
    Interfaz de comandos para operación legal via Hermes Agent.
    
    Mantiene compatibilidad con:
    - Modo Hermes (Telegram): comandos tipo /matter, /contrato
    - Modo Dashboard: mismo backend de datos
    """
    
    def __init__(self, base_dir="~/WillowLegal"):
        """
        Inicializar con directorio base.
        
        Args:
            base_dir: Directorio raíz de WillowLegal (default: ~/WillowLegal)
        """
        self.base_dir = Path(base_dir).expanduser()
        self.datos_dir = self.base_dir / "datos"
        self.datos_dir.mkdir(parents=True, exist_ok=True)
        
        # Archivos de datos
        self.matters_file = self.datos_dir / "matters.json"
        self.documentos_file = self.datos_dir / "documentos.json"
        self.alertas_file = self.datos_dir / "alertas.json"
        self.finanzas_file = self.datos_dir / "finanzas.json"
        
        # Referencia al motor
        self.motor_dir = self.base_dir / "00_Sistema" / "Motor_Kami"
        self.repo_dir = Path(__file__).parent.parent  # ws-hermes-legal-pro
    
    # ============================================================
    # MATTERS
    # ============================================================
    
    def crear_matter(self, nombre: str, **kwargs) -> dict:
        """
        Crear nuevo matter desde comando Telegram.
        
        Args:
            nombre: Nombre del cliente o asunto
            cliente: (opcional) Nombre del cliente si difiere
            area: (opcional) Área legal (default: Mercantil)
            prioridad: (opcional) baja/media/alta (default: media)
            
        Returns:
            dict con status, matter_id, mensaje
        """
        try:
            # Cargar matters existentes
            matters = self._load_json(self.matters_file, [])
            
            # Generar ID
            matter_id = f"WIL-{len(matters)+1:03d}"
            
            # Crear matter
            matter = {
                "id": matter_id,
                "nombre": nombre,
                "cliente": kwargs.get("cliente", nombre),
                "estado": "Intake",
                "area": kwargs.get("area", "Mercantil"),
                "materia": kwargs.get("materia", "corporativo"),
                "prioridad": kwargs.get("prioridad", "media"),
                "creado": datetime.now().isoformat(),
                "actualizado": datetime.now().isoformat(),
                "next_step": "Intake inicial pendiente",
                "blocker": "none",
                "carpeta": str(self.base_dir / "01_Clientes" / self._safe_name(nombre)),
                "deadline": kwargs.get("deadline", None),
                "descripcion": kwargs.get("descripcion", "")
            }
            
            matters.append(matter)
            self._save_json(self.matters_file, matters)
            
            # Crear estructura de carpetas
            self._crear_carpetas_matter(matter["carpeta"])
            
            # Crear en Drive (usar token existente)
            try:
                from scripts.drive_manager import DriveManager
                dm = DriveManager()
                drive_folder_id = dm.create_client_structure(matter["cliente"])
                matter["drive_folder_id"] = drive_folder_id
                matter["drive_link"] = f"https://drive.google.com/drive/folders/{drive_folder_id}"
                print(f"📁 Drive: Carpeta creada {drive_folder_id}")
            except Exception as e:
                print(f"⚠️  Drive no disponible: {e}")
                matter["drive_folder_id"] = None
                matter["drive_link"] = None
            
            return {
                "status": "ok",
                "matter_id": matter_id,
                "mensaje": (
                    f"✅ Matter creado: {matter_id}\n"
                    f"📁 Carpeta: {matter['carpeta']}\n"
                    f"📋 Next step: {matter['next_step']}\n"
                    f"🏷️  Área: {matter['area']}\n"
                    f"📁 Drive: {matter.get('drive_link', 'No disponible')}"
                )
            }
            
        except Exception as e:
            return {
                "status": "error",
                "mensaje": f"❌ Error creando matter: {str(e)}"
            }
    
    def listar_matters(self, limite: int = 10) -> dict:
        """Listar matters activos para mostrar en Telegram."""
        try:
            matters = self._load_json(self.matters_file, [])
            
            if not matters:
                return {
                    "status": "ok",
                    "mensaje": "📭 No hay matters registrados"
                }
            
            lines = ["📋 MATTERS ACTIVOS:"]
            for m in matters[-limite:]:
                emoji = "🟢" if m.get("estado") == "Activo" else "🟡" if m.get("estado") == "Intake" else "🔴"
                drive_icon = "📁" if m.get("drive_folder_id") else "❌"
                lines.append(f"  {emoji} {m['id']}: {m['nombre']} {drive_icon}")
            
            return {
                "status": "ok",
                "mensaje": "\n".join(lines),
                "data": matters[-limite:]
            }
            
        except Exception as e:
            return {
                "status": "error",
                "mensaje": f"❌ Error listando matters: {str(e)}"
            }
    
    def ver_matter(self, matter_id: str) -> dict:
        """Ver detalle de un matter específico."""
        try:
            matters = self._load_json(self.matters_file, [])
            
            matter = next((m for m in matters if m["id"] == matter_id), None)
            if not matter:
                return {
                    "status": "error",
                    "mensaje": f"❌ Matter {matter_id} no encontrado"
                }
            
            return {
                "status": "ok",
                "mensaje": (
                    f"📋 {matter['id']}: {matter['nombre']}\n"
                    f"   Estado: {matter['estado']}\n"
                    f"   Área: {matter['area']}\n"
                    f"   Next step: {matter.get('next_step', 'N/A')}\n"
                    f"   Blocker: {matter.get('blocker', 'none')}\n"
                    f"   📁 {matter['carpeta']}"
                ),
                "data": matter
            }
            
        except Exception as e:
            return {
                "status": "error",
                "mensaje": f"❌ Error: {str(e)}"
            }
    
    # ============================================================
    # DOCUMENTOS / CONTRATOS
    # ============================================================
    
    def generar_documento(self, template: str, matter_id: str = None, **kwargs) -> dict:
        """
        Generar documento legal via Motor Kami.
        
        Args:
            template: Key del template (nda, prestacion_servicios, etc.)
            matter_id: (opcional) Matter asociado
            variables: (opcional) Dict con variables adicionales
            
        Returns:
            dict con status, mensaje, path del PDF
        """
        try:
            # Verificar template existe
            template_file = self.repo_dir / "motor_kami" / "templates" / f"{template}.json"
            if not template_file.exists():
                templates_dir = self.repo_dir / "motor_kami" / "templates"
                disponibles = [f.stem for f in templates_dir.glob("*.json") if f.stem != "index"]
                return {
                    "status": "error",
                    "mensaje": (
                        f"❌ Template '{template}' no encontrado\n"
                        f"📋 Disponibles: {', '.join(disponibles[:10])}"
                    )
                }
            
            # Cargar template y matter
            import tempfile
            import os
            
            with open(template_file, "r", encoding="utf-8") as f:
                template_data = json.load(f)
            
            # Obtener datos del matter
            matters = self._load_json(self.matters_file, [])
            matter = next((m for m in matters if m["id"] == matter_id), None) if matter_id else None
            
            # Construir datos para el motor
            template_label = template_data.get("metadata", {}).get("label", template)
            cliente_nombre = matter.get("cliente", matter.get("nombre", "Cliente")) if matter else kwargs.get("cliente", "Cliente")
            
            # Construir cláusulas apropiadas según template
            if template == "nda":
                clausulas_data = [
                    {"titulo": "Objeto", "subclausulas": [
                        "Las partes acuerdan mantener la confidencialidad de toda información intercambiada."
                    ]},
                    {"titulo": "Información Confidencial", "subclausulas": [
                        "Se considera información confidencial todo dato técnico, comercial, financiero o de cualquier naturaleza."
                    ]},
                    {"titulo": "Obligaciones", "subclausulas": [
                        "No divulgar la información confidencial a terceros.",
                        "Usar la información solo para los fines del presente acuerdo.",
                        "Devolver o destruir la información al término del acuerdo."
                    ]},
                    {"titulo": "Vigencia", "subclausulas": [
                        "El presente acuerdo tendrá una vigencia de 2 años."
                    ]}
                ]
            else:
                clausulas_data = [
                    {"titulo": "Objeto", "subclausulas": [
                        matter.get("descripcion", "Servicios legales profesionales") if matter else "Servicios legales profesionales"
                    ]},
                    {"titulo": "Obligaciones de las Partes", "subclausulas": [
                        "El Prestador se obliga a prestar los servicios con la debida diligencia profesional.",
                        "El Cliente se obliga a proporcionar la información necesaria para la prestación de los servicios."
                    ]},
                    {"titulo": "Honorarios", "subclausulas": [
                        "Los honorarios serán pactados en documento anexo."
                    ]},
                    {"titulo": "Vigencia", "subclausulas": [
                        "El presente contrato tendrá vigencia indefinida."
                    ]}
                ]
            
            doc_data = {
                "tipo": "contrato",
                "titulo": kwargs.get("titulo", template_label),
                "marca": "Hermes Legal Pro",
                "numero_contrato": f"{matter_id}-{template}" if matter_id else template,
                "fecha": datetime.now().strftime("%d de %B de %Y"),
                "subtitulo": kwargs.get("subtitulo", ""),
                "antecedentes": matter.get("descripcion", "Servicios legales profesionales") if matter else "Servicios legales profesionales",
                "prestador": {
                    "nombre": "We Law S.C.",
                    "rfc": "WEL123456ABC",
                    "domicilio": "Ciudad de México",
                    "representante": "Lic. Pablo Meneses",
                    "email": "contacto@welaw.mx"
                },
                "cliente": {
                    "nombre": cliente_nombre,
                    "rfc": kwargs.get("rfc_cliente", "XAXX010101000"),
                    "domicilio": kwargs.get("domicilio_cliente", "México"),
                    "representante": kwargs.get("representante_cliente", cliente_nombre),
                    "email": kwargs.get("email_cliente", "")
                },
                "clausulas": clausulas_data,
                "anexos": [],
                "cliente_nombre": cliente_nombre
            }
            
            # Escribir JSON temporal
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as tmp:
                json.dump(doc_data, tmp, ensure_ascii=False)
                tmp_path = tmp.name
            
            # Preparar output path
            output_dir = self.repo_dir / "motor_kami" / "output"
            output_dir.mkdir(exist_ok=True)
            output_filename = kwargs.get("output_filename", f"{matter_id}_{template}.pdf" if matter_id else f"{template}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
            output_path = output_dir / output_filename
            
            # Ejecutar motor
            motor_script = self.repo_dir / "motor_kami" / "motor_kami.py"
            cmd = [
                sys.executable,
                str(motor_script),
                "--input", tmp_path,
                "--output", str(output_path),
                "--preview-html"
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            # Limpiar archivo temporal
            os.unlink(tmp_path)
            
            if result.returncode != 0:
                return {
                    "status": "error",
                    "mensaje": f"❌ Motor Kami error:\n{result.stderr}"
                }
            
            mensaje = (
                f"📝 Documento generado:\n"
                f"   Template: {template_label}\n"
                f"   📄 {output_filename}\n"
                f"   📁 {output_dir}"
            )
            
            # Subir a Drive si el matter tiene carpeta
            if matter and matter.get("drive_folder_id"):
                try:
                    from scripts.drive_manager import DriveManager
                    dm = DriveManager()
                    drive_result = dm.upload_pdf(str(output_path), cliente_nombre)
                    mensaje += f"\n📤 Drive: {drive_result['link']}"
                except Exception as e:
                    mensaje += f"\n⚠️  Drive: {e}"
            
            return {
                "status": "ok",
                "mensaje": mensaje,
                "pdf_path": str(output_path)
            }
                
        except Exception as e:
            return {
                "status": "error",
                "mensaje": f"❌ Error generando documento: {str(e)}"
            }
    
    def listar_templates(self) -> dict:
        """Listar templates disponibles."""
        try:
            templates_dir = self.repo_dir / "motor_kami" / "templates"
            templates = [f.stem for f in templates_dir.glob("*.json") if f.stem != "index"]
            
            lines = ["📋 TEMPLATES DISPONIBLES:"]
            for t in sorted(templates):
                lines.append(f"  • {t}")
            
            return {
                "status": "ok",
                "mensaje": "\n".join(lines)
            }
            
        except Exception as e:
            return {
                "status": "error",
                "mensaje": f"❌ Error: {str(e)}"
            }
    
    # ============================================================
    # PLAZOS / ALERTAS
    # ============================================================
    
    def crear_plazo(self, matter_id: str, descripcion: str, fecha: str, **kwargs) -> dict:
        """Crear plazo con alerta."""
        try:
            alertas = self._load_json(self.alertas_file, [])
            
            alerta = {
                "id": f"ALERT-{len(alertas)+1:03d}",
                "matter_id": matter_id,
                "descripcion": descripcion,
                "fecha": fecha,
                "tipo": kwargs.get("tipo", "plazo"),
                "estado": "pendiente",
                "creado": datetime.now().isoformat()
            }
            
            alertas.append(alerta)
            self._save_json(self.alertas_file, alertas)
            
            # Crear en Google Calendar
            mensaje_extra = ""
            try:
                from scripts.calendar_manager import CalendarManager
                cm = CalendarManager()
                
                cal_result = cm.create_deadline(
                    matter_id=matter_id,
                    descripcion=descripcion,
                    fecha=fecha,
                    reminder_days=[3, 1]
                )
                
                alerta["calendar_event_id"] = cal_result['id']
                alerta["calendar_link"] = cal_result['link']
                self._save_json(self.alertas_file, alertas)
                
                mensaje_extra = f"\n📅 Calendar: {cal_result['link']}"
            except Exception as e:
                print(f"⚠️  Calendar: {e}")
            
            return {
                "status": "ok",
                "mensaje": (
                    f"📅 Plazo creado: {alerta['id']}\n"
                    f"   Matter: {matter_id}\n"
                    f"   📌 {descripcion}\n"
                    f"   📆 Fecha límite: {fecha}"
                    f"{mensaje_extra}"
                )
            }
            
        except Exception as e:
            return {
                "status": "error",
                "mensaje": f"❌ Error: {str(e)}"
            }
    
    def ver_alertas(self, matter_id: str = None) -> dict:
        """Ver alertas pendientes."""
        try:
            alertas = self._load_json(self.alertas_file, [])
            
            if matter_id:
                alertas = [a for a in alertas if a.get("matter_id") == matter_id]
            
            pendientes = [a for a in alertas if a.get("estado") == "pendiente"]
            
            if not pendientes:
                return {
                    "status": "ok",
                    "mensaje": "✅ No hay alertas pendientes"
                }
            
            lines = [f"📢 ALERTAS PENDIENTES ({len(pendientes)})"]
            for a in pendientes[-10:]:
                lines.append(f"  • {a['id']}: {a['descripcion']} (vence: {a['fecha']})")
            
            return {
                "status": "ok",
                "mensaje": "\n".join(lines)
            }
            
        except Exception as e:
            return {
                "status": "error",
                "mensaje": f"❌ Error: {str(e)}"
            }
    
    # ============================================================
    # STATUS / REPORTES
    # ============================================================
    
    def status_despacho(self) -> dict:
        """Estado general del despacho."""
        try:
            matters = self._load_json(self.matters_file, [])
            alertas = self._load_json(self.alertas_file, [])
            
            activos = [m for m in matters if m.get("estado") in ["Activo", "Intake"]]
            pendientes = [a for a in alertas if a.get("estado") == "pendiente"]
            
            lines = [
                "📊 ESTADO DEL DESPACHO",
                "",
                f"📁 Matters activos: {len(activos)}",
                f"📢 Alertas pendientes: {len(pendientes)}",
                f"📊 Total matters: {len(matters)}",
                "",
                "🟢 MATTERS RECIENTES:"
            ]
            
            for m in matters[-5:]:
                lines.append(f"   {m['id']}: {m['nombre']} ({m['estado']})")
            
            return {
                "status": "ok",
                "mensaje": "\n".join(lines)
            }
            
        except Exception as e:
            return {
                "status": "error",
                "mensaje": f"❌ Error: {str(e)}"
            }
    
    # ============================================================
    # FINANZAS
    # ============================================================
    
    def registrar_finanza(self, matter_id: str, monto: float, concepto: str, tipo: str = "anticipo", **kwargs) -> dict:
        """
        Registrar un movimiento financiero.
        
        Args:
            matter_id: ID del matter
            monto: Monto en MXN
            concepto: Descripción del movimiento
            tipo: anticipo | honorario | factura | gasto
            
        Returns:
            dict con status, finanza_id, mensaje
        """
        try:
            finanzas = self._load_json(self.finanzas_file, [])
            
            monto_val = float(monto)
            finanza = {
                "id": f"FIN-{len(finanzas)+1:04d}",
                "matter_id": matter_id,
                "concepto": concepto,
                "monto": monto_val,
                "tipo": tipo,
                "estado": kwargs.get("estado", "pendiente"),
                "fecha": kwargs.get("fecha", datetime.now().strftime("%Y-%m-%d")),
                "notas": kwargs.get("notas", ""),
                "fecha_registro": datetime.now().isoformat()
            }
            
            finanzas.append(finanza)
            self._save_json(self.finanzas_file, finanzas)
            
            return {
                "status": "ok",
                "finanza_id": finanza["id"],
                "mensaje": f"✅ {tipo.upper()} registrado: {finanza['id']} — ${monto_val:,.2f} MXN\n   Matter: {matter_id}\n   Concepto: {concepto}"
            }
        except Exception as e:
            return {
                "status": "error",
                "mensaje": f"❌ Error registrando finanza: {str(e)}"
            }
    
    def ver_finanzas(self, matter_id: str = None) -> dict:
        """
        Ver movimientos financieros.
        
        Args:
            matter_id: (opcional) Filtrar por matter
            
        Returns:
            dict con status, mensaje formateado
        """
        try:
            finanzas = self._load_json(self.finanzas_file, [])
            
            if matter_id:
                movimientos = [f for f in finanzas if f["matter_id"] == matter_id]
                if not movimientos:
                    return {
                        "status": "ok",
                        "mensaje": f"📊 Sin movimientos para {matter_id}"
                    }
                
                total = sum(f["monto"] for f in movimientos)
                lines = [f"💰 Finanzas: {matter_id}", "─" * 40]
                for f in movimientos:
                    icon = "💵" if f["tipo"] == "anticipo" else "💼" if f["tipo"] == "honorario" else "🧾" if f["tipo"] == "factura" else "💸"
                    lines.append(f"{icon} {f['id']} | {f['tipo'].upper()} | ${f['monto']:,.2f} | {f['estado']}")
                    lines.append(f"   {f['concepto']} ({f['fecha']})")
                lines.append("─" * 40)
                lines.append(f"📈 Total: ${total:,.2f} MXN")
                
                return {
                    "status": "ok",
                    "mensaje": "\n".join(lines)
                }
            else:
                # Resumen global
                if not finanzas:
                    return {
                        "status": "ok",
                        "mensaje": "📊 Sin movimientos financieros registrados"
                    }
                
                total = sum(f["monto"] for f in finanzas)
                anticipos = sum(f["monto"] for f in finanzas if f["tipo"] == "anticipo")
                honorarios = sum(f["monto"] for f in finanzas if f["tipo"] == "honorario")
                
                return {
                    "status": "ok",
                    "mensaje": (
                        f"📊 Resumen Financiero\n"
                        f"─" * 40 + "\n"
                        f"💵 Anticipos: ${anticipos:,.2f}\n"
                        f"💼 Honorarios: ${honorarios:,.2f}\n"
                        f"📈 Total: ${total:,.2f} MXN\n"
                        f"📝 Movimientos: {len(finanzas)}"
                    )
                }
        except Exception as e:
            return {
                "status": "error",
                "mensaje": f"❌ Error: {str(e)}"
            }
    
    # ============================================================
    # HELPERS PRIVADOS
    # ============================================================
    
    def _load_json(self, path: Path, default):
        """Cargar JSON o retornar default."""
        if path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return default
    
    def _save_json(self, path: Path, data):
        """Guardar JSON con formato."""
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def _safe_name(self, name: str) -> str:
        """Convertir nombre a nombre de carpeta seguro."""
        return "".join(c if c.isalnum() or c in " _-" else "_" for c in name).strip().replace(" ", "_")
    
    def _crear_carpetas_matter(self, carpeta: str):
        """Crear estructura de carpetas para un matter."""
        base = Path(carpeta)
        subdirs = [
            "01_Intake",
            "02_Contratos/Borradores",
            "02_Contratos/Firmados",
            "03_Correspondencia/Entrante",
            "03_Correspondencia/Saliente",
            "04_Litigio",
            "05_Facturacion",
            "06_Entregables/Documentos_Finales",
            "07_Archivo"
        ]
        for sub in subdirs:
            (base / sub).mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    # Test básico
    cmd = HermesLegalCommands()
    print(cmd.crear_matter("Test_Hermes_Integration"))
    print(cmd.listar_matters())
    print(cmd.status_despacho())
