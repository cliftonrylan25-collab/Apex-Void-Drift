import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import random
import datetime
import math

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="A.P.E.X. VOID DRIFT",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# ADVANCED CSS INJECTION (THE "PRO" UI)
# ==========================================
ADVANCED_CSS = """
<style>
/* Import High-Tech Fonts */
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700;900&family=Rajdhani:wght@300;500;600;700&family=Share+Tech+Mono&display=swap');

/* Base Theme & Animated Background */
.stApp {
    background-color: #030509;
    background-image: 
        radial-gradient(circle at 15% 50%, rgba(12, 20, 36, 0.8), transparent 25%),
        radial-gradient(circle at 85% 30%, rgba(19, 15, 40, 0.8), transparent 25%);
    background-attachment: fixed;
    color: #e2e8f0;
    font-family: 'Rajdhani', sans-serif !important;
}

/* Hide standard Streamlit elements */
#MainMenu, footer, header {visibility: hidden;}

/* Global Typography */
h1, h2, h3, .stTabs [data-baseweb="tab"] p {
    font-family: 'Orbitron', sans-serif !important;
    text-transform: uppercase;
    letter-spacing: 1.5px;
}

h1 {
    color: #f8fafc !important;
    text-shadow: 0 0 15px rgba(56, 189, 248, 0.6), 0 0 30px rgba(56, 189, 248, 0.2);
    font-weight: 900 !important;
}

h3 {
    color: #38bdf8 !important;
    font-size: 1.2rem !important;
    margin-bottom: 1rem !important;
    border-bottom: 1px solid rgba(56, 189, 248, 0.2);
    padding-bottom: 0.5rem;
}

/* Glassmorphism Cards */
.cyber-card {
    background: rgba(10, 15, 25, 0.6);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(56, 189, 248, 0.15);
    border-top: 3px solid #38bdf8;
    border-radius: 6px;
    padding: 20px;
    margin-bottom: 15px;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    transition: all 0.3s ease;
    overflow-wrap: break-word;
}
.cyber-card:hover {
    border-color: rgba(56, 189, 248, 0.4);
    box-shadow: 0 8px 32px 0 rgba(56, 189, 248, 0.15);
}
.cyber-card.danger { border-top-color: #ef4444; }
.cyber-card.warning { border-top-color: #f59e0b; }
.cyber-card.success { border-top-color: #10b981; }
.cyber-card.purple { border-top-color: #8b5cf6; }

/* Metrics */
.metric-title {
    font-size: 0.75rem;
    color: #94a3b8;
    text-transform: uppercase;
    font-weight: 700;
    letter-spacing: 1px;
    margin-bottom: 5px;
}
.metric-value {
    font-size: 1.5rem;
    color: #f8fafc;
    font-weight: 700;
    font-family: 'Share Tech Mono', monospace;
    text-shadow: 0 0 10px rgba(255, 255, 255, 0.2);
}

/* CRT Terminal Console */
.console-wrapper {
    position: relative;
    background: #020408;
    border: 1px solid #1e293b;
    border-left: 4px solid #8b5cf6;
    border-radius: 4px;
    padding: 15px;
    height: 400px;
    overflow-y: auto;
    box-shadow: inset 0 0 20px rgba(0,0,0,0.8);
}
.console-wrapper::after {
    content: " ";
    display: block;
    position: absolute;
    top: 0; left: 0; bottom: 0; right: 0;
    background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
    z-index: 2;
    background-size: 100% 2px, 3px 100%;
    pointer-events: none;
}
.console-log {
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.85rem;
    color: #a78bfa;
    text-shadow: 0 0 5px rgba(167, 139, 250, 0.4);
    line-height: 1.5;
}
.console-log span {
    display: block;
    margin-bottom: 4px;
    border-bottom: 1px dashed rgba(30, 41, 59, 0.5);
    padding-bottom: 4px;
}
.console-log span:first-child {
    color: #e2e8f0;
    text-shadow: 0 0 8px rgba(255,255,255,0.6);
}

/* Custom Cyber Buttons */
.stButton>button {
    background: rgba(15, 23, 42, 0.7) !important;
    color: #38bdf8 !important;
    border: 1px solid #38bdf8 !important;
    border-radius: 2px !important;
    font-family: 'Orbitron', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 1px;
    text-transform: uppercase;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    width: 100%;
    padding: 0.75rem !important;
    box-shadow: inset 0 0 0 rgba(56, 189, 248, 0);
    white-space: pre-wrap !important;
    height: auto !important;
    min-height: 3rem;
}
.stButton>button:hover {
    background: rgba(56, 189, 248, 0.1) !important;
    color: #ffffff !important;
    box-shadow: inset 0 0 15px rgba(56, 189, 248, 0.3), 0 0 15px rgba(56, 189, 248, 0.4) !important;
    transform: translateY(-1px);
}

/* Contextual Button Colors via HTML Wrappers */
.btn-combat>button { border-color: #ef4444 !important; color: #ef4444 !important; }
.btn-combat>button:hover { background: rgba(239, 68, 68, 0.1) !important; box-shadow: inset 0 0 15px rgba(239, 68, 68, 0.3), 0 0 15px rgba(239, 68, 68, 0.4) !important; color:#fff !important;}

.btn-evade>button { border-color: #f59e0b !important; color: #f59e0b !important; }
.btn-evade>button:hover { background: rgba(245, 158, 11, 0.1) !important; box-shadow: inset 0 0 15px rgba(245, 158, 11, 0.3), 0 0 15px rgba(245, 158, 11, 0.4) !important; color:#fff !important;}

.btn-launch>button { border-color: #10b981 !important; color: #10b981 !important; }
.btn-launch>button:hover { background: rgba(16, 185, 129, 0.1) !important; box-shadow: inset 0 0 15px rgba(16, 185, 129, 0.3), 0 0 15px rgba(16, 185, 129, 0.4) !important; color:#fff !important;}

/* Animated Progress Bars */
.progress-container {
    width: 100%;
    background-color: rgba(30, 41, 59, 0.5);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 3px;
    margin-top: 5px;
    height: 12px;
    overflow: hidden;
    position: relative;
}
.progress-fill {
    height: 100%;
    transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}
.progress-fill::after {
    content: "";
    position: absolute;
    top: 0; left: 0; bottom: 0; right: 0;
    background: linear-gradient(90deg, rgba(255,255,255,0) 0%, rgba(255,255,255,0.3) 50%, rgba(255,255,255,0) 100%);
    animation: shimmer 2s infinite;
}
@keyframes shimmer {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}

/* Tabs Styling */
.stTabs [data-baseweb="tab-list"] {
    background-color: transparent;
    gap: 10px;
}
.stTabs [data-baseweb="tab"] {
    background-color: rgba(15, 23, 42, 0.4);
    border: 1px solid rgba(56, 189, 248, 0.2);
    border-bottom: none;
    border-radius: 4px 4px 0 0;
    color: #94a3b8;
    transition: all 0.2s;
}
.stTabs [aria-selected="true"] {
    background-color: rgba(56, 189, 248, 0.1);
    color: #38bdf8 !important;
    border-color: #38bdf8;
    box-shadow: 0 -4px 15px rgba(56, 189, 248, 0.15);
}

/* Popover / Info Button */
.popover-help-btn button {
    border-color: #c084fc !important;
    color: #c084fc !important;
    border-radius: 50% !important;
    width: 40px !important;
    height: 40px !important;
    min-height: unset !important;
    padding: 0 !important;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-left: auto;
}
.popover-help-btn button:hover {
    background: rgba(192, 132, 252, 0.2) !important;
    box-shadow: 0 0 15px rgba(192, 132, 252, 0.5) !important;
}

hr { border-color: rgba(56, 189, 248, 0.2); margin: 2rem 0; }
</style>
"""
st.markdown(ADVANCED_CSS, unsafe_allow_html=True)

