import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import random
import math
import datetime

# ==========================================
# PAGE CONFIGURATION & THEME
# ==========================================
st.set_page_config(page_title="A.P.E.X. SALVAGE COMMAND", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS focused on mobile responsiveness and terminal aesthetics
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&display=swap');
html, body, [class*="css"], [class*="st-"] {
    font-family: 'Rajdhani', sans-serif !important;
    letter-spacing: 0.5px;
}
.stApp {
    background-color: #050914;
    color: #e2e8f0;
}
h1, h2, h3 {
    color: #38bdf8 !important;
    text-transform: uppercase;
    text-shadow: 0 0 10px rgba(56, 189, 248, 0.3);
    margin-bottom: 0rem;
}
.metric-box {
    background: linear-gradient(180deg, #0f172a 0%, #020617 100%);
    border: 1px solid #1e293b;
    border-top: 3px solid #38bdf8;
    padding: 15px;
    border-radius: 4px;
    margin-bottom: 10px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.5);
}
.metric-box.danger { border-top-color: #ef4444; }
.metric-box.warning { border-top-color: #f59e0b; }
.metric-box.success { border-top-color: #10b981; }
.metric-title {
    font-size: 12px;
    color: #94a3b8;
    text-transform: uppercase;
    font-weight: 600;
}
.metric-value {
    font-size: 22px;
    color: #f8fafc;
    font-weight: 700;
    font-family: monospace;
}
.console-log {
    background-color: #020617;
    border: 1px solid #1e293b;
    border-left: 4px solid #8b5cf6;
    padding: 15px;
    height: 400px;
    overflow-y: auto;
    font-family: monospace !important;
    font-size: 13px;
    color: #a78bfa;
}
.stButton>button {
    background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
    color: #38bdf8;
    border: 1px solid #334155;
    border-radius: 2px;
    font-weight: 600;
    text-transform: uppercase;
    transition: all 0.2s;
    width: 100%;
}
.stButton>button:hover {
    border-color: #38bdf8;
    color: #ffffff;
    box-shadow: 0 0 15px rgba(56, 189, 248, 0.4);
}
.action-btn>button {
    background: linear-gradient(180deg, #047857 0%, #064e3b 100%) !important;
    color: #ecfdf5 !important;
    border-color: #10b981 !important;
}
.danger-btn>button {
    background: linear-gradient(180deg, #991b1b 0%, #7f1d1d 100%) !important;
    color: #fef2f2 !important;
    border-color: #ef4444 !important;
}
.upgrade-card {
    background: #0f172a;
    border: 1px solid #1e293b;
    padding: 15px;
    border-radius: 4px;
    margin-bottom: 15px;
}
.upgrade-title {
    color: #8b5cf6;
    font-weight: 700;
    font-size: 16px;
    margin-bottom: 5px;
}
hr { border-color: #1e293b; }
.progress-container {
    width: 100%;
    background-color: #1e293b;
    border-radius: 2px;
    margin-top: 5px;
    height: 10px;
    overflow: hidden;
}
.progress-fill {
    height: 100%;
    transition: width 0.3s ease;
}
.popover-help-btn button {
    margin-top: 15px;
    border-color: #8b5cf6 !important;
    color: #8b5cf6 !important;
}
.popover-help-btn button:hover {
    background: #8b5cf6 !important;
    color: #ffffff !important;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

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
        "desc": "Increases max Hull Integrity.",
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
        "desc": "Single Overhead Cam with 4-valve cylinder vectors. Highly efficient. Reduces fuel consumption by 12% per level.",
        "base_cost": 1500, "cost_mult": 2.2, "effect": 0.12
    },
    "radar": {
        "name": "L.O.O.T. Array",
        "desc": "Logistical Observation array. Extends radar range and rare anomaly detection.",
        "base_cost": 2000, "cost_mult": 2.5, "effect": 1
    },
    "weapons": {
        "name": "Kinetic Interceptors",
        "desc": "Automated defense cannons. Increases combat survival rate.",
        "base_cost": 1200, "cost_mult": 2.0, "effect": 15
    },
    "apex": {
        "name": "A.P.E.X. Core",
        "desc": "Advanced Predictive Executive Matrix. Provides tactical evasion and automated system repairs.",
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
        self.log = ["A.P.E.X. Matrix Online.", "Awaiting Launch sequence."]
        
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
        
        if roll > 0.96: r, c, n = 5, "#a855f7", "Dark Matter Anomaly"
        elif roll > 0.82: r, c, n = 4, "#f59e0b", "High-Energy Signature"
        elif roll > 0.55: r, c, n = 3, "#3b82f6", "Encrypted Wreckage"
        elif roll > 0.25: r, c, n = 2, "#10b981", "Reinforced Struts"
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
def render_bar(current, maximum, color):
    pct = min(100, max(0, int((current / maximum) * 100)))
    st.markdown(f"""
    <div class="progress-container">
        <div class="progress-fill" style="width: {pct}%; background-color: {color};"></div>
    </div>
    <div style="font-size:11px; color:#94a3b8; text-align:right;">{current:.1f} / {maximum:.1f}</div>
    """, unsafe_allow_html=True)

def render_market_chart(market):
    fig = go.Figure()
    colors = ["#94a3b8", "#fca5a5", "#cbd5e1", "#818cf8", "#fde047", "#c084fc"]
    for idx, (item, history) in enumerate(market.history.items()):
        y_data = history[-15:] if len(history) > 15 else history
        x_data = list(range(len(y_data)))
        fig.add_trace(go.Scatter(
            x=x_data, y=y_data, mode='lines+markers', name=item,
            line=dict(color=colors[idx % len(colors)], width=2),
            marker=dict(size=6)
        ))
    
    fig.update_layout(
        title="Live Commodity Pricing (Station Alpha)",
        title_font=dict(color="#38bdf8", family="Rajdhani"),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#cbd5e1"),
        xaxis=dict(showgrid=False, visible=False),
        yaxis=dict(gridcolor="#1e293b"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=10, r=10, t=50, b=10),
        height=300
    )
    return fig

def render_radar(ship):
    if ship.depth_au == 0 or not ship.radar_data:
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(r=[0], theta=[0], mode='markers', marker=dict(color='#38bdf8', size=10, symbol='cross'), name='Vessel'))
    else:
        active = [b for b in ship.radar_data if not b['harvested']]
        if not active:
             fig = go.Figure()
             fig.add_trace(go.Scatterpolar(r=[0], theta=[0], mode='markers', marker=dict(color='#38bdf8', size=10, symbol='cross'), name='Vessel'))
        else:
            r = [b['dist'] for b in active]
            theta = [b['angle'] for b in active]
            colors = [b['color'] for b in active]
            sizes = [b['rarity'] * 3 + 8 for b in active]
            names = [b['name'] for b in active]
            
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(r=[0], theta=[0], mode='markers', marker=dict(color='#38bdf8', size=12, symbol='cross'), hoverinfo='text', text='A.P.E.X. VESSEL'))
            fig.add_trace(go.Scatterpolar(
                r=r, theta=theta, mode='markers',
                marker=dict(color=colors, size=sizes, opacity=0.8, line=dict(color='#e2e8f0', width=1)),
                hoverinfo='text', text=names
            ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 15], gridcolor='#1e293b', tickfont=dict(color='#475569')),
            angularaxis=dict(gridcolor='#1e293b', tickfont=dict(color='#475569')),
            bgcolor='#020617'
        ),
        showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=20, b=20), height=350
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

    # HEADER WITH INFO BUTTON
    header_col1, header_col2 = st.columns([0.85, 0.15])
    with header_col1:
        st.markdown("<h1>🌌 A.P.E.X. VOID DRIFT</h1>", unsafe_allow_html=True)
    with header_col2:
        st.markdown("<div class='popover-help-btn'>", unsafe_allow_html=True)
        with st.popover("ℹ️ HELP", use_container_width=True):
            st.markdown("""
            ### 📖 A.P.E.X. FLIGHT MANUAL
            Welcome to the command terminal. Your objective is to launch from Station Alpha, scavenge deep space for valuable scrap, and return alive to sell your payload.
            
            **1. Navigation & The Void**
            * **Launch / Burn Prograde:** Pushes your vessel deeper into the sector. The deeper you travel, the rarer the scrap, but the deadlier the enemies. This consumes Delta-v (fuel).
            * **Burn Retrograde:** Returns you to Station Alpha. 
            * *CRITICAL WARNING:* Returning costs Delta-v proportional to your depth. If you run out of fuel in the void, your vessel will be lost. Always monitor your return fuel cost.
            
            **2. L.O.O.T. Array (Radar)**
            * Ping local anomalies on the radar tab.
            * Select an anomaly to expend fuel and harvest it. 
            * Heavier scrap fills your Cargo Hold quickly. Ensure you have the capacity.
            
            **3. Combat Protocols**
            * **Hostile Encounters:** Deeper space triggers interceptions by rogue drones and pirates.
            * **Evasive Maneuvers:** Relies on your Advanced Predictive Executive Matrix to calculate dodge vectors. Costs fuel, but saves your hull.
            * **Kinetic Cannons:** Stand your ground and fire back. Destroying enemies yields Credit bounties.
            
            **4. Station Alpha Shipyard**
            * You must be docked at Alpha to upgrade.
            * Invest Credits (CR) into your Hull, Cargo Bay, Weapons, and Radar. 
            * *Pro-tip:* Upgrading your SOHC-4V Plasma Valvetrain is vital for stretching fuel efficiency on deep runs. Upgrading the core Advanced Predictive Executive Matrix grants passive auto-repairs between jumps.
            
            **5. Commodity Exchange**
            * Scrap prices fluctuate every time you dock or an event passes.
            * Sell high, or risk venturing back out if the market crashes.
            """)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Top Vitals (Mobile Friendly Grid)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'<div class="metric-box"><div class="metric-title">Depth / Record</div><div class="metric-value" style="color:#a78bfa;">{ship.depth_au:.1f} / {ship.max_depth:.1f} AU</div></div>', unsafe_allow_html=True)
        h_color = "#10b981" if ship.hull > ship.get_max_hull()*0.4 else "#ef4444"
        st.markdown('<div class="metric-box"><div class="metric-title">Hull Integrity</div></div>', unsafe_allow_html=True)
        render_bar(ship.hull, ship.get_max_hull(), h_color)
    with col2:
        st.markdown(f'<div class="metric-box"><div class="metric-title">Credits</div><div class="metric-value" style="color:#fbbf24;">{ship.credits:,.0f} CR</div></div>', unsafe_allow_html=True)
        f_color = "#38bdf8" if ship.fuel > ship.get_max_fuel()*0.3 else "#f59e0b"
        st.markdown('<div class="metric-box"><div class="metric-title">Delta-v Propellant</div></div>', unsafe_allow_html=True)
        render_bar(ship.fuel, ship.get_max_fuel(), f_color)

    st.markdown("<hr>", unsafe_allow_html=True)

    # Main Tabs for better mobile layout
    tab_nav, tab_radar, tab_eng, tab_market = st.tabs(["🎛️ FLIGHT CONSOLE", "📡 L.O.O.T. ARRAY", "🛠️ ENGINEERING", "📈 MARKET"])

    # --- TAB 1: FLIGHT CONSOLE & COMBAT ---
    with tab_nav:
        c_act, c_log = st.columns([1, 1.5])
        with c_act:
            st.markdown("### OPERATIONS")
            if ship.hostile_encounter:
                st.error(f"🚨 UNDER ATTACK: {ship.hostile_encounter['name']} (HP: {ship.hostile_encounter['hp']})")
                if st.button("⚔️ FIRE KINETIC CANNONS", key="btn_atk"):
                    execute_combat_round(ship)
                    st.rerun()
                if st.button("💨 EVASIVE MANEUVERS", key="btn_evade"):
                    evade_combat(ship)
                    st.rerun()
            else:
                if ship.depth_au == 0:
                    st.info("🟢 DOCKED AT STATION ALPHA")
                    st.markdown("<div class='action-btn'>", unsafe_allow_html=True)
                    if st.button("🚀 LAUNCH INTO THE VOID"):
                        push_orbit(ship)
                        st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.warning(f"⚠️ DEEP SPACE (Tension: {min(100, int(ship.depth_au * 2))}%)")
                    st.markdown("<div class='action-btn'>", unsafe_allow_html=True)
                    if st.button("🔥 BURN PROGRADE (DEEPER)"):
                        push_orbit(ship)
                        st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    ret_cost = int((ship.depth_au * 2.5) * ship.get_fuel_efficiency())
                    st.markdown("<div class='danger-btn'>", unsafe_allow_html=True)
                    if st.button(f"🔄 BURN RETROGRADE (RETURN) [F: {ret_cost}]"):
                        return_to_base(ship, market)
                        st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown("### CARGO HOLD")
            render_bar(ship.get_cargo_weight(), ship.get_max_cargo(), "#8b5cf6")
            with st.expander(f"Manifest [{len(ship.cargo)} Items]"):
                if not ship.cargo: st.write("Hold empty.")
                else:
                    for i in ship.cargo: st.markdown(f"<span style='font-size:12px;'>• {i['name']} ({i['weight']}t)</span>", unsafe_allow_html=True)

        with c_log:
            st.markdown("### A.P.E.X. MATRIX LOG")
            log_html = "<br>".join([f"<span>{line}</span>" for line in ship.log])
            st.markdown(f"<div class='console-log'>{log_html}</div>", unsafe_allow_html=True)

    # --- TAB 2: L.O.O.T. RADAR ---
    with tab_radar:
        if ship.depth_au == 0:
            st.markdown("<div style='text-align:center; padding:40px; color:#475569;'>Radar Offline. Launch to engage.</div>", unsafe_allow_html=True)
        else:
            fig = render_radar(ship)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            
            if not ship.hostile_encounter:
                active = [i for i, b in enumerate(ship.radar_data) if not b['harvested']]
                if active:
                    st.markdown("**DETECTED ANOMALIES (Select to Harvest):**")
                    cols = st.columns(3)
                    for i, b_idx in enumerate(active[:9]):
                        b = ship.radar_data[b_idx]
                        f_cost = int(b['dist'] * 3 * ship.get_fuel_efficiency())
                        with cols[i % 3]:
                            if st.button(f"{b['name'][:8]}..\n[F: {f_cost}]", key=f"harv_{b_idx}"):
                                harvest_target(ship, b_idx)
                                st.rerun()
                else:
                    st.success("Sector clear of anomalies.")
            else:
                st.error("RADAR JAMMED BY HOSTILE FORCES.")

    # --- TAB 3: ENGINEERING / UPGRADES ---
    with tab_eng:
        if ship.depth_au > 0:
            st.warning("Must be docked at Station Alpha to access Shipyard.")
        else:
            st.markdown("### STATION ALPHA SHIPYARD")
            u_cols = st.columns(2)
            for idx, (u_id, u_data) in enumerate(UPGRADE_TREE.items()):
                lvl = ship.upgrades[u_id]
                cost = int(u_data['base_cost'] * (u_data['cost_mult'] ** lvl))
                
                with u_cols[idx % 2]:
                    st.markdown(f"""
                    <div class="upgrade-card">
                        <div class="upgrade-title">{u_data['name']} [LVL {lvl}]</div>
                        <div style="font-size:12px; color:#cbd5e1; margin-bottom:8px; min-height:45px;">{u_data['desc']}</div>
                        <div style="color:#fbbf24; font-weight:700; margin-bottom:8px;">{cost:,} CR</div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"INSTALL {u_id.upper()}", key=f"upg_{u_id}", disabled=ship.credits < cost):
                        ship.credits -= cost
                        ship.upgrades[u_id] += 1
                        ship.hull = ship.get_max_hull()
                        ship.fuel = ship.get_max_fuel()
                        ship.add_log(f"⚙️ UPGRADE: {u_data['name']} leveled up.")
                        st.rerun()

    # --- TAB 4: MARKETBOARD ---
    with tab_market:
        st.markdown("### COMMODITY EXCHANGE")
        st.markdown("<p style='font-size:13px; color:#94a3b8;'>Scrap values fluctuate based on station demand. Values shown are per unit.</p>", unsafe_allow_html=True)
        
        m_fig = render_market_chart(market)
        st.plotly_chart(m_fig, use_container_width=True, config={'displayModeBar': False})
        
        st.markdown("**Current Market Rates:**")
        m_cols = st.columns(3)
        for idx, (item, price) in enumerate(market.current_prices.items()):
            base = SCRAP_DB[item]['base']
            color = "#10b981" if price > base else "#ef4444"
            indicator = "▲" if price > base else "▼"
            with m_cols[idx % 3]:
                st.markdown(f"<div style='background:#0f172a; padding:10px; border:1px solid #1e293b; border-radius:4px; margin-bottom:10px;'>"
                            f"<div style='font-size:11px; color:#94a3b8;'>{item}</div>"
                            f"<div style='font-size:16px; font-weight:bold; color:{color};'>{price} CR {indicator}</div>"
                            f"</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()

