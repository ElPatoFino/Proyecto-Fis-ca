#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox
import math
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from fisica import (
    k_desde_fuerza,
    velocidad_inicial_resorte,
    fuerza_resorte,
    energia_potencial_elastica,
    alcance_horizontal,
    alcance_maximo,
    altura_maxima,
    tiempo_vuelo,
    trayectoria_desde_resorte,
    alcance_desde_resorte,
    v0_necesario,
    angulos_para_alcance,
    k_necesario,
    x_necesario,
    G_ESTANDARD
)


class AplicacionProyectil:
    def __init__(self, root):
        self.root = root
        self.root.title("Proyectil impulsado por resorte - Cálculos teóricos")
        self.root.geometry("940x900")
        self.root.resizable(True, True)
        
        # Estilo
        style = ttk.Style()
        style.theme_use('clam')
        
        # Notebook (pestañas)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Pestaña 1: Cálculo directo
        self.tab_directo = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_directo, text="  Cálculo directo (desde resorte)  ")
        self.crear_pestaña_directo()
        
        # Pestaña 2: Cálculo inverso
        self.tab_inverso = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_inverso, text="  Hallar variables (inverso)  ")
        self.crear_pestaña_inverso()
        
        # Pestaña 3: Gráfica de trayectoria
        self.tab_grafica = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_grafica, text="  Gráfica de trayectoria  ")
        self.crear_pestaña_grafica()
    
    def crear_pestaña_directo(self):
        # Frame de parámetros
        frame_param = ttk.LabelFrame(self.tab_directo, text="Parámetros del sistema", padding=10)
        frame_param.pack(fill='x', padx=10, pady=5)
        
        # k
        ttk.Label(frame_param, text="k (N/m):").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.k_directo = ttk.Entry(frame_param, width=15)
        self.k_directo.insert(0, "200.0")
        self.k_directo.grid(row=0, column=1, padx=5, pady=2)
        
        # x
        ttk.Label(frame_param, text="x (m):").grid(row=0, column=2, sticky='w', padx=5, pady=2)
        self.x_directo = ttk.Entry(frame_param, width=15)
        self.x_directo.insert(0, "0.15")
        self.x_directo.grid(row=0, column=3, padx=5, pady=2)
        
        # m
        ttk.Label(frame_param, text="m (kg):").grid(row=1, column=0, sticky='w', padx=5, pady=2)
        self.m_directo = ttk.Entry(frame_param, width=15)
        self.m_directo.insert(0, "0.2")
        self.m_directo.grid(row=1, column=1, padx=5, pady=2)
        
        # theta
        ttk.Label(frame_param, text="Ángulo θ (°):").grid(row=1, column=2, sticky='w', padx=5, pady=2)
        self.theta_directo = ttk.Entry(frame_param, width=15)
        self.theta_directo.insert(0, "45")
        self.theta_directo.grid(row=1, column=3, padx=5, pady=2)
        
        # g
        ttk.Label(frame_param, text="g (m/s²):").grid(row=2, column=0, sticky='w', padx=5, pady=2)
        self.g_directo = ttk.Entry(frame_param, width=15)
        self.g_directo.insert(0, str(G_ESTANDARD))
        self.g_directo.grid(row=2, column=1, padx=5, pady=2)
        
        # Botones
        frame_botones = ttk.Frame(self.tab_directo)
        frame_botones.pack(fill='x', padx=10, pady=5)
        ttk.Button(frame_botones, text="Calcular", command=self.calcular_directo).pack(side='left', padx=5)
        ttk.Button(frame_botones, text="Limpiar", command=self.limpiar_directo).pack(side='left', padx=5)
        
        # Frame de resultados
        frame_res = ttk.LabelFrame(self.tab_directo, text="Resultados", padding=10)
        frame_res.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.text_directo = tk.Text(frame_res, height=28, width=95, wrap='none')
        scrollbar_y = ttk.Scrollbar(frame_res, orient='vertical', command=self.text_directo.yview)
        scrollbar_x = ttk.Scrollbar(frame_res, orient='horizontal', command=self.text_directo.xview)
        self.text_directo.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        self.text_directo.grid(row=0, column=0, sticky='nsew')
        scrollbar_y.grid(row=0, column=1, sticky='ns')
        scrollbar_x.grid(row=1, column=0, sticky='ew')
        frame_res.grid_rowconfigure(0, weight=1)
        frame_res.grid_columnconfigure(0, weight=1)
    
    def crear_pestaña_inverso(self):
        # Frame 1: Hallar ángulos para alcance deseado
        frame_ang = ttk.LabelFrame(self.tab_inverso, text="Hallar ángulos para un alcance deseado", padding=10)
        frame_ang.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(frame_ang, text="v0 (m/s):").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.v0_ang = ttk.Entry(frame_ang, width=12)
        self.v0_ang.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(frame_ang, text="Alcance deseado R (m):").grid(row=0, column=2, sticky='w', padx=5, pady=2)
        self.r_ang = ttk.Entry(frame_ang, width=12)
        self.r_ang.grid(row=0, column=3, padx=5, pady=2)
        
        ttk.Label(frame_ang, text="g (m/s²):").grid(row=0, column=4, sticky='w', padx=5, pady=2)
        self.g_ang = ttk.Entry(frame_ang, width=12)
        self.g_ang.insert(0, str(G_ESTANDARD))
        self.g_ang.grid(row=0, column=5, padx=5, pady=2)
        
        ttk.Button(frame_ang, text="Calcular ángulos", command=self.calcular_angulos).grid(row=1, column=0, columnspan=6, pady=5)
        
        # Frame 2: Hallar v0 necesaria
        frame_v0n = ttk.LabelFrame(self.tab_inverso, text="Hallar v0 necesaria para un alcance deseado", padding=10)
        frame_v0n.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(frame_v0n, text="Ángulo θ (°):").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.theta_v0n = ttk.Entry(frame_v0n, width=12)
        self.theta_v0n.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(frame_v0n, text="Alcance deseado R (m):").grid(row=0, column=2, sticky='w', padx=5, pady=2)
        self.r_v0n = ttk.Entry(frame_v0n, width=12)
        self.r_v0n.grid(row=0, column=3, padx=5, pady=2)
        
        ttk.Label(frame_v0n, text="g (m/s²):").grid(row=0, column=4, sticky='w', padx=5, pady=2)
        self.g_v0n = ttk.Entry(frame_v0n, width=12)
        self.g_v0n.insert(0, str(G_ESTANDARD))
        self.g_v0n.grid(row=0, column=5, padx=5, pady=2)
        
        ttk.Button(frame_v0n, text="Calcular v0 necesaria", command=self.calcular_v0n).grid(row=1, column=0, columnspan=6, pady=5)
        
        # Frame 3: Hallar k o x necesarias
        frame_kx = ttk.LabelFrame(self.tab_inverso, text="Hallar k o x necesaria para obtener una v0 deseada", padding=10)
        frame_kx.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(frame_kx, text="v0 deseada (m/s):").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.v0_kx = ttk.Entry(frame_kx, width=12)
        self.v0_kx.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(frame_kx, text="m (kg):").grid(row=0, column=2, sticky='w', padx=5, pady=2)
        self.m_kx = ttk.Entry(frame_kx, width=12)
        self.m_kx.grid(row=0, column=3, padx=5, pady=2)
        
        ttk.Label(frame_kx, text="x (m) - para hallar k:").grid(row=1, column=0, sticky='w', padx=5, pady=2)
        self.x_k = ttk.Entry(frame_kx, width=12)
        self.x_k.grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(frame_kx, text="k (N/m) - para hallar x:").grid(row=1, column=2, sticky='w', padx=5, pady=2)
        self.k_x = ttk.Entry(frame_kx, width=12)
        self.k_x.grid(row=1, column=3, padx=5, pady=2)
        
        ttk.Button(frame_kx, text="Hallar k necesaria", command=self.calcular_kn).grid(row=2, column=0, columnspan=2, pady=5)
        ttk.Button(frame_kx, text="Hallar x necesaria", command=self.calcular_xn).grid(row=2, column=2, columnspan=2, pady=5)
        
        # Frame 4: Hallar k desde fuerza y deformación
        frame_fx = ttk.LabelFrame(self.tab_inverso, text="Hallar k desde fuerza y deformación (Ley de Hooke F = k·x)", padding=10)
        frame_fx.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(frame_fx, text="F (N):").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.f_fx = ttk.Entry(frame_fx, width=12)
        self.f_fx.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(frame_fx, text="x (m):").grid(row=0, column=2, sticky='w', padx=5, pady=2)
        self.x_fx = ttk.Entry(frame_fx, width=12)
        self.x_fx.grid(row=0, column=3, padx=5, pady=2)
        
        ttk.Button(frame_fx, text="Hallar k", command=self.calcular_k_desde_fx).grid(row=0, column=4, padx=10, pady=2)
        
        # Frame de resultados
        frame_res_inv = ttk.LabelFrame(self.tab_inverso, text="Resultados", padding=10)
        frame_res_inv.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.text_inverso = tk.Text(frame_res_inv, height=18, width=95, wrap='none')
        scrollbar2_y = ttk.Scrollbar(frame_res_inv, orient='vertical', command=self.text_inverso.yview)
        scrollbar2_x = ttk.Scrollbar(frame_res_inv, orient='horizontal', command=self.text_inverso.xview)
        self.text_inverso.configure(yscrollcommand=scrollbar2_y.set, xscrollcommand=scrollbar2_x.set)
        self.text_inverso.grid(row=0, column=0, sticky='nsew')
        scrollbar2_y.grid(row=0, column=1, sticky='ns')
        scrollbar2_x.grid(row=1, column=0, sticky='ew')
        frame_res_inv.grid_rowconfigure(0, weight=1)
        frame_res_inv.grid_columnconfigure(0, weight=1)
    
    def crear_pestaña_grafica(self):
        self.modo_escala = tk.StringVar(value="real")
        self.proporcion_manual = tk.BooleanVar(value=False)
        self._ultima_trayectoria = None
        
        frame_param = ttk.LabelFrame(self.tab_grafica, text="Parámetros del sistema", padding=10)
        frame_param.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(frame_param, text="k (N/m):").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.k_graf = ttk.Entry(frame_param, width=15)
        self.k_graf.insert(0, "200.0")
        self.k_graf.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(frame_param, text="x (m):").grid(row=0, column=2, sticky='w', padx=5, pady=2)
        self.x_graf = ttk.Entry(frame_param, width=15)
        self.x_graf.insert(0, "0.15")
        self.x_graf.grid(row=0, column=3, padx=5, pady=2)
        
        ttk.Label(frame_param, text="m (kg):").grid(row=1, column=0, sticky='w', padx=5, pady=2)
        self.m_graf = ttk.Entry(frame_param, width=15)
        self.m_graf.insert(0, "0.2")
        self.m_graf.grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(frame_param, text="Ángulo θ (°):").grid(row=1, column=2, sticky='w', padx=5, pady=2)
        self.theta_graf = ttk.Entry(frame_param, width=15)
        self.theta_graf.insert(0, "45")
        self.theta_graf.grid(row=1, column=3, padx=5, pady=2)
        
        ttk.Label(frame_param, text="g (m/s²):").grid(row=2, column=0, sticky='w', padx=5, pady=2)
        self.g_graf = ttk.Entry(frame_param, width=15)
        self.g_graf.insert(0, str(G_ESTANDARD))
        self.g_graf.grid(row=2, column=1, padx=5, pady=2)
        
        frame_escala = ttk.LabelFrame(self.tab_grafica, text="Escala de la gráfica", padding=10)
        frame_escala.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(frame_escala, text="Modo:").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        ttk.Radiobutton(
            frame_escala, text="Ajustada", variable=self.modo_escala, value="ajustada",
            command=self._cambiar_modo_escala
        ).grid(row=0, column=1, sticky='w', padx=5, pady=2)
        ttk.Radiobutton(
            frame_escala, text="Real 1:1", variable=self.modo_escala, value="real",
            command=self._cambiar_modo_escala
        ).grid(row=0, column=2, sticky='w', padx=5, pady=2)
        ttk.Radiobutton(
            frame_escala, text="Manual", variable=self.modo_escala, value="manual",
            command=self._cambiar_modo_escala
        ).grid(row=0, column=3, sticky='w', padx=5, pady=2)
        
        ttk.Label(frame_escala, text="x_min (m):").grid(row=1, column=0, sticky='w', padx=5, pady=2)
        self.xmin_manual = ttk.Entry(frame_escala, width=10)
        self.xmin_manual.grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(frame_escala, text="x_max (m):").grid(row=1, column=2, sticky='w', padx=5, pady=2)
        self.xmax_manual = ttk.Entry(frame_escala, width=10)
        self.xmax_manual.grid(row=1, column=3, padx=5, pady=2)
        
        ttk.Label(frame_escala, text="y_min (m):").grid(row=1, column=4, sticky='w', padx=5, pady=2)
        self.ymin_manual = ttk.Entry(frame_escala, width=10)
        self.ymin_manual.grid(row=1, column=5, padx=5, pady=2)
        
        ttk.Label(frame_escala, text="y_max (m):").grid(row=1, column=6, sticky='w', padx=5, pady=2)
        self.ymax_manual = ttk.Entry(frame_escala, width=10)
        self.ymax_manual.grid(row=1, column=7, padx=5, pady=2)
        
        self.chk_proporcion = ttk.Checkbutton(
            frame_escala, text="Mantener proporción 1:1", variable=self.proporcion_manual,
            command=self._al_cambiar_proporcion
        )
        self.chk_proporcion.grid(row=2, column=0, columnspan=2, sticky='w', padx=5, pady=2)
        
        self.btn_aplicar_escala = ttk.Button(
            frame_escala, text="Aplicar escala", command=self.aplicar_escala_manual
        )
        self.btn_aplicar_escala.grid(row=2, column=2, columnspan=2, padx=5, pady=2)
        
        self.btn_copiar_vista = ttk.Button(
            frame_escala, text="Copiar vista actual", command=self.copiar_vista_actual
        )
        self.btn_copiar_vista.grid(row=2, column=4, columnspan=3, padx=5, pady=2)
        
        frame_botones = ttk.Frame(self.tab_grafica)
        frame_botones.pack(fill='x', padx=10, pady=5)
        ttk.Button(frame_botones, text="Graficar trayectoria", command=self.graficar_trayectoria).pack(side='left', padx=5)
        ttk.Button(frame_botones, text="Limpiar", command=self.limpiar_grafica).pack(side='left', padx=5)
        
        frame_res = ttk.LabelFrame(self.tab_grafica, text="Resultados", padding=10)
        frame_res.pack(fill='x', padx=10, pady=5)
        
        self.resultado_graf = tk.StringVar(value="Ingresa los parámetros y presiona «Graficar trayectoria».")
        ttk.Label(frame_res, textvariable=self.resultado_graf, justify='left').pack(anchor='w')
        
        frame_canvas = ttk.LabelFrame(self.tab_grafica, text="Trayectoria parabólica", padding=5)
        frame_canvas.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.fig_graf = Figure(figsize=(7.5, 4.6), dpi=100)
        self.ax_graf = self.fig_graf.add_subplot(111)
        self.ax_graf.set_xlabel("x [m]")
        self.ax_graf.set_ylabel("y [m]")
        self.ax_graf.grid(True, linestyle='--', alpha=0.5)
        self.fig_graf.tight_layout()
        
        self.canvas_graf = FigureCanvasTkAgg(self.fig_graf, master=frame_canvas)
        self.toolbar_graf = NavigationToolbar2Tk(self.canvas_graf, frame_canvas, pack_toolbar=False)
        self.toolbar_graf.update()
        self.toolbar_graf.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas_graf.get_tk_widget().pack(side=tk.TOP, fill='both', expand=True)
        
        self._actualizar_estado_manual()
    
    def _entries_manuales(self):
        return (self.xmin_manual, self.xmax_manual, self.ymin_manual, self.ymax_manual)
    
    def _actualizar_estado_manual(self):
        estado = 'normal' if self.modo_escala.get() == 'manual' else 'disabled'
        for entry in self._entries_manuales():
            entry.configure(state=estado)
        self.chk_proporcion.configure(state=estado)
        self.btn_aplicar_escala.configure(state=estado)
        self.btn_copiar_vista.configure(state='normal')
    
    def _texto_modo(self):
        if self.modo_escala.get() == 'manual':
            return "Manual 1:1" if self.proporcion_manual.get() else "Manual"
        return "Real 1:1" if self.modo_escala.get() == 'real' else "Ajustada"
    
    def _sincronizar_campos_manuales(self):
        x_min, x_max = self.ax_graf.get_xlim()
        y_min, y_max = self.ax_graf.get_ylim()
        valores = (x_min, x_max, y_min, y_max)
        for entry, valor in zip(self._entries_manuales(), valores):
            entry.delete(0, tk.END)
            entry.insert(0, f"{valor:.6g}")
    
    def _leer_limites_manuales(self):
        try:
            x_min = float(self.xmin_manual.get())
            x_max = float(self.xmax_manual.get())
            y_min = float(self.ymin_manual.get())
            y_max = float(self.ymax_manual.get())
        except ValueError:
            raise ValueError("Los límites manuales deben ser números válidos")
        
        limites = (x_min, x_max, y_min, y_max)
        if not all(math.isfinite(v) for v in limites):
            raise ValueError("Los límites manuales deben ser finitos")
        if x_min >= x_max:
            raise ValueError("x_min debe ser menor que x_max")
        if y_min >= y_max:
            raise ValueError("y_min debe ser menor que y_max")
        
        return x_min, x_max, y_min, y_max
    
    def _limites_reales(self, xs, ys):
        x_min = min(0.0, min(xs))
        x_max = max(0.0, max(xs))
        y_min = min(0.0, min(ys))
        y_max = max(0.0, max(ys))
        span = max(x_max - x_min, y_max - y_min)
        if span <= 0:
            span = 1.0
        margen = 0.08 * span
        centro_x = (x_min + x_max) / 2
        return (
            centro_x - span / 2 - margen,
            centro_x + span / 2 + margen,
            y_min - margen,
            y_min + span + margen,
        )
    
    def _establecer_limites_manuales_iniciales(self, xs, ys):
        limites = self._limites_reales(xs, ys)
        for entry, valor in zip(self._entries_manuales(), limites):
            entry.delete(0, tk.END)
            entry.insert(0, f"{valor:.6g}")
    
    def _aplicar_vista_ajustada(self):
        self.ax_graf.set_aspect('auto')
        self.ax_graf.autoscale(enable=True, axis='both', tight=False)
        self.ax_graf.set_xmargin(0.08)
        self.ax_graf.set_ymargin(0.08)
        self.ax_graf.relim()
        self.ax_graf.autoscale_view()
    
    def _aplicar_vista_real(self):
        xs = self._ultima_trayectoria["xs"]
        ys = self._ultima_trayectoria["ys"]
        x_min, x_max, y_min, y_max = self._limites_reales(xs, ys)
        self.ax_graf.set_aspect('equal', adjustable='box')
        self.ax_graf.set_xlim(x_min, x_max)
        self.ax_graf.set_ylim(y_min, y_max)
    
    def _aplicar_vista_manual(self):
        x_min, x_max, y_min, y_max = self._leer_limites_manuales()
        
        if self.proporcion_manual.get():
            rango_x = x_max - x_min
            rango_y = y_max - y_min
            span = max(rango_x, rango_y)
            centro_x = (x_min + x_max) / 2
            centro_y = (y_min + y_max) / 2
            x_min = centro_x - span / 2
            x_max = centro_x + span / 2
            y_min = centro_y - span / 2
            y_max = centro_y + span / 2
            self.ax_graf.set_aspect('equal', adjustable='box')
        else:
            self.ax_graf.set_aspect('auto')
        
        self.ax_graf.set_xlim(x_min, x_max)
        self.ax_graf.set_ylim(y_min, y_max)
    
    def _aplicar_escala_actual(self):
        modo = self.modo_escala.get()
        if modo == 'ajustada':
            self._aplicar_vista_ajustada()
        elif modo == 'manual':
            self._aplicar_vista_manual()
        else:
            self._aplicar_vista_real()
    
    def _actualizar_resultados(self):
        datos = self._ultima_trayectoria
        if datos is None:
            return
        self.resultado_graf.set(
            f"v0 = {datos['v0']:.4f} m/s    |    R = {datos['R']:.4f} m    |    "
            f"H_max = {datos['Hmax']:.4f} m    |    T = {datos['Tvuelo']:.4f} s\n"
            f"Puntos graficados: {len(datos['xs'])}    |    Escala: {self._texto_modo()}    |    "
            f"Tiro parabólico sin resistencia del aire"
        )
    
    def _dibujar_trayectoria_actual(self):
        datos = self._ultima_trayectoria
        if datos is None:
            return
        
        xs = datos["xs"]
        ys = datos["ys"]
        
        self.ax_graf.clear()
        self.ax_graf.plot(xs, ys, color='#1f77b4', linewidth=2, label="Trayectoria")
        self.ax_graf.axhline(0, color='#555555', linewidth=0.8)
        
        if len(xs) > 1:
            idx_max = max(range(len(ys)), key=ys.__getitem__)
            x_pico = xs[idx_max]
            y_pico = ys[idx_max]
            self.ax_graf.plot([x_pico], [y_pico], marker='o', linestyle='none', color='#d62728', label="Altura máxima")
            self.ax_graf.annotate(
                f"H_max = {y_pico:.3f} m",
                xy=(x_pico, y_pico),
                xytext=(8, 8),
                textcoords='offset points',
                color='#d62728'
            )
            
            x_final = xs[-1]
            y_final = ys[-1]
            self.ax_graf.plot([x_final], [y_final], marker='s', linestyle='none', color='#2ca02c', label="Alcance")
            self.ax_graf.annotate(
                f"R = {x_final:.3f} m",
                xy=(x_final, y_final),
                xytext=(-10, 12),
                textcoords='offset points',
                color='#2ca02c',
                ha='right'
            )
        
        self.ax_graf.set_xlabel("x [m]")
        self.ax_graf.set_ylabel("y [m]")
        self.ax_graf.set_title(
            f"Trayectoria parabólica (k={datos['k']} N/m, x={datos['compresion']} m, "
            f"m={datos['m']} kg, θ={datos['theta']}°) - {self._texto_modo()}"
        )
        self.ax_graf.grid(True, linestyle='--', alpha=0.5)
        self.ax_graf.legend(loc='best')
        self._aplicar_escala_actual()
        self.fig_graf.tight_layout()
        self.canvas_graf.draw()
        self._actualizar_resultados()
    
    def _cambiar_modo_escala(self):
        self._actualizar_estado_manual()
        if self._ultima_trayectoria is None:
            return
        
        if self.modo_escala.get() == 'manual':
            self.proporcion_manual.set(bool(self.ax_graf.get_aspect() == 1.0))
            self._sincronizar_campos_manuales()
        
        try:
            self._dibujar_trayectoria_actual()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error al cambiar la escala: {str(e)}")
    
    def _al_cambiar_proporcion(self):
        if self.modo_escala.get() != 'manual' or self._ultima_trayectoria is None:
            return
        try:
            self._dibujar_trayectoria_actual()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error al cambiar la proporción: {str(e)}")
    
    def aplicar_escala_manual(self):
        if self._ultima_trayectoria is None:
            messagebox.showinfo("Sin trayectoria", "Primero grafica una trayectoria.")
            return
        try:
            if self.modo_escala.get() != 'manual':
                self.modo_escala.set('manual')
                self._actualizar_estado_manual()
            self._dibujar_trayectoria_actual()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error al aplicar la escala: {str(e)}")
    
    def copiar_vista_actual(self):
        if self._ultima_trayectoria is None:
            messagebox.showinfo("Sin trayectoria", "Primero grafica una trayectoria.")
            return
        self.proporcion_manual.set(bool(self.ax_graf.get_aspect() == 1.0))
        self.modo_escala.set('manual')
        self._actualizar_estado_manual()
        self._sincronizar_campos_manuales()
        self._actualizar_resultados()
    
    def graficar_trayectoria(self):
        try:
            k = float(self.k_graf.get())
            compresion = float(self.x_graf.get())
            m = float(self.m_graf.get())
            theta = float(self.theta_graf.get())
            g = float(self.g_graf.get())
            
            v0 = velocidad_inicial_resorte(k, compresion, m)
            xs, ys = trayectoria_desde_resorte(k, compresion, m, theta, g)
            R = alcance_horizontal(v0, theta, g)
            Hmax = altura_maxima(v0, theta, g)
            Tvuelo = tiempo_vuelo(v0, theta, g)
            
            if self.modo_escala.get() == 'manual' and any(
                not entry.get().strip() for entry in self._entries_manuales()
            ):
                self._establecer_limites_manuales_iniciales(xs, ys)
            
            self._ultima_trayectoria = {
                "xs": xs,
                "ys": ys,
                "k": k,
                "compresion": compresion,
                "m": m,
                "theta": theta,
                "g": g,
                "v0": v0,
                "R": R,
                "Hmax": Hmax,
                "Tvuelo": Tvuelo,
            }
            self._dibujar_trayectoria_actual()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error al graficar: {str(e)}")
    
    def limpiar_grafica(self):
        self.k_graf.delete(0, tk.END)
        self.x_graf.delete(0, tk.END)
        self.m_graf.delete(0, tk.END)
        self.theta_graf.delete(0, tk.END)
        self.g_graf.delete(0, tk.END)
        self.k_graf.insert(0, "200.0")
        self.x_graf.insert(0, "0.15")
        self.m_graf.insert(0, "0.2")
        self.theta_graf.insert(0, "45")
        self.g_graf.insert(0, str(G_ESTANDARD))
        
        self.modo_escala.set('real')
        self.proporcion_manual.set(False)
        for entry in self._entries_manuales():
            entry.configure(state='normal')
            entry.delete(0, tk.END)
        self._actualizar_estado_manual()
        self._ultima_trayectoria = None
        
        self.resultado_graf.set("Ingresa los parámetros y presiona «Graficar trayectoria».")
        self.ax_graf.clear()
        self.ax_graf.set_aspect('auto')
        self.ax_graf.set_xlabel("x [m]")
        self.ax_graf.set_ylabel("y [m]")
        self.ax_graf.grid(True, linestyle='--', alpha=0.5)
        self.fig_graf.tight_layout()
        self.canvas_graf.draw()
    
    def calcular_directo(self):
        try:
            k = float(self.k_directo.get())
            x = float(self.x_directo.get())
            m = float(self.m_directo.get())
            theta = float(self.theta_directo.get())
            g = float(self.g_directo.get())
            
            v0 = velocidad_inicial_resorte(k, x, m)
            F = fuerza_resorte(k, x)
            E = energia_potencial_elastica(k, x)
            R = alcance_horizontal(v0, theta, g)
            Rmax = alcance_maximo(v0, g)
            Hmax = altura_maxima(v0, theta, g)
            Tvuelo = tiempo_vuelo(v0, theta, g)
            
            self.text_directo.delete('1.0', tk.END)
            self.text_directo.insert(tk.END, "=" * 55 + "\n")
            self.text_directo.insert(tk.END, "CÁLCULO DESDE CARACTERÍSTICAS DEL RESORTE\n")
            self.text_directo.insert(tk.END, "=" * 55 + "\n\n")
            
            self.text_directo.insert(tk.END, "PARÁMETROS:\n")
            self.text_directo.insert(tk.END, f"  k = {k} N/m | x = {x} m | m = {m} kg | θ = {theta}° | g = {g} m/s²\n\n")
            
            self.text_directo.insert(tk.END, "ENERGÍA Y FUERZA:\n")
            self.text_directo.insert(tk.END, f"  Energía elástica E = (1/2)k x² = {E:.4f} J\n")
            self.text_directo.insert(tk.END, f"  Fuerza máxima F = k·x = {F:.3f} N (Ley de Hooke)\n\n")
            
            self.text_directo.insert(tk.END, "VELOCIDAD INICIAL:\n")
            self.text_directo.insert(tk.END, f"  v0 = sqrt((k x²)/m) = {v0:.4f} m/s\n\n")
            
            self.text_directo.insert(tk.END, "TRAYECTORIA (tiro parabólico, sin resistencia del aire):\n")
            self.text_directo.insert(tk.END, f"  Alcance R (θ={theta}°) = {R:.4f} m\n")
            self.text_directo.insert(tk.END, f"  Alcance máximo R_max (45°) = {Rmax:.4f} m\n")
            self.text_directo.insert(tk.END, f"  Altura máxima H_max = {Hmax:.4f} m\n")
            self.text_directo.insert(tk.END, f"  Tiempo de vuelo T = {Tvuelo:.4f} s\n\n")
            
            self.text_directo.insert(tk.END, "=" * 55 + "\n")
            self.text_directo.insert(tk.END, "Nota: F=kx y E=(1/2)kx² son distintos (resorte ideal)\n")
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except ZeroDivisionError:
            messagebox.showerror("Error", "Valores inválidos (división por cero)")
        except Exception as e:
            messagebox.showerror("Error", f"Error en los cálculos: {str(e)}")
    
    def limpiar_directo(self):
        self.k_directo.delete(0, tk.END)
        self.x_directo.delete(0, tk.END)
        self.m_directo.delete(0, tk.END)
        self.theta_directo.delete(0, tk.END)
        self.g_directo.delete(0, tk.END)
        self.k_directo.insert(0, "200.0")
        self.x_directo.insert(0, "0.15")
        self.m_directo.insert(0, "0.2")
        self.theta_directo.insert(0, "45")
        self.g_directo.insert(0, str(G_ESTANDARD))
        self.text_directo.delete('1.0', tk.END)
    
    def calcular_angulos(self):
        try:
            v0 = float(self.v0_ang.get())
            Rdes = float(self.r_ang.get())
            g = float(self.g_ang.get())
            
            angs = angulos_para_alcance(v0, Rdes, g)
            Rmax = alcance_maximo(v0, g)
            
            self.text_inverso.delete('1.0', tk.END)
            self.text_inverso.insert(tk.END, "--- ÁNGULOS PARA ALCANCE DESEADO ---\n\n")
            self.text_inverso.insert(tk.END, f"v0 = {v0} m/s | R_deseado = {Rdes} m | R_max = {Rmax:.4f} m\n\n")
            
            if angs is None:
                self.text_inverso.insert(tk.END, "✗ NO ES FÍSICAMENTE POSIBLE\n")
                self.text_inverso.insert(tk.END, f"El alcance deseado ({Rdes} m) supera el alcance máximo ({Rmax:.4f} m)\n")
            elif Rdes == 0:
                self.text_inverso.insert(tk.END, "Para alcance 0 m: θ = 0°\n")
            else:
                self.text_inverso.insert(tk.END, "✓ POSIBLE\n\n")
                self.text_inverso.insert(tk.END, f"Ángulo 1: θ1 = {angs[0]:.2f}°\n")
                self.text_inverso.insert(tk.END, f"Ángulo 2: θ2 = {angs[1]:.2f}°\n\n")
                self.text_inverso.insert(tk.END, "(Son complementarios: θ1 + θ2 = 90°)\n")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def calcular_v0n(self):
        try:
            theta = float(self.theta_v0n.get())
            Rdes = float(self.r_v0n.get())
            g = float(self.g_v0n.get())
            
            v0n = v0_necesario(Rdes, theta, g)
            Rmax_posible = alcance_maximo(v0n, g)
            
            self.text_inverso.delete('1.0', tk.END)
            self.text_inverso.insert(tk.END, "--- v0 NECESARIA PARA ALCANCE DESEADO ---\n\n")
            self.text_inverso.insert(tk.END, f"θ = {theta}° | R_deseado = {Rdes} m\n\n")
            self.text_inverso.insert(tk.END, f"v0 necesaria = {v0n:.4f} m/s\n")
            self.text_inverso.insert(tk.END, f"(Con esta v0, R_max teórico = {Rmax_posible:.4f} m a 45°)\n")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def calcular_kn(self):
        try:
            v0d = float(self.v0_kx.get())
            x = float(self.x_k.get())
            m = float(self.m_kx.get())
            
            k_req = k_necesario(v0d, x, m)
            F_req = k_req * x
            E_req = 0.5 * k_req * x**2
            
            self.text_inverso.delete('1.0', tk.END)
            self.text_inverso.insert(tk.END, "--- k NECESARIA ---\n\n")
            self.text_inverso.insert(tk.END, f"v0 deseada = {v0d} m/s | x = {x} m | m = {m} kg\n\n")
            self.text_inverso.insert(tk.END, f"k necesaria = {k_req:.2f} N/m\n")
            self.text_inverso.insert(tk.END, f"Fuerza máxima F = k·x = {F_req:.2f} N\n")
            self.text_inverso.insert(tk.END, f"Energía (1/2)kx² = {E_req:.4f} J\n")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def calcular_xn(self):
        try:
            v0d = float(self.v0_kx.get())
            k = float(self.k_x.get())
            m = float(self.m_kx.get())
            
            x_req = x_necesario(v0d, k, m)
            F_req = k * x_req
            E_req = 0.5 * k * x_req**2
            
            self.text_inverso.delete('1.0', tk.END)
            self.text_inverso.insert(tk.END, "--- x NECESARIA ---\n\n")
            self.text_inverso.insert(tk.END, f"v0 deseada = {v0d} m/s | k = {k} N/m | m = {m} kg\n\n")
            self.text_inverso.insert(tk.END, f"x necesaria = {x_req:.4f} m ({x_req*100:.2f} cm)\n")
            self.text_inverso.insert(tk.END, f"Fuerza máxima F = k·x = {F_req:.2f} N\n")
            self.text_inverso.insert(tk.END, f"Energía (1/2)kx² = {E_req:.4f} J\n")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def calcular_k_desde_fx(self):
        try:
            f = float(self.f_fx.get())
            x = float(self.x_fx.get())
            
            k_req = k_desde_fuerza(f, x)
            E_req = 0.5 * k_req * x**2
            
            self.text_inverso.delete('1.0', tk.END)
            self.text_inverso.insert(tk.END, "--- k DESDE FUERZA Y DEFORMACIÓN ---\n\n")
            self.text_inverso.insert(tk.END, f"F = {f} N | x = {x} m\n\n")
            self.text_inverso.insert(tk.END, f"k = F/x = {k_req:.2f} N/m\n")
            self.text_inverso.insert(tk.END, f"Energía almacenada (1/2)kx² = {E_req:.4f} J\n")
            self.text_inverso.insert(tk.END, f"Fuerza máxima con esta k y x = {f:.2f} N\n")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionProyectil(root)
    root.mainloop()