# ==========================================
# GAME CONSTANTS & DATABASES
# ==========================================
SCRAP_DB = {
    "Iron-Carbon": {"base": 15, "volatility": 0.05, "weight": 2.0, "rarity": 1},
    "Copper Spools": {"base": 30, "volatility": 0.08, "weight": 1.5, "rarity": 1},
    "Titanium Struts": {"base": 75, "volatility": 0.12, "weight": 4.0, "rarity": 2},
    "Quantum Circuits": {"base": 180, "volatility": 0.25, "weight": 0.5, "rarity": 3},
    "Isotope Cells": {"base": 400, "volatility": 0.40, "weight": 5.0, "rarity": 4},
    "Dark Matter": {"base": 2500, "volatility": 0.60, "weight": 1.0, "rarity": 5}
}

UPGRADE_TREE = {
    "hull": {
        "name": "Ablative Armor",
        "desc": "Reinforces max Hull Integrity.",
        "base_cost": 500, "cost_mult": 1.8, "effect": 75
    },
    "fuel": {
        "name": "Propellant Tanks",
        "desc": "Expands Delta-v capacity.",
        "base_cost": 400, "cost_mult": 1.5, "effect": 150
    },
    "cargo": {
        "name": "Void Cargo Bay",
        "desc": "Increases maximum tonnage capacity.",
        "base_cost": 800, "cost_mult": 1.7, "effect": 35
    },
    "sohc4v": {
        "name": "SOHC-4V Plasma Head",
        "desc": "Highly efficient plasma valvetrain. Reduces fuel consumption by 12% per level.",
        "base_cost": 1500, "cost_mult": 2.2, "effect": 0.12
    },
    "radar": {
        "name": "L.O.O.T. Array",
        "desc": "Extends radar range and enhances rare anomaly detection.",
        "base_cost": 2000, "cost_mult": 2.5, "effect": 1
    },
    "weapons": {
        "name": "Kinetic Interceptors",
        "desc": "Automated defense cannons. Increases combat survival rate.",
        "base_cost": 1200, "cost_mult": 2.0, "effect": 15
    },
    "apex": {
        "name": "A.P.E.X. Core",
        "desc": "Advanced Predictive Executive matrix. Grants tactical evasion and auto-repairs.",
        "base_cost": 5000, "cost_mult": 3.0, "effect": 0.08
    }
}

