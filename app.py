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
st.set_page_config(page_title="A.P.E.X. SALVAGE COMMAND", layout="wide", initial_sidebar_state="expanded")

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
.metric-box.danger {
    border-top-color: #ef4444;
}
.metric-title {
    font-size: 12px;
    color: #94a3b8;
    text-transform: uppercase;
    font-weight: 600;
}
.metric-value {
    font-size: 24px;
    color: #f8fafc;
    font-weight: 700;
    font-family: monospace;
}
.console-log {
    background-color: #020617;
    border: 1px solid #1e293b;
    border-left: 4px solid #8b5cf6;
    padding: 15px;
    height: 300px;
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
.progress-bar-container {
    width: 100%;
    background-color: #1e293b;
    border-radius: 2px;
    margin-top: 5px;
}
.progress-bar-fill {
    height: 8px;
    border-radius: 2px;
    transition: width 0.3s ease;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ==========================================
# GAME CONSTANTS & DATABASES
# ==========================================
SCRAP_TYPES = {
    "Iron-Carbon Debris": {"base_val": 10, "weight": 2.0, "rarity": 1, "desc": "Common starship hull fragments."},
    "Copper Wiring Spools": {"base_val": 25, "weight": 1.5, "rarity": 1, "desc": "Conductive materials stripped from derelicts."},
    "Titanium Struts": {"base_val": 50, "weight": 4.0, "rarity": 2, "desc": "Heavy structural aerospace supports."},
    "Quantum Circuitry": {"base_val": 120, "weight": 0.5, "rarity": 3, "desc": "Fragile computing cores. High value, low mass."},
    "Isotope Batteries": {"base_val": 300, "weight": 5.0, "rarity": 4, "desc": "Highly volatile, incredibly valuable power cells."},
    "Dark Matter Shard": {"base_val": 1500, "weight": 1.0, "rarity": 5, "desc": "Anomalous material defying standard physics."}
}

UPGRADE_TREE = {
    "hull": {
        "name": "Hull Plating",
        "desc": "Increases max Hull Integrity to survive hazards.",
        "base_cost": 500,
        "cost_mult": 1.8,
        "effect": 50 # +50 Max Hull per level
    },
    "fuel": {
        "name": "Delta-v Fuel Tanks",
        "desc": "Expands propellant capacity for deeper orbital dives.",
        "base_cost": 400,
        "cost_mult": 1.5,
        "effect": 100 # +100 Max Fuel per level
    },
    "cargo": {
        "name": "Cargo Bay Expansion",
        "desc": "Increases maximum tonnage capacity for salvage.",
        "base_cost": 750,
        "cost_mult": 1.6,
        "effect": 25 # +25 Max Weight per level
    },
    "sohc4v": {
        "name": "SOHC-4V Plasma Valvetrain",
        "desc": "Advanced engine configuration with 4-valve cylinder vectors. Reduces fuel consumption by 15% per level.",
        "base_cost": 1500,
        "cost_mult": 2.5,
        "effect": 0.15 # 15% reduction per level
    },
    "loot_scanner": {
        "name": "L.O.O.T. Observation Engine",
        "desc": "Logistical Observation array. Increases chances of finding rare anomalies and high-tier scrap.",
        "base_cost": 2000,
        "cost_mult": 2.2,
        "effect": 1 # +1 Bonus Roll on loot tables
    },
    "apex_matrix": {
        "name": "A.P.E.X. Co-Processor",
        "desc": "Advanced Predictive Executive Matrix. Automatically evades 10% of hazards per level.",
        "base_cost": 5000,
        "cost_mult": 3.0,
        "effect": 0.10 # 10% dodge chance per level
    }
}

# ==========================================
# CORE CLASSES
# ==========================================
class SalvageShip:
    def __init__(self):
        self.credits = 0
        self.depth_au = 0.0 # Orbital Depth from Station
        self.max_depth_record = 0.0
        
        # Upgrades Dictionary (Level ints)
        self.upgrades = {k: 0 for k in UPGRADE_TREE.keys()}
        
        # Current Vitals
        self.hull = self.get_max_hull()
        self.fuel = self.get_max_fuel()
        
        # Inventory List of Dicts
        self.cargo = [] 
        
        self.log = ["A.P.E.X. Matrix Initialized.", "Vessel docked at Station Alpha."]
        self.radar_data = [] # Stores active blips

    def get_max_hull(self):
        return 100 + (self.upgrades['hull'] * UPGRADE_TREE['hull']['effect'])

    def get_max_fuel(self):
        return 200 + (self.upgrades['fuel'] * UPGRADE_TREE['fuel']['effect'])

    def get_max_cargo(self):
        return 50.0 + (self.upgrades['cargo'] * UPGRADE_TREE['cargo']['effect'])

    def get_current_cargo_weight(self):
        return sum(item['weight'] for item in self.cargo)

    def get_fuel_efficiency(self):
        # Base fuel consumption is 1.0. SOHC4V reduces it. Max reduction capped at 80%
        reduction = self.upgrades['sohc4v'] * UPGRADE_TREE['sohc4v']['effect']
        return max(0.2, 1.0 - reduction)

    def get_dodge_chance(self):
        return min(0.75, self.upgrades['apex_matrix'] * UPGRADE_TREE['apex_matrix']['effect'])

    def add_log(self, msg):
        timestamp = datetime.datetime.now().strftime('%H:%M:%S')
        self.log.insert(0, f"[{timestamp}] {msg}")
        if len(self.log) > 40:
            self.log.pop()

    def take_damage(self, amount, source):
        # APEX Matrix Dodge Check
        if random.random() < self.get_dodge_chance():
            self.add_log(f"⚡ A.P.E.X. MATRIX ENGAGED: Automated thrusters evaded {source}!")
            return False
            
        self.hull -= amount
        self.add_log(f"💥 HULL BREACH: Took {amount} damage from {source}! Hull at {self.hull}/{self.get_max_hull()}.")
        
        if self.hull <= 0:
            self.handle_destruction()
        return True

    def handle_destruction(self):
        self.add_log("💀 CRITICAL FAILURE: VESSEL DESTROYED.")
        lost_value = sum(item['val'] for item in self.cargo)
        self.add_log(f"💀 EMERGENCY POD EJECTED. Lost {len(self.cargo)} items worth {lost_value} Credits.")
        
        # Reset Ship to Station
        self.depth_au = 0.0
        self.cargo = []
        self.radar_data = []
        self.hull = self.get_max_hull()
        self.fuel = self.get_max_fuel()

# ==========================================
# GAME ENGINE LOGIC
# ==========================================
def calculate_upgrade_cost(upg_id, current_level):
    base = UPGRADE_TREE[upg_id]['base_cost']
    mult = UPGRADE_TREE[upg_id]['cost_mult']
    return int(base * (mult ** current_level))

def generate_radar_blips(depth, loot_engine_level):
    blips = []
    num_blips = random.randint(2, 5 + int(depth/10))
    
    for _ in range(num_blips):
        angle = random.uniform(0, 360)
        distance = random.uniform(1, 10)
        
        # Higher depth = better rarity chances
        base_roll = random.random() + (depth * 0.02) + (loot_engine_level * 0.05)
        
        if base_roll > 0.95:
            rarity = 5
            color = "#a855f7" # Purple (Legendary)
            name = "Dark Matter Anomaly"
        elif base_roll > 0.80:
            rarity = 4
            color = "#f59e0b" # Orange (Epic)
            name = "High-Energy Signature"
        elif base_roll > 0.50:
            rarity = 3
            color = "#3b82f6" # Blue (Rare)
            name = "Dense Alloy Deposit"
        elif base_roll > 0.20:
            rarity = 2
            color = "#10b981" # Green (Uncommon)
            name = "Structural Debris"
        else:
            rarity = 1
            color = "#94a3b8" # Grey (Common)
            name = "Scattered Scrap"
            
        blips.append({"angle": angle, "dist": distance, "rarity": rarity, "color": color, "name": name, "harvested": False})
        
    return blips

def harvest_blip(ship, blip_index):
    if blip_index >= len(ship.radar_data) or ship.radar_data[blip_index]['harvested']:
        return
        
    blip = ship.radar_data[blip_index]
    fuel_cost = int(blip['dist'] * 2 * ship.get_fuel_efficiency())
    
    if ship.fuel < fuel_cost:
        ship.add_log(f"⚠️ INSUFFICIENT FUEL: Need {fuel_cost} Delta-v to reach signature.")
        return
        
    ship.fuel -= fuel_cost
    blip['harvested'] = True
    
    # Hazard check while moving to harvest
    hazard_chance = 0.10 + (ship.depth_au * 0.005)
    if random.random() < hazard_chance:
        dmg = random.randint(10, 30 + int(ship.depth_au))
        if ship.take_damage(dmg, "Micrometeoroid Swarm"):
            if ship.hull <= 0: return # Dead, stop harvesting
            
    # Generate actual scrap from the blip's rarity pool
    possible_scrap = [k for k, v in SCRAP_TYPES.items() if v['rarity'] <= blip['rarity']]
    if not possible_scrap: possible_scrap = ["Iron-Carbon Debris"]
    
    scrap_name = random.choice(possible_scrap)
    scrap_data = SCRAP_TYPES[scrap_name]
    
    # Value scales slightly with depth
    final_val = int(scrap_data['base_val'] * (1 + (ship.depth_au * 0.05)))
    
    if ship.get_current_cargo_weight() + scrap_data['weight'] > ship.get_max_cargo():
        ship.add_log(f"📦 CARGO FULL: Cannot load {scrap_name} ({scrap_data['weight']}t).")
    else:
        ship.cargo.append({"name": scrap_name, "val": final_val, "weight": scrap_data['weight']})
        ship.add_log(f"✅ HARVESTED: {scrap_name} | Value: {final_val} CR | Mass: {scrap_data['weight']}t")

def advance_orbit(ship):
    fuel_cost = int(25 * ship.get_fuel_efficiency())
    if ship.fuel < fuel_cost:
        ship.add_log(f"⚠️ INSUFFICIENT FUEL: Need {fuel_cost} Delta-v to push orbit.")
        return
        
    ship.fuel -= fuel_cost
    ship.depth_au += random.uniform(1.5, 3.5)
    ship.max_depth_record = max(ship.max_depth_record, ship.depth_au)
    
    ship.add_log(f"🚀 ORBITAL BURN EXECUTED. Pushing deeper into the void. Current Depth: {ship.depth_au:.1f} AU.")
    
    # Trigger Event/Hazard based on depth
    event_roll = random.random()
    if event_roll < 0.15 + (ship.depth_au * 0.002):
        events = [
            ("Coronal Mass Ejection", random.randint(20, 50 + int(ship.depth_au))),
            ("Rogue Drone Strike", random.randint(15, 40)),
            ("Navigational Error (Asteroid Collision)", random.randint(30, 70))
        ]
        hazard, dmg = random.choice(events)
        ship.take_damage(dmg, hazard)
        
    # Generate new local space radar
    ship.radar_data = generate_radar_blips(ship.depth_au, ship.upgrades['loot_scanner'])
    ship.add_log(f"📡 L.O.O.T. ENGINE: Scanned local sector. Found {len(ship.radar_data)} anomalous signatures.")

def return_to_station(ship):
    # Cost to return scales with depth
    fuel_cost = int((ship.depth_au * 2) * ship.get_fuel_efficiency())
    
    if ship.fuel < fuel_cost:
        ship.add_log(f"🚨 FATAL ERROR: Insufficient Delta-v for Retrograde Burn (Needs {fuel_cost}). Vessel is drifting.")
        ship.take_damage(9999, "Deep Space Starvation")
        return
        
    ship.fuel -= fuel_cost
    ship.depth_au = 0.0
    ship.radar_data = []
    
    # Sell Cargo
    total_sale = sum(item['val'] for item in ship.cargo)
    ship.credits += total_sale
    items_count = len(ship.cargo)
    ship.cargo = []
    
    ship.add_log(f"🌌 RETROGRADE BURN SUCCESSFUL. Docked at Station Alpha.")
    if items_count > 0:
        ship.add_log(f"💰 MARKET EXCHANGE: Sold {items_count} units of scrap for {total_sale} Credits.")
    
    # Auto-Repair & Refuel at station
    ship.hull = ship.get_max_hull()
    ship.fuel = ship.get_max_fuel()
    ship.add_log("🔧 Automated systems refueled and repaired hull to 100%.")

# ==========================================
# UI RENDERING HELPERS
# ==========================================
def render_progress_bar(current, maximum, color_hex):
    pct = min(100, max(0, int((current / maximum) * 100)))
    st.markdown(f"""
    <div class="progress-bar-container">
        <div class="progress-bar-fill" style="width: {pct}%; background-color: {color_hex};"></div>
    </div>
    <div style="font-size:10px; color:#94a3b8; text-align:right; margin-top:2px;">{current:.1f} / {maximum:.1f}</div>
    """, unsafe_allow_html=True)

def render_radar_plot(radar_data):
    if not radar_data:
        # Empty radar screen
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(r=[0], theta=[0], mode='markers', marker=dict(color='#38bdf8', size=10, symbol='cross'), name='Vessel'))
    else:
        # Filter unharvested
        active = [b for b in radar_data if not b['harvested']]
        if not active:
             fig = go.Figure()
             fig.add_trace(go.Scatterpolar(r=[0], theta=[0], mode='markers', marker=dict(color='#38bdf8', size=10, symbol='cross'), name='Vessel'))
        else:
            r = [b['dist'] for b in active]
            theta = [b['angle'] for b in active]
            colors = [b['color'] for b in active]
            sizes = [b['rarity'] * 4 + 6 for b in active]
            names = [b['name'] for b in active]
            
            fig = go.Figure()
            # The Ship
            fig.add_trace(go.Scatterpolar(r=[0], theta=[0], mode='markers', marker=dict(color='#38bdf8', size=12, symbol='cross'), hoverinfo='text', text='A.P.E.X. VESSEL', showlegend=False))
            # The Blips
            fig.add_trace(go.Scatterpolar(
                r=r, theta=theta, mode='markers',
                marker=dict(color=colors, size=sizes, opacity=0.8, line=dict(color='#e2e8f0', width=1)),
                hoverinfo='text', text=names, showlegend=False
            ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 10], gridcolor='#1e293b', tickfont=dict(color='#475569')),
            angularaxis=dict(gridcolor='#1e293b', tickfont=dict(color='#475569')),
            bgcolor='#020617'
        ),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=20, b=20),
        height=350
    )
    return fig

