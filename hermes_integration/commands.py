#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hermes Legal Commands — Parser de comandos Telegram para operación legal.

Uso:
    from hermes_integration.commands import HermesLegalCommands
    cmd = HermesLegalCommands()
    result = cmd.crear_matter("Innovatech Digital")
    print(result["mensaje"])

v2.0: Migrado a usar config.yaml + JSONDatastore + IDGenerator
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# v2.0: Importar core
sys.path.insert(0, str(Path(__file__).parent.parent))
from config.config_loader import Config
from core.datastore import JSONDatastore
from core.id_generator import IDGenerator


class HermesLegalCommands:
    """
    Interfaz de comandos para operación legal via Hermes Agent.
    
    v2.0: Usa configuración centralizada y datastore unificado.
    """
    
    def __init__(self, base_dir=None):
        """
        Inicializar con configuración centralizada.
        
        Args:
            base_dir: (legacy, ignorado en v2.0) Se usa config.datastore.path
        """
        # v2.0: Configuración centralizada
        self.config = Config.load()
        self.datastore = JSONDatastore(
            self.config.datastore.path,
            self.config.datastore.backup_dir
        )
        self.id_generator = IDGenerator(self.datastore, self.config.ids if isinstance(self.config.ids, dict) else self.config.ids.__dict__)
        
        # v2.0: Referencia al repo para templates y motor
        self.repo_dir = Path(__file__).parent.parent
        self.motor_dir = self.repo_dir / "motor_kami"
    
    # ============================================================
    # HELPERS
    # ============================================================
    
    def _safe_name(self, nombre: str) -> str:
        return "".join(c for c in nombre if c.isalnum() or c in " _-").strip()
    
    def _crear_carpetas_matter(self, carpeta_path: str):
        base = Path(carpeta_path)
        subcarpetas = [
            "01_Intake",
            "02_Contratos/Borradores",
            "02_Contratos/Firmados",
            "02_Contratos/Anexos",
            "03_Correspondencia/Entrante",
            "03_Correspondencia/Saliente",
            "04_Litigio/Demandas",
            "04_Litigio/Contestaciones",
            "04_Litigio/Pruebas",
            "04_Litigio/Audiencias",
            "05_Facturacion/Cotizaciones",
            "05_Facturacion/Facturas",
            "05_Facturacion/Pagos",
            "06_Entregables/Documentos_Finales",
            "06_Entregables/Presentaciones",
            "06_Entregables/Reportes",
            "07_Archivo/Cerrado"
        ]
        for sub in subcarpetas:
            (base / sub).mkdir(parents=True, exist_ok=True)
        return base
    
    # ============================================================
    # MATTERS
    # ============================================================
    
    def crear_matter(self, nombre: str, **kwargs) -> dict:
        """
        Crear nuevo matter desde comando Telegram.
        
        v2.0: Usa IDGenerator para IDs WIL-XXX y datastore para persistencia.
        """
        try:
            # v2.0: Generar ID via IDGenerator
            matter_id = self.id_generator.generate_matter_id()
            
            # v2.0: Crear matter con estructura unificada
            matter = {
                "id": matter_id,
                "nombre": nombre,
                "cliente": kwargs.get("cliente", nombre),
                "estado": "activo",
                "area_practica": kwargs.get("area", "Mercantil"),
                "materia": kwargs.get("materia", "corporativo"),
                "prioridad": kwargs.get("prioridad", "media"),
                "descripcion": kwargs.get("descripcion", ""),
                "fecha_creacion": datetime.now().isoformat(),
                "actualizado": datetime.now().isoformat(),
                "next_step": "Intake inicial pendiente",
                "blocker": "none",
                "carpeta": str(Path.home() / "WillowLegal" / "01_Clientes" / self._safe_name(nombre)),
                "deadline": kwargs.get("deadline", None),
                "reuniones": [],
                "documentos": [],
                "tareas": []
            }
            
            # v2.0: Guardar via datastore
            self.datastore.insert("matters", matter)
            
            # Crear estructura de carpetas
            self._crear_carpetas_matter(matter["carpeta"])
            
            # Crear en Drive (usar token existente)
            try:
                from scripts.drive_manager import DriveManager
                dm = DriveManager()
                drive_folder_id = dm.create_client_structure(matter["cliente"])
                matter["drive_folder_id"] = drive_folder_id
                matter["drive_link"] = f"https://drive.google.com/drive/folders/{drive_folder_id}"
                # Actualizar en datastore
                self.datastore.update("matters", "id", matter_id, {
                    "drive_folder_id": drive_folder_id,
                    "drive_link": matter["drive_link"]
                })
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
                    f"🏷️  Área: {matter['area_practica']}\n"
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
            matters = self.datastore.get("matters")
            
            if not matters:
                return {
                    "status": "ok",
                    "mensaje": "📭 No hay matters registrados"
                }
            
            lines = ["📋 MATTERS ACTIVOS:"]
            for m in matters[-limite:]:
                emoji = "🟢" if m.get("estado") == "activo" else "🟡" if m.get("estado") == "Intake" else "🔴"
                drive_icon = "📁" if m.get("drive_folder_id") else "❌"
                lines.append(f"  {emoji} {m['id']}: {m.get('nombre', m.get('cliente', 'Sin nombre'))} {drive_icon}")
            
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
            matter = self.datastore.find_one("matters", id=matter_id)
            
            if not matter:
                return {
                    "status": "error",
                    "mensaje": f"❌ Matter {matter_id} no encontrado"
                }
            
            return {
                "status": "ok",
                "mensaje": (
                    f"📋 {matter['id']}: {matter.get('nombre', matter.get('cliente', 'N/A'))}\n"
                    f"   Estado: {matter['estado']}\n"
                    f"   Área: {matter.get('area_practica', matter.get('area', 'N/A'))}\n"
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
        
        v2.0: Usa generar_documento_real() directamente — no subprocess.
        """
        try:
            # Verificar template existe
            template_file = self.motor_dir / "templates" / f"{template}.json"
            if not template_file.exists():
                templates_dir = self.motor_dir / "templates"
                disponibles = [f.stem for f in templates_dir.glob("*.json") if f.stem != "index"]
                return {
                    "status": "error",
                    "mensaje": (
                        f"❌ Template '{template}' no encontrado\n"
                        f"📋 Disponibles: {', '.join(disponibles[:10])}"
                    )
                }
            
            # Obtener datos del matter
            matter = self.datastore.find_one("matters", id=matter_id) if matter_id else None
            
            # v2.0: Usar despacho desde config
            despacho_data = {
                "nombre": self.config.despacho.nombre,
                "rfc": self.config.despacho.rfc,
                "representante": self.config.despacho.representante,
                "email": self.config.despacho.email,
                "domicilio": self.config.despacho.domicilio,
            }
            
            # Preparar output path
            output_dir = Path(self.config.motor_kami.get('output_dir', '~/.willowlegal/output/')).expanduser()
            output_dir.mkdir(parents=True, exist_ok=True)
            output_filename = kwargs.get("output_filename", f"{matter_id}_{template}.pdf" if matter_id else f"{template}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
            output_path = output_dir / output_filename
            
            # v2.0: Llamar generar_documento_real() directamente
            from motor_kami.motor_kami import generar_documento_real
            
            result = generar_documento_real(
                template_key=template,
                matter_data=matter or {},
                output_path=output_path,
                extra_vars=kwargs.get("variables", {}),
                despacho_data=despacho_data
            )
            
            if not result.get("success"):
                return {
                    "status": "error",
                    "mensaje": f"❌ Error del Motor Kami: {result.get('error', 'Desconocido')}"
                }
            
            # v2.0: Registrar documento en datastore
            doc_id = self.id_generator.generate_document_id()
            self.datastore.insert("documentos", {
                "id": doc_id,
                "matter_id": matter_id,
                "template_key": template,
                "estado": "generado",
                "fecha_creacion": datetime.now().isoformat(),
                "ruta_pdf": str(output_path),
                "ruta_editable": str(output_path.with_suffix(".html"))
            })
            
            mensaje = (
                f"📝 Documento generado:\n"
                f"   Template: {result.get('template_label', template)}\n"
                f"   📄 {output_filename}\n"
                f"   📁 {output_dir}"
            )
            
            # Subir a Drive si el matter tiene carpeta
            if matter and matter.get("drive_folder_id"):
                try:
                    from scripts.drive_manager import DriveManager
                    dm = DriveManager()
                    cliente_nombre = matter.get("cliente", matter.get("nombre", "Cliente"))
                    drive_result = dm.upload_pdf(str(output_path), cliente_nombre)
                    mensaje += f"\n📤 Drive: {drive_result.get('link', 'OK')}"
                except Exception as e:
                    mensaje += f"\n⚠️  Drive: {e}"
            
            return {
                "status": "ok",
                "mensaje": mensaje,
                "pdf_path": str(output_path),
                "documento_id": doc_id
            }
                
        except Exception as e:
            return {
                "status": "error",
                "mensaje": f"❌ Error generando documento: {str(e)}"
            }
    
    def listar_templates(self) -> dict:
        """Listar templates disponibles."""
        try:
            templates_dir = self.motor_dir / "templates"
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
            plazo_id = self.id_generator.generate_plazo_id()
            
            plazo = {
                "id": plazo_id,
                "matter_id": matter_id,
                "descripcion": descripcion,
                "fecha_vencimiento": fecha,
                "tipo": kwargs.get("tipo", "plazo"),
                "estado": "pendiente",
                "creado": datetime.now().isoformat()
            }
            
            self.datastore.insert("plazos", plazo)
            
            # Crear alerta asociada
            alerta_id = self.id_generator.generate_alerta_id()
            self.datastore.insert("alertas", {
                "id": alerta_id,
                "matter_id": matter_id,
                "titulo": f"Plazo: {descripcion}",
                "tipo": "plazo",
                "fecha": fecha,
                "estado": "pendiente",
                "creado": datetime.now().isoformat()
            })
            
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
                
                self.datastore.update("plazos", "id", plazo_id, {
                    "calendar_event_id": cal_result['id'],
                    "calendar_link": cal_result['link']
                })
                
                mensaje_extra = f"\n📅 Calendar: {cal_result['link']}"
            except Exception as e:
                print(f"⚠️  Calendar: {e}")
            
            return {
                "status": "ok",
                "mensaje": (
                    f"📅 Plazo creado: {plazo_id}\n"
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
            alertas = self.datastore.get("alertas")
            
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
                lines.append(f"  • {a['id']}: {a.get('titulo', a.get('descripcion', 'Sin título'))} (vence: {a['fecha']})")
            
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
            matters = self.datastore.get("matters")
            alertas = self.datastore.get("alertas")
            
            activos = [m for m in matters if m.get("estado") in ["activo", "Intake"]]
            pendientes = [a for a in alertas if a.get("estado") == "pendiente"]
            
            lines = [
                f"📊 ESTADO DEL DESPACHO — {self.config.despacho.nombre}",
                "",
                f"📁 Matters activos: {len(activos)}",
                f"📢 Alertas pendientes: {len(pendientes)}",
                f"📊 Total matters: {len(matters)}",
                "",
                "🟢 MATTERS RECIENTES:"
            ]
            
            for m in matters[-5:]:
                lines.append(f"   {m['id']}: {m.get('nombre', m.get('cliente', 'N/A'))} ({m['estado']})")
            
            return {
                "status": "ok",
                "mensaje": "\n".join(lines),
                "resumen": {
                    "activos": len(activos),
                    "pendientes": len(pendientes),
                    "total": len(matters)
                }
            }
            
        except Exception as e:
            return {
                "status": "error",
                "mensaje": f"❌ Error: {str(e)}"
            }
    
    def exportar_resumen(self) -> dict:
        """Exportar resumen a formato texto."""
        try:
            matters = self.datastore.get("matters")
            finanzas = self.datastore.get("finanzas")
            
            movimientos = finanzas.get("movimientos", []) if isinstance(finanzas, dict) else []
            total_ingresos = sum(m["monto"] for m in movimientos if m.get("tipo") in ["ingreso", "anticipo", "pago", "honorario"])
            total_egresos = sum(m["monto"] for m in movimientos if m.get("tipo") in ["egreso", "gasto"])
            
            lines = [
                f"📊 RESUMEN FINANCIERO — {self.config.despacho.nombre}",
                "",
                f"💰 Ingresos: ${total_ingresos:,.2f}",
                f"💸 Egresos: ${total_egresos:,.2f}",
                f"📈 Balance: ${total_ingresos - total_egresos:,.2f}",
                "",
                f"📁 Total matters: {len(matters)}"
            ]
            
            return {
                "status": "ok",
                "mensaje": "\n".join(lines)
            }
            
        except Exception as e:
            return {
                "status": "error",
                "mensaje": f"❌ Error: {str(e)}"
            }