# ==========================================
# CORE CLASSES
# ==========================================
class DynamicMarket:
    def __init__(self):
        self.history = {k: [v['base']] for k, v in SCRAP_DB.items()}
        self.current_prices = {k: v['base'] for k, v in SCRAP_DB.items()}
        self.trend_cycles = {k: 0 for k in SCRAP_DB.keys()}

    def simulate_cycle(self):
        for item, data in SCRAP_DB.items():
            base = data['base']
            volatility = data['volatility']
            
            if random.random() > 0.8: 
                self.trend_cycles[item] = random.choice([-1, 1]) * random.uniform(0.5, 2.0)
            
            trend = self.trend_cycles.get(item, 0)
            shift = random.uniform(-volatility, volatility) + (trend * 0.05)
            
            new_price = self.current_prices[item] * (1 + shift)
            new_price = max(base * 0.2, min(base * 4.0, new_price))
            self.current_prices[item] = int(new_price)
            
            self.history[item].append(self.current_prices[item])
            if len(self.history[item]) > 20:
                self.history[item].pop(0)

class SalvageShip:
    def __init__(self):
        self.credits = 0
        self.depth_au = 0.0 
        self.max_depth = 0.0
        
        self.upgrades = {k: 0 for k in UPGRADE_TREE.keys()}
        self.cargo = [] 
        self.radar_data = [] 
        self.log = ["A.P.E.X. System Online.", "Awaiting Launch sequence."]
        
        self.hull = self.get_max_hull()
        self.fuel = self.get_max_fuel()
        self.hostile_encounter = None

    def get_max_hull(self): return 150 + (self.upgrades['hull'] * UPGRADE_TREE['hull']['effect'])
    def get_max_fuel(self): return 300 + (self.upgrades['fuel'] * UPGRADE_TREE['fuel']['effect'])
    def get_max_cargo(self): return 50.0 + (self.upgrades['cargo'] * UPGRADE_TREE['cargo']['effect'])
    def get_firepower(self): return 20 + (self.upgrades['weapons'] * UPGRADE_TREE['weapons']['effect'])
    
    def get_fuel_efficiency(self):
        reduction = self.upgrades['sohc4v'] * UPGRADE_TREE['sohc4v']['effect']
        return max(0.15, 1.0 - reduction)

    def get_apex_dodge(self):
        return min(0.60, self.upgrades['apex'] * UPGRADE_TREE['apex']['effect'])

    def get_cargo_weight(self):
        return sum(item['weight'] for item in self.cargo)

    def add_log(self, msg):
        ts = datetime.datetime.now().strftime('%H:%M:%S')
        self.log.insert(0, f"[{ts}] {msg}")
        if len(self.log) > 50: self.log.pop()

    def take_damage(self, amount, source):
        if random.random() < self.get_apex_dodge():
            self.add_log(f"⚡ A.P.E.X. MATRIX: Micro-thrusters evaded {source}!")
            return False
            
        self.hull -= amount
        self.add_log(f"💥 BREACH: Took {amount} DMG from {source}. Hull: {self.hull}/{self.get_max_hull()}")
        
        if self.hull <= 0:
            self.handle_destruction()
        return True

    def handle_destruction(self):
        self.add_log("💀 FATAL: VESSEL DESTROYED. Emergency Pod deployed.")
        self.depth_au = 0.0
        self.cargo = []
        self.radar_data = []
        self.hostile_encounter = None
        self.hull = self.get_max_hull()
        self.fuel = self.get_max_fuel()
        st.session_state.market.simulate_cycle()