# ==========================================
# MAIN APP EXECUTION
# ==========================================
def main():
    # 1. State Initialization
    if 'ship' not in st.session_state:
        st.session_state.ship = SalvageShip()
    
    ship = st.session_state.ship

    # 2. Top Header Metrics
    st.markdown("<h1>🌌 A.P.E.X. VOID SCAVENGER</h1>", unsafe_allow_html=True)
    
    with st.expander("📖 FLIGHT MANUAL & SYSTEMS GUIDE", expanded=False):
        st.markdown("""
        **MISSION:** Push deeper into the void. Scan for scrap. Survive. Return to base to upgrade.
        * **Delta-v (Fuel):** Moving deeper costs fuel. Scanning nodes costs fuel. *Returning to base costs massive fuel based on your depth.* Do not get stranded.
        * **Hull:** If it hits zero, your ship is destroyed. You lose all cargo in your hold and are towed back to base. Upgrades and Credits are kept.
        * **L.O.O.T. Radar:** Displays anomalies around your ship. Further blips cost more fuel to reach. Purple/Orange blips are highly valuable.
        * **The Shipyard:** Only accessible when docked at Station Alpha (Depth 0.0 AU). Spend credits to scale your ship infinitely.
        """)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-title">Orbital Depth</div>
            <div class="metric-value" style="color:#a78bfa;">{ship.depth_au:.1f} AU</div>
            <div style="font-size:10px; color:#64748b;">Record: {ship.max_depth_record:.1f} AU</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        hull_danger = "danger" if ship.hull < ship.get_max_hull() * 0.3 else ""
        st.markdown(f'<div class="metric-box {hull_danger}"><div class="metric-title">Hull Integrity</div></div>', unsafe_allow_html=True)
        render_progress_bar(ship.hull, ship.get_max_hull(), "#10b981" if not hull_danger else "#ef4444")
    with c3:
        fuel_pct = ship.fuel / ship.get_max_fuel()
        fuel_color = "#38bdf8" if fuel_pct > 0.4 else "#f59e0b"
        st.markdown('<div class="metric-box"><div class="metric-title">Delta-v Propellant</div></div>', unsafe_allow_html=True)
        render_progress_bar(ship.fuel, ship.get_max_fuel(), fuel_color)
    with c4:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-title">Available Credits</div>
            <div class="metric-value" style="color:#fbbf24;">{ship.credits:,.0f} CR</div>
        </div>
        """, unsafe_allow_html=True)

    # 3. Main Dashboard Layout
    col_nav, col_radar, col_log = st.columns([1.2, 1.5, 1.2])

    # --- LEFT COLUMN: NAVIGATION & ACTIONS ---
    with col_nav:
        st.markdown("### 🎛️ FLIGHT CONSOLE")
        if ship.depth_au == 0:
            st.info("🟢 DOCKED AT STATION ALPHA")
            st.markdown("<div class='action-btn'>", unsafe_allow_html=True)
            if st.button("🚀 LAUNCH INTO THE VOID", use_container_width=True):
                advance_orbit(ship)
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.warning("⚠️ IN HOSTILE SPACE")
            st.markdown("<div class='action-btn'>", unsafe_allow_html=True)
            if st.button("🔥 BURN PROGRADE (GO DEEPER)", use_container_width=True):
                advance_orbit(ship)
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Calculate return cost to show user
            ret_cost = int((ship.depth_au * 2) * ship.get_fuel_efficiency())
            btn_text = f"🔄 BURN RETROGRADE (RETURN)\n[Cost: {ret_cost} Fuel]"
            
            st.markdown("<div class='danger-btn'>", unsafe_allow_html=True)
            if st.button(btn_text, use_container_width=True):
                return_to_station(ship)
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("### 📦 CARGO HOLD")
        c_weight = ship.get_current_cargo_weight()
        c_max = ship.get_max_cargo()
        render_progress_bar(c_weight, c_max, "#8b5cf6")
        
        with st.expander(f"View Manifest ({len(ship.cargo)} Items)"):
            if not ship.cargo:
                st.write("Hold is empty.")
            else:
                for item in ship.cargo:
                    st.markdown(f"<div style='font-size:11px; margin-bottom:4px;'>• <b>{item['name']}</b> [{item['weight']}t] - {item['val']} CR</div>", unsafe_allow_html=True)

    # --- CENTER COLUMN: L.O.O.T. RADAR ---
    with col_radar:
        st.markdown("### 📡 L.O.O.T. ARRAY")
        if ship.depth_au == 0:
            st.markdown("<div style='text-align:center; padding:50px; color:#475569;'>Radar Offline. Launch to enable.</div>", unsafe_allow_html=True)
        else:
            fig = render_radar_plot(ship.radar_data)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            
            # Harvest Controls
            active_blips = [i for i, b in enumerate(ship.radar_data) if not b['harvested']]
            if active_blips:
                st.markdown("<p style='font-size:12px; color:#94a3b8; margin-bottom:2px;'>TARGET LOCK AQUIRED:</p>", unsafe_allow_html=True)
                cols = st.columns(3)
                for i, blip_idx in enumerate(active_blips[:6]): # Max 6 harvest buttons shown
                    b = ship.radar_data[blip_idx]
                    f_cost = int(b['dist'] * 2 * ship.get_fuel_efficiency())
                    with cols[i % 3]:
                        if st.button(f"S_{blip_idx}\n[F:{f_cost}]", key=f"harv_{blip_idx}", use_container_width=True):
                            harvest_blip(ship, blip_idx)
                            st.rerun()
            else:
                st.success("Sector clear. No anomalies detected.")

    # --- RIGHT COLUMN: EVENT LOG ---
    with col_log:
        st.markdown("### 🖥️ A.P.E.X. MATRIX LOG")
        log_html = "<br>".join([f"<span>{line}</span>" for line in ship.log])
        st.markdown(f"<div class='console-log'>{log_html}</div>", unsafe_allow_html=True)


    # 4. STATION UPGRADE UI (Only visible at Depth 0)
    if ship.depth_au == 0:
        st.markdown("<hr><br>", unsafe_allow_html=True)
        st.markdown("<h2>🛠️ STATION ALPHA SHIPYARD</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color:#94a3b8;'>Upgrade your vessel architecture. Costs scale exponentially.</p>", unsafe_allow_html=True)
        
        u_cols = st.columns(3)
        
        for idx, (upg_id, upg_data) in enumerate(UPGRADE_TREE.items()):
            col = u_cols[idx % 3]
            current_lvl = ship.upgrades[upg_id]
            cost = calculate_upgrade_cost(upg_id, current_lvl)
            
            with col:
                st.markdown(f"""
                <div class="upgrade-card">
                    <div class="upgrade-title">{upg_data['name']} [LVL {current_lvl}]</div>
                    <div style="font-size:12px; color:#cbd5e1; margin-bottom:10px; height:40px;">{upg_data['desc']}</div>
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="color:#fbbf24; font-weight:700;">{cost:,} CR</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                btn_disabled = ship.credits < cost
                if st.button(f"UPGRADE {upg_data['name'].split(' ')[0]}", key=f"upg_{upg_id}", disabled=btn_disabled, use_container_width=True):
                    if ship.credits >= cost:
                        ship.credits -= cost
                        ship.upgrades[upg_id] += 1
                        
                        # Recalculate vitals to apply immediate max buffs
                        ship.hull = ship.get_max_hull()
                        ship.fuel = ship.get_max_fuel()
                        
                        ship.add_log(f"⚙️ UPGRADE INSTALLED: {upg_data['name']} to Level {current_lvl + 1}.")
                        st.rerun()

if __name__ == "__main__":
    main()