# ==========================================
# GAME ENGINE FUNCTIONS
# ==========================================
def scan_sector(ship):
    blips = []
    radar_lvl = ship.upgrades['radar']
    num_blips = random.randint(3, 6 + radar_lvl)
    
    for _ in range(num_blips):
        angle = random.uniform(0, 360)
        distance = random.uniform(1.0, 10.0 + (radar_lvl * 2.0))
        roll = random.random() + (ship.depth_au * 0.01) + (radar_lvl * 0.03)
        
        if roll > 0.96: r, c, n = 5, "#c084fc", "Dark Matter Anomaly"
        elif roll > 0.82: r, c, n = 4, "#fcd34d", "High-Energy Signature"
        elif roll > 0.55: r, c, n = 3, "#60a5fa", "Encrypted Wreckage"
        elif roll > 0.25: r, c, n = 2, "#34d399", "Reinforced Struts"
        else: r, c, n = 1, "#94a3b8", "Generic Scrap"
            
        blips.append({"angle": angle, "dist": distance, "rarity": r, "color": c, "name": n, "harvested": False})
    
    ship.radar_data = blips
    ship.add_log(f"📡 L.O.O.T. ARRAY: Sector scanned. {len(blips)} signatures found.")

def trigger_encounter(ship):
    if random.random() > 0.75:
        enemy_types = [
            {"name": "Rogue Mining Drone", "hp": 40, "dmg": 15},
            {"name": "Pirate Interceptor", "hp": 80, "dmg": 30},
            {"name": "Automated Defense Platform", "hp": 150, "dmg": 50}
        ]
        tier = min(2, int(ship.depth_au / 15))
        base_enemy = enemy_types[tier]
        ship.hostile_encounter = {
            "name": base_enemy["name"],
            "hp": base_enemy["hp"] + int(ship.depth_au * 2),
            "dmg": base_enemy["dmg"] + int(ship.depth_au)
        }
        ship.add_log(f"🚨 HOSTILE DETECTED: {ship.hostile_encounter['name']} closing in!")

def execute_combat_round(ship):
    enemy = ship.hostile_encounter
    if not enemy: return
    
    dmg_dealt = int(ship.get_firepower() * random.uniform(0.8, 1.2))
    enemy['hp'] -= dmg_dealt
    ship.add_log(f"⚔️ KINETIC CANNONS: Dealt {dmg_dealt} DMG to {enemy['name']}.")
    
    if enemy['hp'] <= 0:
        ship.add_log(f"✅ THREAT NEUTRALIZED: {enemy['name']} destroyed.")
        ship.hostile_encounter = None
        bounty = int(enemy['dmg'] * 5 * (1 + (ship.depth_au*0.1)))
        ship.credits += bounty
        ship.add_log(f"💰 BOUNTY CLAIMED: {bounty} CR.")
        return

    dmg_taken = int(enemy['dmg'] * random.uniform(0.8, 1.2))
    ship.take_damage(dmg_taken, enemy['name'])

def evade_combat(ship):
    fuel_cost = int(40 * ship.get_fuel_efficiency())
    if ship.fuel < fuel_cost:
        ship.add_log("⚠️ CANNOT EVADE: Insufficient Delta-v!")
        execute_combat_round(ship)
        return
        
    ship.fuel -= fuel_cost
    if random.random() < 0.5 + ship.get_apex_dodge():
        ship.add_log("💨 EVASION SUCCESSFUL: Broke enemy lock.")
        ship.hostile_encounter = None
    else:
        ship.add_log("❌ EVASION FAILED: Enemy maintains pursuit!")
        execute_combat_round(ship)

def harvest_target(ship, blip_idx):
    if ship.hostile_encounter:
        ship.add_log("⚠️ CANNOT HARVEST: Hostile active in sector!")
        return

    blip = ship.radar_data[blip_idx]
    f_cost = int(blip['dist'] * 3 * ship.get_fuel_efficiency())
    
    if ship.fuel < f_cost:
        ship.add_log(f"⚠️ LOW FUEL: Need {f_cost} Delta-v.")
        return
        
    ship.fuel -= f_cost
    blip['harvested'] = True
    
    if random.random() < 0.15 + (ship.depth_au * 0.005):
        ship.take_damage(random.randint(15, 35), "Debris Collision")
        if ship.hull <= 0: return 
            
    pool = [k for k, v in SCRAP_DB.items() if v['rarity'] <= blip['rarity']]
    if not pool: pool = ["Iron-Carbon"]
    
    item = random.choice(pool)
    weight = SCRAP_DB[item]['weight']
    
    if ship.get_cargo_weight() + weight > ship.get_max_cargo():
        ship.add_log(f"📦 HOLD FULL: Cannot fit {item} ({weight}t).")
    else:
        ship.cargo.append({"name": item, "weight": weight})
        ship.add_log(f"✅ SECURED: {item} | Mass: {weight}t")

def push_orbit(ship):
    if ship.hostile_encounter:
        ship.add_log("⚠️ CANNOT BURN: Hostile active in sector!")
        return

    f_cost = int(35 * ship.get_fuel_efficiency())
    if ship.fuel < f_cost:
        ship.add_log(f"⚠️ LOW FUEL: Need {f_cost} Delta-v for Prograde Burn.")
        return
        
    ship.fuel -= f_cost
    ship.depth_au += random.uniform(2.0, 5.0)
    ship.max_depth = max(ship.max_depth, ship.depth_au)
    
    ship.add_log(f"🚀 PROGRADE BURN: Pushing to {ship.depth_au:.1f} AU.")
    
    heal = int(ship.get_max_hull() * (ship.upgrades['apex'] * 0.05))
    if heal > 0 and ship.hull < ship.get_max_hull():
        ship.hull = min(ship.get_max_hull(), ship.hull + heal)
        ship.add_log(f"🔧 A.P.E.X. Auto-Repair restored {heal} Hull.")

    scan_sector(ship)
    trigger_encounter(ship)

def return_to_base(ship, market):
    if ship.hostile_encounter:
        ship.add_log("⚠️ CANNOT DOCK: Hostile active in sector!")
        return

    f_cost = int((ship.depth_au * 2.5) * ship.get_fuel_efficiency())
    
    if ship.fuel < f_cost:
        ship.add_log(f"🚨 CRITICAL: Insufficient Delta-v for Retrograde. Drifting...")
        ship.take_damage(9999, "Void Starvation")
        return
        
    ship.fuel -= f_cost
    ship.depth_au = 0.0
    ship.radar_data = []
    
    ship.add_log("🌌 RETROGRADE BURN SUCCESS. Docked at Station Alpha.")
    
    total_payout = 0
    item_counts = {}
    for item in ship.cargo:
        name = item['name']
        price = market.current_prices[name]
        total_payout += price
        item_counts[name] = item_counts.get(name, 0) + 1
        
    if total_payout > 0:
        ship.credits += total_payout
        manifest_str = ", ".join([f"{k}x{v}" for k,v in item_counts.items()])
        ship.add_log(f"💰 MARKET SALE: {manifest_str}")
        ship.add_log(f"💰 TOTAL PROFIT: {total_payout:,.0f} CR.")
    
    ship.cargo = []
    ship.hull = ship.get_max_hull()
    ship.fuel = ship.get_max_fuel()
    market.simulate_cycle()

# ==========================================
# UI RENDERING HELPERS
# ==========================================
def render_cyber_bar(current, maximum, color_hex, unit=""):
    pct = min(100, max(0, int((current / maximum) * 100)))
    st.markdown(f"""
    <div class="progress-container">
        <div class="progress-fill" style="width: {pct}%; background-color: {color_hex}; box-shadow: 0 0 10px {color_hex};"></div>
    </div>
    <div style="display:flex; justify-content:space-between; font-size:12px; color:#cbd5e1; margin-top:4px; font-family:'Share Tech Mono', monospace;">
        <span>{pct}%</span>
        <span>{current:.1f} / {maximum:.1f} {unit}</span>
    </div>
    """, unsafe_allow_html=True)

def render_market_chart(market):
    fig = go.Figure()
    colors = ["#94a3b8", "#ef4444", "#38bdf8", "#8b5cf6", "#f59e0b", "#c084fc"]
    for idx, (item, history) in enumerate(market.history.items()):
        y_data = history[-15:] if len(history) > 15 else history
        x_data = list(range(len(y_data)))
        fig.add_trace(go.Scatter(
            x=x_data, y=y_data, mode='lines+markers', name=item,
            line=dict(color=colors[idx % len(colors)], width=2, shape='spline'),
            marker=dict(size=6, symbol='diamond', line=dict(width=1, color='#fff'))
        ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#cbd5e1", family="Rajdhani"),
        xaxis=dict(showgrid=False, visible=False),
        yaxis=dict(gridcolor="rgba(30, 41, 59, 0.5)", zerolinecolor="rgba(30, 41, 59, 0.5)"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=0, r=0, t=30, b=0),
        height=300
    )
    return fig

def render_radar(ship):
    fig = go.Figure()
    
    # Base Vessel Ping
    fig.add_trace(go.Scatterpolar(
        r=[0], theta=[0], mode='markers',
        marker=dict(color='#38bdf8', size=15, symbol='x', line=dict(color='#fff', width=2)),
        hoverinfo='text', text='A.P.E.X. VESSEL', name='Vessel'
    ))

    if ship.depth_au > 0 and ship.radar_data:
        active = [b for b in ship.radar_data if not b['harvested']]
        if active:
            r = [b['dist'] for b in active]
            theta = [b['angle'] for b in active]
            colors = [b['color'] for b in active]
            sizes = [b['rarity'] * 4 + 8 for b in active]
            names = [b['name'] for b in active]
            
            fig.add_trace(go.Scatterpolar(
                r=r, theta=theta, mode='markers',
                marker=dict(color=colors, size=sizes, opacity=0.85, line=dict(color='#e2e8f0', width=1)),
                hoverinfo='text', text=names, name='Anomalies'
            ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 15], gridcolor='rgba(56, 189, 248, 0.2)', tickfont=dict(color='#475569')),
            angularaxis=dict(gridcolor='rgba(56, 189, 248, 0.2)', tickfont=dict(color='#475569')),
            bgcolor='rgba(2, 6, 23, 0.6)'
        ),
        showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=20, b=20), height=400
    )
    return fig

# ==========================================
# MAIN EXECUTION
# ==========================================
def main():
    if 'ship' not in st.session_state:
        st.session_state.ship = SalvageShip()
    if 'market' not in st.session_state:
        st.session_state.market = DynamicMarket()
        
    ship = st.session_state.ship
    market = st.session_state.market

    # HEADER & HELP POPOVER
    header_col1, header_col2 = st.columns([0.9, 0.1])
    with header_col1:
        st.markdown("<h1>A.P.E.X. VOID DRIFT</h1>", unsafe_allow_html=True)
    with header_col2:
        st.markdown("<div class='popover-help-btn'>", unsafe_allow_html=True)
        with st.popover("?", use_container_width=True):
            st.markdown("""
            ### 📖 FLIGHT MANUAL
            **1. Navigation:** Burn Prograde to travel deeper (better loot, harder enemies). Burn Retrograde to return to Alpha Station. Running out of fuel means death.
            **2. Radar:** Scan and harvest anomalies. Watch your cargo weight limit.
            **3. Combat:** Deep space triggers hostiles. Evade (costs fuel, uses A.P.E.X. evasion stat) or fight with Kinetic Cannons.
            **4. Shipyard:** Dock at Alpha Station to upgrade your Hull, Fuel, Cargo, Radar, Weapons, and A.P.E.X. Core.
            **5. Market:** Sell scrap at Alpha. Prices fluctuate constantly.
            """)
        st.markdown("</div>", unsafe_allow_html=True)

    # VITALS RIBBON
    v1, v2, v3, v4 = st.columns(4)
    with v1:
        # 🐛 THE FIX: Added the / {ship.max_depth:.1f} back into the HTML string interpolation 
        st.markdown(f'<div class="cyber-card purple"><div class="metric-title">Depth / Record</div><div class="metric-value">{ship.depth_au:.1f} / {ship.max_depth:.1f} AU</div></div>', unsafe_allow_html=True)
    with v2:
        st.markdown(f'<div class="cyber-card warning"><div class="metric-title">Account Balance</div><div class="metric-value">{ship.credits:,.0f} CR</div></div>', unsafe_allow_html=True)
    with v3:
        h_color = "#10b981" if ship.hull > ship.get_max_hull()*0.4 else "#ef4444"
        card_class = "success" if ship.hull > ship.get_max_hull()*0.4 else "danger"
        st.markdown(f'<div class="cyber-card {card_class}" style="padding-bottom:10px;"><div class="metric-title">Hull Integrity</div>', unsafe_allow_html=True)
        render_cyber_bar(ship.hull, ship.get_max_hull(), h_color)
        st.markdown('</div>', unsafe_allow_html=True)
    with v4:
        f_color = "#38bdf8" if ship.fuel > ship.get_max_fuel()*0.3 else "#f59e0b"
        card_class = "" if ship.fuel > ship.get_max_fuel()*0.3 else "warning"
        st.markdown(f'<div class="cyber-card {card_class}" style="padding-bottom:10px;"><div class="metric-title">Delta-V Fuel</div>', unsafe_allow_html=True)
        render_cyber_bar(ship.fuel, ship.get_max_fuel(), f_color)
        st.markdown('</div>', unsafe_allow_html=True)

    # MAIN INTERFACE TABS
    tab_nav, tab_radar, tab_eng, tab_market = st.tabs(["🎛️ COMMAND MODULE", "📡 SENSOR ARRAY", "🛠️ SHIPYARD", "📈 EXCHANGE"])

    # --- COMMAND MODULE ---
    with tab_nav:
        c_act, c_log = st.columns([1, 1.5])
        with c_act:
            st.markdown("### TACTICAL OPERATIONS")
            if ship.hostile_encounter:
                st.markdown(f"""
                <div class="cyber-card danger">
                    <div style="color:#ef4444; font-family:'Orbitron'; font-weight:bold; font-size:1.2rem; margin-bottom:10px;">
                        🚨 THREAT DETECTED
                    </div>
                    <strong>Entity:</strong> {ship.hostile_encounter['name']}<br>
                    <strong>Armor:</strong> {ship.hostile_encounter['hp']} HP<br>
                    <strong>DPS:</strong> {ship.hostile_encounter['dmg']}
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("<div class='btn-combat'>", unsafe_allow_html=True)
                if st.button("⚔️ FIRE KINETIC CANNONS"):
                    execute_combat_round(ship)
                    st.rerun()
                st.markdown("</div><br>", unsafe_allow_html=True)
                
                st.markdown("<div class='btn-evade'>", unsafe_allow_html=True)
                if st.button("💨 EVASIVE MANEUVERS"):
                    evade_combat(ship)
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                if ship.depth_au == 0:
                    st.markdown("""
                    <div class="cyber-card success" style="text-align:center;">
                        <h4 style="color:#10b981; font-family:'Orbitron';">🟢 DOCKED AT ALPHA</h4>
                        <p style="color:#94a3b8; font-size:14px;">Systems nominal. Ready for launch.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown("<div class='btn-launch'>", unsafe_allow_html=True)
                    if st.button("🚀 LAUNCH INTO THE VOID"):
                        push_orbit(ship)
                        st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    tension = min(100, int(ship.depth_au * 2))
                    st.markdown(f"""
                    <div class="cyber-card warning" style="text-align:center;">
                        <h4 style="color:#f59e0b; font-family:'Orbitron';">⚠️ DEEP SPACE</h4>
                        <p style="color:#94a3b8; font-size:14px;">Sector Tension: {tension}%</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("<div class='btn-launch'>", unsafe_allow_html=True)
                    if st.button("🔥 BURN PROGRADE (DEEPER)"):
                        push_orbit(ship)
                        st.rerun()
                    st.markdown("</div><br>", unsafe_allow_html=True)
                    
                    ret_cost = int((ship.depth_au * 2.5) * ship.get_fuel_efficiency())
                    st.markdown("<div class='btn-combat'>", unsafe_allow_html=True)
                    if st.button(f"🔄 BURN RETROGRADE (RETURN)\n[FUEL: {ret_cost}]"):
                        return_to_base(ship, market)
                        st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("### CARGO BAY")
            st.markdown("<div class='cyber-card purple'>", unsafe_allow_html=True)
            render_cyber_bar(ship.get_cargo_weight(), ship.get_max_cargo(), "#c084fc", "Tons")
            with st.expander(f"View Manifest [{len(ship.cargo)} Items]"):
                if not ship.cargo: st.write("Hold empty.")
                else:
                    for i in ship.cargo: st.markdown(f"<span style='font-size:13px; color:#cbd5e1;'>• {i['name']} ({i['weight']}t)</span>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with c_log:
            st.markdown("### SYSTEM LOG")
            log_html = "".join([f"<span>{line}</span>" for line in ship.log])
            st.markdown(f"<div class='console-wrapper'><div class='console-log'>{log_html}</div></div>", unsafe_allow_html=True)

    # --- SENSOR ARRAY ---
    with tab_radar:
        if ship.depth_au == 0:
            st.markdown("""
            <div style='text-align:center; padding:80px 20px; border: 1px dashed rgba(56, 189, 248, 0.3); border-radius: 8px; margin-top: 20px;'>
                <h2 style='color:#475569;'>SENSOR ARRAY OFFLINE</h2>
                <p style='color:#64748b;'>Launch vessel to activate L.O.O.T. array telemetry.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            c_rad1, c_rad2 = st.columns([1.5, 1])
            with c_rad1:
                st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
                fig = render_radar(ship)
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
                st.markdown("</div>", unsafe_allow_html=True)
            with c_rad2:
                st.markdown("### TARGET LOCK")
                if ship.hostile_encounter:
                    st.markdown("<div class='cyber-card danger' style='text-align:center; color:#ef4444;'><strong>RADAR JAMMED BY HOSTILE</strong></div>", unsafe_allow_html=True)
                else:
                    active = [i for i, b in enumerate(ship.radar_data) if not b['harvested']]
                    if not active:
                        st.success("Sector clear of anomalies.")
                    else:
                        for b_idx in active:
                            b = ship.radar_data[b_idx]
                            f_cost = int(b['dist'] * 3 * ship.get_fuel_efficiency())
                            st.markdown(f"""
                            <div style="background:rgba(15, 23, 42, 0.6); border-left:3px solid {b['color']}; padding:10px; margin-bottom:10px; border-radius:2px;">
                                <div style="display:flex; justify-content:space-between; align-items:center;">
                                    <div>
                                        <div style="color:{b['color']}; font-weight:bold; font-size:14px;">{b['name']}</div>
                                        <div style="color:#94a3b8; font-size:12px;">Dist: {b['dist']:.1f} | Fuel Cost: {f_cost}</div>
                                    </div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            if st.button(f"HARVEST", key=f"harv_{b_idx}", help=f"Costs {f_cost} fuel"):
                                harvest_target(ship, b_idx)
                                st.rerun()

    # --- SHIPYARD ---
    with tab_eng:
        if ship.depth_au > 0:
            st.markdown("""
            <div style='text-align:center; padding:80px 20px; border: 1px dashed #ef4444; border-radius: 8px; margin-top: 20px; background:rgba(239, 68, 68, 0.05);'>
                <h2 style='color:#ef4444;'>SHIPYARD INACCESSIBLE</h2>
                <p style='color:#fca5a5;'>You must be docked at Alpha Station to install upgrades.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("### ALPHA STATION ENGINEERING")
            u_cols = st.columns(3)
            for idx, (u_id, u_data) in enumerate(UPGRADE_TREE.items()):
                lvl = ship.upgrades[u_id]
                cost = int(u_data['base_cost'] * (u_data['cost_mult'] ** lvl))
                
                with u_cols[idx % 3]:
                    st.markdown(f"""
                    <div class="cyber-card">
                        <div style="color:#38bdf8; font-family:'Orbitron'; font-weight:700; font-size:16px; margin-bottom:5px;">
                            {u_data['name']} <span style="color:#f8fafc; background:#1e293b; padding:2px 6px; border-radius:12px; font-size:12px;">LVL {lvl}</span>
                        </div>
                        <div style="font-size:13px; color:#cbd5e1; margin-bottom:15px; height:40px; overflow:hidden;">
                            {u_data['desc']}
                        </div>
                        <div style="color:#fbbf24; font-weight:700; font-size:18px; margin-bottom:10px; font-family:'Share Tech Mono';">
                            {cost:,} CR
                        </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"UPGRADE", key=f"upg_{u_id}", disabled=ship.credits < cost):
                        ship.credits -= cost
                        ship.upgrades[u_id] += 1
                        ship.hull = ship.get_max_hull()
                        ship.fuel = ship.get_max_fuel()
                        ship.add_log(f"⚙️ UPGRADE: {u_data['name']} integrated.")
                        st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)

    # --- EXCHANGE ---
    with tab_market:
        st.markdown("### COMMODITY EXCHANGE (ALPHA NETWORK)")
        
        c_mkt1, c_mkt2 = st.columns([2, 1])
        with c_mkt1:
            st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
            m_fig = render_market_chart(market)
            st.plotly_chart(m_fig, use_container_width=True, config={'displayModeBar': False})
            st.markdown("</div>", unsafe_allow_html=True)
            
        with c_mkt2:
            st.markdown("### LIVE TICKER")
            for item, price in market.current_prices.items():
                base = SCRAP_DB[item]['base']
                color = "#10b981" if price > base else "#ef4444"
                indicator = "▲" if price > base else "▼"
                bg_glow = "rgba(16, 185, 129, 0.1)" if price > base else "rgba(239, 68, 68, 0.1)"
                
                st.markdown(f"""
                <div style="background:{bg_glow}; border:1px solid rgba(255,255,255,0.05); padding:12px; border-radius:4px; margin-bottom:8px; display:flex; justify-content:space-between; align-items:center;">
                    <span style="color:#e2e8f0; font-weight:600; font-size:14px;">{item}</span>
                    <span style="color:{color}; font-family:'Share Tech Mono'; font-size:16px; font-weight:bold;">
                        {price} {indicator}
                    </span>
                </div>
                """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

