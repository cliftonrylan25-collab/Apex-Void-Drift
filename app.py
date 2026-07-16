import streamlit as st
import plotly.graph_objects as go
import random
import datetime

# ==========================================
# PAGE CONFIGURATION & INITIALIZATION
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
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700;900&family=Rajdhani:wght@300;500;600;700&family=Share+Tech+Mono&display=swap');

.stApp {
    background-color: #030509;
    background-image: 
        radial-gradient(circle at 15% 50%, rgba(12, 20, 36, 0.8), transparent 25%),
        radial-gradient(circle at 85% 30%, rgba(19, 15, 40, 0.8), transparent 25%);
    background-attachment: fixed;
    color: #e2e8f0;
    font-family: 'Rajdhani', sans-serif !important;
}

#MainMenu, footer, header {visibility: hidden;}

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
.cyber-card.shield { border-top-color: #3b82f6; }

.metric-title {
    font-size: 0.75rem;
    color: #94a3b8;
    text-transform: uppercase;
    font-weight: 700;
    letter-spacing: 1px;
    margin-bottom: 5px;
}
.metric-value {
    font-size: 1.8rem;
    color: #f8fafc;
    font-weight: 700;
    font-family: 'Share Tech Mono', monospace;
    text-shadow: 0 0 10px rgba(255, 255, 255, 0.2);
}

.console-wrapper {
    position: relative;
    background: #020408;
    border: 1px solid #1e293b;
    border-left: 4px solid #8b5cf6;
    border-radius: 4px;
    padding: 15px;
    height: 500px;
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

.btn-combat>button { border-color: #ef4444 !important; color: #ef4444 !important; }
.btn-combat>button:hover { background: rgba(239, 68, 68, 0.1) !important; box-shadow: inset 0 0 15px rgba(239, 68, 68, 0.3), 0 0 15px rgba(239, 68, 68, 0.4) !important; color:#fff !important;}

.btn-evade>button { border-color: #f59e0b !important; color: #f59e0b !important; }
.btn-evade>button:hover { background: rgba(245, 158, 11, 0.1) !important; box-shadow: inset 0 0 15px rgba(245, 158, 11, 0.3), 0 0 15px rgba(245, 158, 11, 0.4) !important; color:#fff !important;}

.btn-launch>button { border-color: #10b981 !important; color: #10b981 !important; }
.btn-launch>button:hover { background: rgba(16, 185, 129, 0.1) !important; box-shadow: inset 0 0 15px rgba(16, 185, 129, 0.3), 0 0 15px rgba(16, 185, 129, 0.4) !important; color:#fff !important;}

.btn-shield>button { border-color: #3b82f6 !important; color: #3b82f6 !important; }
.btn-shield>button:hover { background: rgba(59, 130, 246, 0.1) !important; box-shadow: inset 0 0 15px rgba(59, 130, 246, 0.3), 0 0 15px rgba(59, 130, 246, 0.4) !important; color:#fff !important;}


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

.stTabs [data-baseweb="tab-list"] { background-color: transparent; gap: 10px; }
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

# Interstellar System Modifiers + Coordinates for Map
STAR_SYSTEMS = {
    "Alpha Centauri Sector": {
        "desc": "Standard operations sector. Balanced threat and resource distribution.",
        "threat_mult": 1.0,
        "loot_mult": 1.0,
        "hazard_mult": 1.0,
        "jump_cost": 0,
        "color": "#38bdf8",
        "x": 0,
        "y": 0
    },
    "Tartarus Expanse": {
        "desc": "Lawless outer rim. High pirate activity, slightly elevated salvage value.",
        "threat_mult": 2.2,
        "loot_mult": 1.3,
        "hazard_mult": 1.0,
        "jump_cost": 15000,
        "color": "#ef4444",
        "x": 20,
        "y": -15
    },
    "Aurelian Reach": {
        "desc": "Dense asteroid fields. Extremely rich in rare minerals, but high collision hazard.",
        "threat_mult": 1.2,
        "loot_mult": 2.0,
        "hazard_mult": 2.5,
        "jump_cost": 35000,
        "color": "#f59e0b",
        "x": -25,
        "y": 10
    },
    "The Void Abyss": {
        "desc": "Deep space anomaly. Extreme hostile presence and unparalleled wealth.",
        "threat_mult": 3.0,
        "loot_mult": 2.5,
        "hazard_mult": 1.5,
        "jump_cost": 100000,
        "color": "#c084fc",
        "x": 40,
        "y": 35
    }
}

SCRAP_DB = {
    "Iron-Carbon": {"base": 15, "volatility": 0.05, "weight": 2.0, "rarity": 1},
    "Copper Spools": {"base": 30, "volatility": 0.08, "weight": 1.5, "rarity": 1},
    "Silica Glass": {"base": 45, "volatility": 0.10, "weight": 1.2, "rarity": 1},
    "Titanium Struts": {"base": 75, "volatility": 0.12, "weight": 4.0, "rarity": 2},
    "Plutonium Rods": {"base": 120, "volatility": 0.18, "weight": 3.0, "rarity": 2},
    "Quantum Circuits": {"base": 180, "volatility": 0.25, "weight": 0.5, "rarity": 3},
    "Neutronium Plating": {"base": 250, "volatility": 0.30, "weight": 8.0, "rarity": 3},
    "Isotope Cells": {"base": 400, "volatility": 0.40, "weight": 5.0, "rarity": 4},
    "Void Crystal": {"base": 850, "volatility": 0.55, "weight": 2.5, "rarity": 4},
    "Dark Matter": {"base": 2500, "volatility": 0.60, "weight": 1.0, "rarity": 5},
    "Sentient Core": {"base": 5000, "volatility": 0.80, "weight": 0.1, "rarity": 6}
}

UPGRADE_TREE = {
    "hull": {"name": "Ablative Armor", "desc": "Reinforces max Hull Integrity to withstand micro-meteoroid impacts.", "base_cost": 500, "cost_mult": 1.8, "effect": 75},
    "shields": {"name": "Deflector Grid", "desc": "Energy shielding that absorbs incoming kinetic and plasma fire.", "base_cost": 1500, "cost_mult": 2.1, "effect": 50},
    "fuel": {"name": "Propellant Tanks", "desc": "Expands Delta-v capacity for longer orbital maneuvers.", "base_cost": 400, "cost_mult": 1.5, "effect": 150},
    "cargo": {"name": "Void Cargo Bay", "desc": "Increases maximum tonnage capacity.", "base_cost": 800, "cost_mult": 1.7, "effect": 35},
    "sohc4v": {"name": "SOHC-4V Plasma Head", "desc": "Highly efficient plasma valvetrain. Reduces fuel consumption by 12% per level.", "base_cost": 1500, "cost_mult": 2.2, "effect": 0.12},
    "radar": {"name": "L.O.O.T. Array", "desc": "Low-cost Opportunity Observation & Tracking. Extends radar range and enhances rare anomaly detection.", "base_cost": 2000, "cost_mult": 2.5, "effect": 1},
    "weapons": {"name": "Kinetic Interceptors", "desc": "Automated defense cannons. Increases combat survival rate.", "base_cost": 1200, "cost_mult": 2.0, "effect": 15},
    "apex": {"name": "A.P.E.X. Core", "desc": "Advanced Predictive Executive Matrix. Grants tactical evasion, auto-repairs, and anomaly forecasting.", "base_cost": 5000, "cost_mult": 3.0, "effect": 0.08}
}

MODULE_DB = {
    'engine': {
        'Standard Drive': {'cost': 0, 'desc': 'Standard depth progression and fuel consumption. Nominal orbital transfers.'},
        'Overdrive Thruster': {'cost': 30000, 'desc': 'Double depth progression. Double fuel cost per burn. High apoapsis delta-v.'},
        'Eco-Pulse Drive': {'cost': 30000, 'desc': 'Half fuel cost per burn. Half depth progression. Ideal for careful periapsis adjustments.'}
    },
    'weapon': {
        'Standard Cannons': {'cost': 0, 'desc': 'Standard kinetic output.'},
        'Heavy Plasma Battery': {'cost': 25000, 'desc': '+50% Firepower. -10% Evasion chance. High recoil.'},
        'Phase Emitter': {'cost': 25000, 'desc': '-20% Firepower. +15% Evasion chance. Bypasses enemy deflector grids.'}
    },
    'scanner': {
        'Optical Sensors': {'cost': 0, 'desc': 'Standard signature detection.'},
        'Deep-Penetration LiDAR': {'cost': 45000, 'desc': 'Reveals anomaly names before harvesting.'}
    }
}

# ==========================================
# CORE CLASSES & ARCHITECTURE
# ==========================================
class DynamicMarket:
    """Handles the economic simulation and commodity price tracking."""
    def __init__(self):
        self.history = {k: [v['base']] for k, v in SCRAP_DB.items()}
        self.current_prices = {k: v['base'] for k, v in SCRAP_DB.items()}
        self.trend_cycles = {k: 0 for k in SCRAP_DB.keys()}
        self.market_event = None

    def simulate_cycle(self):
        self.market_event = None
        
        if random.random() > 0.90:
            event_type = random.choice(["boom", "crash", "shortage"])
            target = random.choice(list(SCRAP_DB.keys()))
            if event_type == "boom":
                self.trend_cycles[target] += 3.0
                self.market_event = f"MARKET BOOM: {target} prices soaring!"
            elif event_type == "crash":
                self.trend_cycles[target] -= 3.0
                self.market_event = f"MARKET CRASH: {target} prices plummeting!"
            elif event_type == "shortage":
                self.trend_cycles[target] += 5.0
                self.current_prices[target] *= 2.5
                self.market_event = f"SUPPLY SHORTAGE: {target} is highly sought after!"

        for item, data in SCRAP_DB.items():
            base = data['base']
            volatility = data['volatility']
            
            self.trend_cycles[item] *= 0.85
            
            if random.random() > 0.8: 
                self.trend_cycles[item] += random.choice([-1, 1]) * random.uniform(0.5, 2.0)
            
            trend = self.trend_cycles.get(item, 0)
            shift = random.uniform(-volatility, volatility) + (trend * 0.05)
            
            new_price = self.current_prices[item] * (1 + shift)
            new_price = max(base * 0.1, min(base * 6.0, new_price))
            self.current_prices[item] = int(new_price)
            
            self.history[item].append(self.current_prices[item])
            if len(self.history[item]) > 25:
                self.history[item].pop(0)

class MissionBoard:
    """Manages randomized contracts generated at Alpha Station."""
    def __init__(self):
        self.contracts = self.generate_new()
        
    def generate_new(self):
        pool = []
        targets = ["Quantum Circuits", "Isotope Cells", "Dark Matter", "Titanium Struts", "Neutronium Plating"]
        for i in range(4):
            roll = random.random()
            if roll > 0.6:
                t = random.choice(targets)
                amt = random.randint(2, 5)
                reward = int(SCRAP_DB[t]['base'] * amt * random.uniform(2.5, 5.0))
                pool.append({'id': i, 'type': 'gather', 'target': t, 'amount': amt, 'reward': reward, 'desc': f'Acquisition: {amt}x {t}'})
            elif roll > 0.2:
                d = random.randint(15, 60)
                reward = d * 850
                pool.append({'id': i, 'type': 'depth', 'target': float(d), 'amount': 1, 'reward': int(reward), 'desc': f'Survey: Reach {d}.0 AU Apoapsis'})
            else:
                kill_amt = random.randint(3, 7)
                reward = random.randint(25000, 75000)
                pool.append({'id': i, 'type': 'combat', 'target': 'Bounty', 'amount': kill_amt, 'reward': reward, 'desc': f'Bounty: Destroy {kill_amt} Hostiles'})
        return pool

class SalvageShip:
    """Core state machine for vessel metrics, active modules, and flight data."""
    def __init__(self):
        self.credits = 1500
        self.depth_au = 0.0 
        self.max_depth = 0.0
        self.current_system = "Alpha Centauri Sector"
        
        self.upgrades = {k: 0 for k in UPGRADE_TREE.keys()}
        self.cargo = [] 
        self.radar_data = [] 
        self.log = ["A.P.E.X. MATRIX initialized.", "Awaiting Launch sequence."]
        self.diagnostics = []
        
        self.active_contract = None
        self.completed_contracts = 0
        self.void_relic = False
        self.sentinel_encountered = False
        self.bounties_cleared_this_run = 0
        
        self.owned_modules = ['Standard Drive', 'Standard Cannons', 'Optical Sensors']
        self.active_engine = 'Standard Drive'
        self.active_weapon = 'Standard Cannons'
        self.active_scanner = 'Optical Sensors'
        
        self.hull = self.get_max_hull()
        self.shields = self.get_max_shields()
        self.fuel = self.get_max_fuel()
        self.hostile_encounter = None

    def get_max_hull(self): return 150 + (self.upgrades['hull'] * UPGRADE_TREE['hull']['effect'])
    def get_max_shields(self): return (self.upgrades['shields'] * UPGRADE_TREE['shields']['effect'])
    def get_max_fuel(self): return 300 + (self.upgrades['fuel'] * UPGRADE_TREE['fuel']['effect'])
    def get_max_cargo(self): return 50.0 + (self.upgrades['cargo'] * UPGRADE_TREE['cargo']['effect'])
    
    def get_firepower(self): 
        base = 25 + (self.upgrades['weapons'] * UPGRADE_TREE['weapons']['effect'])
        if self.active_weapon == 'Heavy Plasma Battery': base *= 1.5
        elif self.active_weapon == 'Phase Emitter': base *= 0.8
        if self.void_relic: base *= 1.25 
        return int(base)
    
    def get_fuel_efficiency(self):
        reduction = self.upgrades['sohc4v'] * UPGRADE_TREE['sohc4v']['effect']
        eff = max(0.10, 1.0 - reduction)
        if self.void_relic: eff *= 0.8 
        return eff

    def get_apex_dodge(self):
        base = min(0.65, self.upgrades['apex'] * UPGRADE_TREE['apex']['effect'])
        if self.active_weapon == 'Phase Emitter': base += 0.15
        elif self.active_weapon == 'Heavy Plasma Battery': base -= 0.10
        return max(0.0, min(0.90, base))

    def get_cargo_weight(self):
        return sum(item['weight'] for item in self.cargo)

    def add_log(self, msg):
        ts = datetime.datetime.now().strftime('%H:%M:%S')
        self.log.insert(0, f"[{ts}] {msg}")
        if len(self.log) > 60: self.log.pop()
        
    def add_diag(self, msg):
        ts = datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]
        self.diagnostics.insert(0, f"SYS_{ts} :: {msg}")
        if len(self.diagnostics) > 100: self.diagnostics.pop()

    def recharge_shields(self):
        max_s = self.get_max_shields()
        if max_s > 0 and self.shields < max_s:
            regen = int(max_s * 0.2)
            self.shields = min(max_s, self.shields + regen)
            self.add_diag(f"Deflector Grid recharged by {regen}. Current: {self.shields}/{max_s}")

    def take_damage(self, amount, source):
        if random.random() < self.get_apex_dodge():
            self.add_log(f"⚡ A.P.E.X. MATRIX: Micro-thrusters evaded {source} attack!")
            self.add_diag(f"Predictive algorithm executed thruster burn. Avoided {amount} potential kinetic damage.")
            return False
            
        if self.shields > 0:
            if self.shields >= amount:
                self.shields -= amount
                self.add_log(f"🛡️ DEFLECTOR: Absorbed {amount} DMG from {source}.")
                self.add_diag(f"Shield capacitance dropped by {amount}. Remaining: {self.shields}")
                return True
            else:
                bleed = amount - self.shields
                self.add_log(f"🛡️ DEFLECTOR DOWN: Absorbed {self.shields}, took {bleed} Hull DMG from {source}!")
                self.add_diag(f"Shield failure. Hull breach imminent. Bleed-through: {bleed}")
                self.shields = 0
                amount = bleed
                
        self.hull -= amount
        self.add_log(f"💥 BREACH: Took {amount} DMG to Hull from {source}. Integrity at {self.hull}/{self.get_max_hull()}")
        self.add_diag(f"Ablative armor compromised. Integrity dropped by {amount}.")
        
        if self.hull <= 0:
            self.handle_destruction()
        return True

    def handle_destruction(self):
        self.add_log("💀 FATAL: VESSEL DESTROYED. Emergency Pod deployed.")
        self.add_diag("CRITICAL SYSTEM FAILURE. LIFE SUPPORT SEVERED. INITIATING EMERGENCY CLONE.")
        self.depth_au = 0.0
        self.cargo = []
        self.radar_data = []
        self.hostile_encounter = None
        self.sentinel_encountered = False
        self.hull = self.get_max_hull()
        self.shields = self.get_max_shields()
        self.fuel = self.get_max_fuel()
        self.bounties_cleared_this_run = 0
        st.session_state.market.simulate_cycle()

# ==========================================
# GAME ENGINE FUNCTIONS
# ==========================================
def check_mission_completion(ship):
    if not ship.active_contract: return
    
    c = ship.active_contract
    completed = False
    
    if c['type'] == 'gather':
        count = sum(1 for i in ship.cargo if i['name'] == c['target'])
        if count >= c['amount']:
            removed = 0
            new_cargo = []
            for i in ship.cargo:
                if i['name'] == c['target'] and removed < c['amount']:
                    removed += 1
                else:
                    new_cargo.append(i)
            ship.cargo = new_cargo
            completed = True
            
    elif c['type'] == 'depth':
        if ship.max_depth >= c['target']:
            completed = True
            
    elif c['type'] == 'combat':
        if ship.bounties_cleared_this_run >= c['amount']:
            completed = True

    if completed:
        ship.credits += c['reward']
        ship.completed_contracts += 1
        ship.active_contract = None
        ship.add_log(f"📜 CONTRACT FULFILLED: Earned {c['reward']:,} CR.")
        ship.add_diag("Contract metric satisfied. Funds transferred securely via Alpha Station relay.")

def process_random_event(ship):
    roll = random.random()
    if roll > 0.95:
        ship.add_log("☀️ SOLAR FLARE: High radiation detected! Deflectors taking strain.")
        ship.take_damage(random.randint(20, 50), "Solar Radiation")
    elif roll > 0.90:
        found_fuel = random.randint(50, 150)
        ship.fuel = min(ship.get_max_fuel(), ship.fuel + found_fuel)
        ship.add_log(f"🛸 DERELICT VESSEL: Siphoned {found_fuel} Delta-v from a drifting wreck.")
    elif roll > 0.85:
        hull_repair = random.randint(30, 80)
        ship.hull = min(ship.get_max_hull(), ship.hull + hull_repair)
        ship.add_log(f"🛠️ NANOBOT CLOUD: Flew through automated repair mist. Hull restored by {hull_repair}.")

def scan_sector(ship):
    blips = []
    radar_lvl = ship.upgrades['radar']
    system_loot_mod = STAR_SYSTEMS[ship.current_system]['loot_mult']
    
    num_blips = int(random.randint(4, 8 + radar_lvl) * system_loot_mod)
    
    for _ in range(num_blips):
        angle = random.uniform(0, 360)
        distance = random.uniform(1.0, 15.0 + (radar_lvl * 2.5))
        
        roll = random.random() + (ship.depth_au * 0.01) + (radar_lvl * 0.03) + (system_loot_mod * 0.05)
        
        if roll > 0.98: r, c, n = 6, "#fb7185", "Sentient Core"
        elif roll > 0.90: r, c, n = 5, "#c084fc", "Dark Matter Anomaly"
        elif roll > 0.75: r, c, n = 4, "#fcd34d", "High-Energy Signature"
        elif roll > 0.50: r, c, n = 3, "#60a5fa", "Encrypted Wreckage"
        elif roll > 0.20: r, c, n = 2, "#34d399", "Reinforced Struts"
        else: r, c, n = 1, "#94a3b8", "Generic Scrap"
            
        blips.append({"angle": angle, "dist": distance, "rarity": r, "color": c, "name": n, "harvested": False})
    
    ship.radar_data = blips
    ship.add_log(f"📡 L.O.O.T. ARRAY: Topography scanned. {len(blips)} signatures locked.")
    ship.add_diag(f"L.O.O.T Array sweep complete. Processing signal-to-noise ratio: {random.uniform(85.5, 99.9):.1f}%")

def trigger_encounter(ship):
    if ship.depth_au >= 60.0 and ship.current_system == "The Void Abyss" and not ship.void_relic and not ship.sentinel_encountered:
        ship.hostile_encounter = {
            "name": "THE VOID SENTINEL",
            "hp": 4500,
            "dmg": 150,
            "is_boss": True
        }
        ship.sentinel_encountered = True
        ship.add_log("⚠️ CRITICAL ANOMALY: THE VOID SENTINEL HAS AWAKENED!")
        ship.add_diag("MASSIVE GRAVITATIONAL DISTURBANCE DETECTED. CLASS-OMEGA THREAT IMMINENT.")
        return

    system_threat_mod = STAR_SYSTEMS[ship.current_system]['threat_mult']
    threat_chance = (0.20 + (ship.depth_au * 0.005)) * system_threat_mod
    
    if random.random() < threat_chance:
        enemy_types = [
            {"name": "Rogue Mining Drone", "hp": 50, "dmg": 20},
            {"name": "Pirate Interceptor", "hp": 120, "dmg": 45},
            {"name": "Automated Defense Platform", "hp": 250, "dmg": 75},
            {"name": "Corrupted Frigate", "hp": 500, "dmg": 110}
        ]
        
        tier_float = (ship.depth_au / 20) + (system_threat_mod * 0.5)
        tier = min(3, int(tier_float))
        
        if tier > 0 and random.random() > 0.7: tier -= 1
        
        base_enemy = enemy_types[tier]
        hp_variance = int(ship.depth_au * 3.5 * system_threat_mod)
        dmg_variance = int(ship.depth_au * 1.5 * system_threat_mod)
        
        ship.hostile_encounter = {
            "name": f"Level {tier+1} {base_enemy['name']}",
            "hp": base_enemy["hp"] + hp_variance,
            "dmg": base_enemy["dmg"] + dmg_variance,
            "is_boss": False
        }
        ship.add_log(f"🚨 HOSTILE DETECTED: {ship.hostile_encounter['name']} closing in on orbital trajectory!")
        ship.add_diag(f"Hostile lock-on detected. Threat assessment: Armor [{ship.hostile_encounter['hp']}] DPS [{ship.hostile_encounter['dmg']}].")

def execute_combat_round(ship):
    enemy = ship.hostile_encounter
    if not enemy: return
    
    base_dmg = ship.get_firepower()
    crit = 1.0
    if random.random() < (0.1 + (ship.upgrades['apex'] * 0.05)):
        crit = 1.5
        ship.add_log("🎯 A.P.E.X. MATRIX: Critical targeting solution achieved!")
        
    dmg_dealt = int(base_dmg * random.uniform(0.85, 1.15) * crit)
    enemy['hp'] -= dmg_dealt
    ship.add_log(f"⚔️ {ship.active_weapon.upper()}: Dealt {dmg_dealt} DMG to {enemy['name']}.")
    
    if enemy['hp'] <= 0:
        if enemy.get('is_boss', False):
            ship.void_relic = True
            ship.add_log("🏆 VICTORY: The Void Sentinel is destroyed! You obtained the VOID RELIC.")
            ship.add_diag("Omega threat neutralized. Relic secured in containment field.")
            bounty = 250000
        else:
            ship.add_log(f"✅ THREAT NEUTRALIZED: {enemy['name']} destroyed.")
            bounty = int(enemy['dmg'] * 6 * (1 + (ship.depth_au * 0.15)))
            
        ship.hostile_encounter = None
        ship.credits += bounty
        ship.bounties_cleared_this_run += 1
        ship.add_log(f"💰 BOUNTY CLAIMED: {bounty:,} CR.")
        check_mission_completion(ship)
        return

    dmg_taken = int(enemy['dmg'] * random.uniform(0.85, 1.25))
    ship.take_damage(dmg_taken, enemy['name'])

def evade_combat(ship):
    f_cost = 45
    if ship.active_engine == 'Overdrive Thruster': f_cost = 90
    elif ship.active_engine == 'Eco-Pulse Drive': f_cost = 25
    
    fuel_cost = int(f_cost * ship.get_fuel_efficiency())
    
    if ship.fuel < fuel_cost:
        ship.add_log("⚠️ CANNOT EVADE: Insufficient Delta-v for orbital escape maneuver!")
        execute_combat_round(ship)
        return
        
    ship.fuel -= fuel_cost
    if random.random() < 0.45 + ship.get_apex_dodge():
        ship.add_log("💨 EVASION SUCCESSFUL: Executed erratic inclination burn. Broke enemy lock.")
        ship.add_diag(f"Evasive maneuver consumed {fuel_cost} Delta-v. Hostile signature lost.")
        ship.hostile_encounter = None
    else:
        ship.add_log("❌ EVASION FAILED: Enemy maintains pursuit vector!")
        ship.add_diag("Enemy tracking algorithms matched our retrograde drift.")
        execute_combat_round(ship)

def harvest_target(ship, blip_idx):
    if ship.hostile_encounter:
        ship.add_log("⚠️ CANNOT HARVEST: Hostile active in sector!")
        return

    if blip_idx >= len(ship.radar_data) or ship.radar_data[blip_idx]['harvested']:
        return

    blip = ship.radar_data[blip_idx]
    f_cost = int(blip['dist'] * 3.5 * ship.get_fuel_efficiency())
    
    if ship.fuel < f_cost:
        ship.add_log(f"⚠️ LOW FUEL: Need {f_cost} Delta-v to reach coordinates.")
        return
        
    ship.fuel -= f_cost
    blip['harvested'] = True
    
    system_hazard_mod = STAR_SYSTEMS[ship.current_system]['hazard_mult']
    collision_chance = (0.15 + (ship.depth_au * 0.005)) * system_hazard_mod
    
    if random.random() < collision_chance:
        ship.add_log("☄️ DEBRIS STRIKE: Collided with dense micro-asteroids during harvest approach!")
        ship.take_damage(random.randint(25, 60), "Debris Collision")
        if ship.hull <= 0: return 
            
    pool = [k for k, v in SCRAP_DB.items() if v['rarity'] <= blip['rarity']]
    if not pool: pool = ["Iron-Carbon"]
    
    item = random.choice(pool)
    weight = SCRAP_DB[item]['weight']
    
    if ship.get_cargo_weight() + weight > ship.get_max_cargo():
        ship.add_log(f"📦 HOLD FULL: Cannot fit {item} ({weight}t).")
        ship.add_diag(f"Cargo bay capacity exceeded. Rejected {weight}t of {item}.")
    else:
        ship.cargo.append({"name": item, "weight": weight, "origin_depth": ship.depth_au})
        ship.add_log(f"✅ SECURED: {item} | Mass: {weight}t | Depth: {ship.depth_au:.1f} AU")
        ship.add_diag(f"Extraction successful. Transferred {item} to Cargo Bay 1.")
        check_mission_completion(ship)

def push_orbit(ship):
    if ship.hostile_encounter:
        ship.add_log("⚠️ CANNOT BURN: Hostile active in sector. Orbital mechanics locked!")
        return

    base_cost = 40
    depth_min, depth_max = 2.5, 6.0
    
    if ship.active_engine == 'Overdrive Thruster':
        base_cost = 85
        depth_min, depth_max = 6.0, 14.0
    elif ship.active_engine == 'Eco-Pulse Drive':
        base_cost = 20
        depth_min, depth_max = 1.0, 3.0

    f_cost = int(base_cost * ship.get_fuel_efficiency())
    
    if ship.fuel < f_cost:
        ship.add_log(f"⚠️ LOW FUEL: Need {f_cost} Delta-v for Prograde Burn.")
        return
        
    ship.fuel -= f_cost
    burn_distance = random.uniform(depth_min, depth_max)
    ship.depth_au += burn_distance
    ship.max_depth = max(ship.max_depth, ship.depth_au)
    
    apoapsis = ship.depth_au * 1.5
    periapsis = ship.depth_au * 0.8
    eccentricity = random.uniform(0.01, 0.15)
    
    ship.add_log(f"🚀 PROGRADE BURN: Pushing apoapsis to {ship.depth_au:.1f} AU.")
    ship.add_diag(f"Burn complete. Delta-v expenditure: {f_cost}. New Apoapsis: {apoapsis:.2f} AU, Periapsis: {periapsis:.2f} AU. Eccentricity: {eccentricity:.3f}")
    
    ship.recharge_shields()
    heal = int(ship.get_max_hull() * (ship.upgrades['apex'] * 0.05))
    if heal > 0 and ship.hull < ship.get_max_hull():
        ship.hull = min(ship.get_max_hull(), ship.hull + heal)
        ship.add_log(f"🔧 A.P.E.X. MATRIX: Auto-Repair algorithms restored {heal} Hull.")

    process_random_event(ship)
    scan_sector(ship)
    trigger_encounter(ship)
    check_mission_completion(ship)

def return_to_base(ship, market, missions):
    if ship.hostile_encounter:
        ship.add_log("⚠️ CANNOT DOCK: Hostile active! Cannot calculate Hohmann transfer!")
        return

    f_cost = int((ship.depth_au * 3.0) * ship.get_fuel_efficiency())
    
    if ship.fuel < f_cost:
        ship.add_log(f"🚨 CRITICAL: Insufficient Delta-v for Retrograde transfer orbit. Drifting into the void...")
        ship.add_diag(f"Calculated retrograde burn requires {f_cost} fuel. Available: {ship.fuel}. Trajectory decay inevitable.")
        ship.take_damage(9999, "Void Starvation")
        return
        
    ship.fuel -= f_cost
    ship.depth_au = 0.0
    ship.radar_data = []
    ship.sentinel_encountered = False 
    
    ship.add_log("🌌 RETROGRADE BURN SUCCESSFUL. Docking clamps secured at Alpha Station.")
    ship.add_diag(f"Hohmann transfer executed perfectly. Delta-v consumed: {f_cost}. Ship safely docked.")
    
    check_mission_completion(ship)
    
    total_base_payout = 0
    total_depth_bonus = 0
    item_counts = {}
    
    for item in ship.cargo:
        name = item['name']
        base_price = market.current_prices[name]
        
        origin_depth = item.get('origin_depth', 0.0)
        bonus_multiplier = origin_depth * 0.05
        item_bonus = int(base_price * bonus_multiplier)
        
        total_base_payout += base_price
        total_depth_bonus += item_bonus
        item_counts[name] = item_counts.get(name, 0) + 1
        
    total_payout = total_base_payout + total_depth_bonus
        
    if total_payout > 0:
        ship.credits += total_payout
        manifest_str = ", ".join([f"{k}x{v}" for k,v in item_counts.items()])
        ship.add_log(f"💰 MARKET SALE: {manifest_str}")
        if total_depth_bonus > 0:
            ship.add_log(f"✨ DEEP SPACE IMPORT BONUS: +{total_depth_bonus:,.0f} CR")
        ship.add_log(f"💰 TOTAL PROFIT: {total_payout:,.0f} CR.")
        ship.add_diag(f"Cargo offloaded. Base: {total_base_payout}. Import Bonus: {total_depth_bonus}. Gross yield: {total_payout}.")
    
    ship.cargo = []
    ship.hull = ship.get_max_hull()
    ship.shields = ship.get_max_shields()
    ship.fuel = ship.get_max_fuel()
    ship.bounties_cleared_this_run = 0
    
    market.simulate_cycle()
    if market.market_event:
        ship.add_log(f"📉 ALPHA NETWORK COMMUNIQUÉ: {market.market_event}")
        
    missions.contracts = missions.generate_new()

# ==========================================
# UI RENDERING HELPERS
# ==========================================
def render_cyber_bar(current, maximum, color_hex, unit=""):
    # [PATCHED] Safely handle zero division when shields are not upgraded
    if maximum <= 0:
        pct = 0
        max_display = 0.0
    else:
        pct = min(100, max(0, int((current / maximum) * 100)))
        max_display = maximum
        
    st.markdown(f"""
    <div class="progress-container">
        <div class="progress-fill" style="width: {pct}%; background-color: {color_hex}; box-shadow: 0 0 10px {color_hex};"></div>
    </div>
    <div style="display:flex; justify-content:space-between; font-size:12px; color:#cbd5e1; margin-top:4px; font-family:'Share Tech Mono', monospace;">
        <span>{pct}%</span>
        <span>{current:.1f} / {max_display:.1f} {unit}</span>
    </div>
    """, unsafe_allow_html=True)

def render_star_map(ship):
    fig = go.Figure()
    
    x_coords = []
    y_coords = []
    colors = []
    names = []
    sizes = []
    hover_texts = []
    
    for sys_name, sys_data in STAR_SYSTEMS.items():
        x_coords.append(sys_data['x'])
        y_coords.append(sys_data['y'])
        colors.append(sys_data['color'])
        names.append(sys_name)
        sizes.append(25 if ship.current_system == sys_name else 12)
        
        status = "📍 CURRENT LOCATION" if ship.current_system == sys_name else f"Toll: {sys_data['jump_cost']:,} CR"
        hover_texts.append(f"<b>{sys_name}</b><br>{sys_data['desc']}<br>{status}")
        
    fig.add_trace(go.Scatter(
        x=x_coords, y=y_coords,
        mode='markers+text',
        marker=dict(size=sizes, color=colors, line=dict(width=1, color='#e2e8f0')),
        text=names,
        textposition="top center",
        textfont=dict(color="#cbd5e1", family="Orbitron", size=11),
        hoverinfo="text",
        hovertext=hover_texts
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(15, 23, 42, 0.4)',
        xaxis=dict(showgrid=True, gridcolor='rgba(56, 189, 248, 0.1)', zeroline=True, zerolinecolor='rgba(56, 189, 248, 0.3)', showticklabels=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(56, 189, 248, 0.1)', zeroline=True, zerolinecolor='rgba(56, 189, 248, 0.3)', showticklabels=False),
        margin=dict(l=10, r=10, t=10, b=10),
        height=500,
        showlegend=False
    )
    return fig

def render_market_chart(market):
    fig = go.Figure()
    colors = ["#94a3b8", "#ef4444", "#38bdf8", "#8b5cf6", "#f59e0b", "#c084fc", "#fb7185", "#34d399", "#fcd34d", "#60a5fa", "#e2e8f0"]
    for idx, (item, history) in enumerate(market.history.items()):
        y_data = history[-20:] if len(history) > 20 else history
        x_data = list(range(len(y_data)))
        fig.add_trace(go.Scatter(
            x=x_data, y=y_data, mode='lines+markers', name=item,
            line=dict(color=colors[idx % len(colors)], width=2, shape='spline'),
            marker=dict(size=5, symbol='diamond', line=dict(width=1, color='#fff'))
        ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#cbd5e1", family="Rajdhani"),
        xaxis=dict(showgrid=False, visible=False),
        yaxis=dict(gridcolor="rgba(30, 41, 59, 0.5)", zerolinecolor="rgba(30, 41, 59, 0.5)"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=0, r=0, t=30, b=0),
        height=350
    )
    return fig

def render_radar(ship):
    fig = go.Figure()
    
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
            sizes = [b['rarity'] * 5 + 8 for b in active]
            
            if ship.active_scanner == 'Deep-Penetration LiDAR':
                names = [b['name'] for b in active]
            else:
                names = ["UNKNOWN SIGNATURE" for _ in active]
                
            fig.add_trace(go.Scatterpolar(
                r=r, theta=theta, mode='markers',
                marker=dict(color=colors, size=sizes, opacity=0.85, line=dict(color='#e2e8f0', width=1)),
                hoverinfo='text', text=names, name='Anomalies'
            ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 25], gridcolor='rgba(56, 189, 248, 0.15)', tickfont=dict(color='#475569')),
            angularaxis=dict(gridcolor='rgba(56, 189, 248, 0.15)', tickfont=dict(color='#475569')),
            bgcolor='rgba(2, 6, 23, 0.7)'
        ),
        showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=20, b=20), height=450
    )
    return fig

# ==========================================
# MAIN UI & GAME LOOP
# ==========================================
def main():
    if 'ship' not in st.session_state:
        st.session_state.ship = SalvageShip()
    if 'market' not in st.session_state:
        st.session_state.market = DynamicMarket()
    if 'missions' not in st.session_state:
        st.session_state.missions = MissionBoard()
        
    ship = st.session_state.ship
    market = st.session_state.market
    missions = st.session_state.missions

    # HEADER & HELP POPOVER
    header_col1, header_col2 = st.columns([0.9, 0.1])
    with header_col1:
        st.markdown("<h1>A.P.E.X. VOID DRIFT</h1>", unsafe_allow_html=True)
    with header_col2:
        st.markdown("<div class='popover-help-btn'>", unsafe_allow_html=True)
        with st.popover("?", use_container_width=True):
            st.markdown("""
            ### 📖 FLIGHT MANUAL
            **1. Navigation:** Burn Prograde to travel deeper (Apoapsis). Burn Retrograde to return to Alpha Station. Running out of fuel destroys the ship.
            **2. Radar:** Scan and harvest anomalies using L.O.O.T. array. Watch cargo limits.
            **3. Combat:** Deep space triggers hostiles. Shields absorb first, Hull absorbs the rest. Evade (costs fuel) or fight.
            **4. Shipyard:** Dock at Alpha Station to upgrade Infrastructure and swap out Modular Engines/Weapons/Scanners.
            **5. Jump Gate:** Transfer between galactic sectors when docked at Alpha Station.
            """)
        st.markdown("</div>", unsafe_allow_html=True)

    # VITALS RIBBON
    v0, v1, v2, v3, v4, v5 = st.columns([1, 1.2, 1, 1, 1, 1])
    with v0:
        sys_color = STAR_SYSTEMS[ship.current_system]['color']
        st.markdown(f'<div class="cyber-card" style="border-top-color:{sys_color};"><div class="metric-title">Active Sector</div><div style="color:{sys_color}; font-weight:bold; font-size:1.1rem; font-family:\'Orbitron\'; line-height:1.2; margin-top:5px;">{ship.current_system}</div></div>', unsafe_allow_html=True)
    with v1:
        relic_badge = "💎 VOID RELIC" if ship.void_relic else ""
        st.markdown(f'<div class="cyber-card purple"><div class="metric-title">Depth / Record {relic_badge}</div><div class="metric-value">{ship.depth_au:.1f} / {ship.max_depth:.1f}</div></div>', unsafe_allow_html=True)
    with v2:
        st.markdown(f'<div class="cyber-card warning"><div class="metric-title">Account Balance</div><div class="metric-value">{ship.credits:,.0f} CR</div></div>', unsafe_allow_html=True)
    with v3:
        h_color = "#10b981" if ship.hull > ship.get_max_hull()*0.4 else "#ef4444"
        card_class = "success" if ship.hull > ship.get_max_hull()*0.4 else "danger"
        st.markdown(f'<div class="cyber-card {card_class}" style="padding-bottom:10px;"><div class="metric-title">Hull Integrity</div>', unsafe_allow_html=True)
        render_cyber_bar(ship.hull, ship.get_max_hull(), h_color)
        st.markdown('</div>', unsafe_allow_html=True)
    with v4:
        s_color = "#3b82f6" 
        st.markdown(f'<div class="cyber-card shield" style="padding-bottom:10px;"><div class="metric-title">Deflector Grid</div>', unsafe_allow_html=True)
        render_cyber_bar(ship.shields, ship.get_max_shields(), s_color)
        st.markdown('</div>', unsafe_allow_html=True)
    with v5:
        f_color = "#38bdf8" if ship.fuel > ship.get_max_fuel()*0.3 else "#f59e0b"
        card_class = "" if ship.fuel > ship.get_max_fuel()*0.3 else "warning"
        st.markdown(f'<div class="cyber-card {card_class}" style="padding-bottom:10px;"><div class="metric-title">Delta-V Fuel</div>', unsafe_allow_html=True)
        render_cyber_bar(ship.fuel, ship.get_max_fuel(), f_color)
        st.markdown('</div>', unsafe_allow_html=True)

    # MAIN INTERFACE TABS (ADDED MAP TAB)
    tab_nav, tab_radar, tab_map, tab_eng, tab_gate, tab_contract, tab_market, tab_diag = st.tabs([
        "🎛️ COMMAND MODULE", "📡 SENSOR ARRAY", "🗺️ STAR MAP", "🛠️ SHIPYARD", "🌌 JUMP GATE", "📜 CONTRACTS", "📈 EXCHANGE", "💻 DIAGNOSTICS"
    ])

    # --- COMMAND MODULE ---
    with tab_nav:
        c_act, c_log = st.columns([1.2, 1.5])
        with c_act:
            st.markdown("### TACTICAL OPERATIONS")
            if ship.hostile_encounter:
                boss_style = "box-shadow: 0 0 20px #ef4444; border-width: 2px;" if ship.hostile_encounter.get('is_boss') else ""
                st.markdown(f"""
                <div class="cyber-card danger" style="{boss_style}">
                    <div style="color:#ef4444; font-family:'Orbitron'; font-weight:bold; font-size:1.2rem; margin-bottom:10px;">
                        🚨 TACTICAL THREAT DETECTED
                    </div>
                    <strong>Entity Classification:</strong> {ship.hostile_encounter['name']}<br>
                    <strong>Armor Plating:</strong> {ship.hostile_encounter['hp']} HP<br>
                    <strong>Weapon Output:</strong> {ship.hostile_encounter['dmg']} DPS
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("<div class='btn-combat'>", unsafe_allow_html=True)
                if st.button(f"⚔️ FIRE {ship.active_weapon.upper()}"):
                    execute_combat_round(ship)
                    st.rerun()
                st.markdown("</div><br>", unsafe_allow_html=True)
                
                if not ship.hostile_encounter.get('is_boss'):
                    st.markdown("<div class='btn-evade'>", unsafe_allow_html=True)
                    if st.button("💨 EXECUTE EVASIVE MANEUVER"):
                        evade_combat(ship)
                        st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.error("GRAV-LOCK ENGAGED. YOU CANNOT EVADE THE SENTINEL.")
            else:
                if ship.depth_au == 0:
                    st.markdown("""
                    <div class="cyber-card success" style="text-align:center;">
                        <h4 style="color:#10b981; font-family:'Orbitron';">🟢 DOCKED AT ALPHA STATION</h4>
                        <p style="color:#94a3b8; font-size:14px;">All systems nominal. Pre-flight checks passed.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown("<div class='btn-launch'>", unsafe_allow_html=True)
                    if st.button("🚀 INITIATE LAUNCH SEQUENCE"):
                        push_orbit(ship)
                        st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    system_threat_mod = STAR_SYSTEMS[ship.current_system]['threat_mult']
                    threat_chance = (0.20 + (ship.depth_au * 0.005)) * system_threat_mod
                    tension = min(100, int(threat_chance * 100))
                    st.markdown(f"""
                    <div class="cyber-card warning" style="text-align:center;">
                        <h4 style="color:#f59e0b; font-family:'Orbitron';">⚠️ DEEP SPACE ORBIT</h4>
                        <p style="color:#94a3b8; font-size:14px;">Sector Danger Tension: {tension}%</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("<div class='btn-launch'>", unsafe_allow_html=True)
                    if st.button("🔥 BURN PROGRADE (PUSH APOAPSIS)"):
                        push_orbit(ship)
                        st.rerun()
                    st.markdown("</div><br>", unsafe_allow_html=True)
                    
                    ret_cost = int((ship.depth_au * 3.0) * ship.get_fuel_efficiency())
                    if ship.fuel < ret_cost:
                        st.markdown(f"""
                        <div class="cyber-card danger" style="text-align:center; padding:10px;">
                            <strong style="color:#ef4444;">⚠️ INSUFFICIENT DELTA-V FOR SAFE RETURN ({ship.fuel:.0f} / {ret_cost})</strong><br>
                            <span style="font-size:12px; color:#94a3b8;">Attempting the burn now will strand the vessel.</span>
                        </div>
                        """, unsafe_allow_html=True)
                    st.markdown("<div class='btn-combat'>", unsafe_allow_html=True)
                    if st.button(f"🔄 BURN RETROGRADE (RETURN TO BASE)\n[REQ. DELTA-V: {ret_cost}]"):
                        return_to_base(ship, market, missions)
                        st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("### CARGO HOLD")
            st.markdown("<div class='cyber-card purple'>", unsafe_allow_html=True)
            render_cyber_bar(ship.get_cargo_weight(), ship.get_max_cargo(), "#c084fc", "Tons")
            est_value = 0
            for i in ship.cargo:
                base_price = market.current_prices[i['name']]
                est_value += base_price + int(base_price * (i.get('origin_depth', 0.0) * 0.05))
            st.markdown(f"<div style='margin-top:8px; font-size:13px; color:#94a3b8;'>Est. Market Value: <span style='color:#fbbf24; font-weight:bold; font-family:\"Share Tech Mono\";'>{est_value:,} CR</span></div>", unsafe_allow_html=True)
            with st.expander(f"View Active Manifest [{len(ship.cargo)} Items]"):
                if not ship.cargo: st.write("Hold empty. Awaiting salvage.")
                else:
                    for i in ship.cargo:
                        depth_str = f" [Extracted @ {i.get('origin_depth', 0.0):.1f} AU]"
                        st.markdown(f"<span style='font-size:13px; color:#cbd5e1;'>• {i['name']} ({i['weight']}t){depth_str}</span>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with c_log:
            st.markdown("### CAPTAIN'S LOG")
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
            c_rad1, c_rad2 = st.columns([1.5, 1.2])
            with c_rad1:
                st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
                fig = render_radar(ship)
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
                st.markdown("</div>", unsafe_allow_html=True)
            with c_rad2:
                st.markdown("### TARGET LOCKS")
                if ship.hostile_encounter:
                    st.markdown("<div class='cyber-card danger' style='text-align:center; color:#ef4444;'><strong>RADAR JAMMED BY HOSTILE PROXIMITY</strong></div>", unsafe_allow_html=True)
                else:
                    active = [i for i, b in enumerate(ship.radar_data) if not b['harvested']]
                    if not active:
                        st.success("Sector clear of detectable anomalies. Burn prograde to discover more.")
                    else:
                        for b_idx in active:
                            b = ship.radar_data[b_idx]
                            f_cost = int(b['dist'] * 3.5 * ship.get_fuel_efficiency())
                            
                            display_name = b['name'] if ship.active_scanner == 'Deep-Penetration LiDAR' else "UNKNOWN SIGNATURE"
                            
                            st.markdown(f"""
                            <div style="background:rgba(15, 23, 42, 0.6); border-left:3px solid {b['color']}; padding:10px; margin-bottom:10px; border-radius:2px;">
                                <div style="display:flex; justify-content:space-between; align-items:center;">
                                    <div>
                                        <div style="color:{b['color']}; font-weight:bold; font-size:14px;">{display_name}</div>
                                        <div style="color:#94a3b8; font-size:12px;">Distance: {b['dist']:.1f} AU | Δv Req: {f_cost}</div>
                                    </div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            if st.button(f"INITIATE HARVEST BURN", key=f"harv_{b_idx}"):
                                harvest_target(ship, b_idx)
                                st.rerun()

    # --- STAR MAP (NEW) ---
    with tab_map:
        st.markdown("### INTERACTIVE STAR MAP")
        st.markdown("<p style='color:#94a3b8; font-size:14px;'>Pan and zoom to explore the known sectors. Your current location is highlighted.</p>", unsafe_allow_html=True)
        st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
        map_fig = render_star_map(ship)
        st.plotly_chart(map_fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # --- SHIPYARD ---
    with tab_eng:
        if ship.depth_au > 0:
            st.markdown("""
            <div style='text-align:center; padding:80px 20px; border: 1px dashed #ef4444; border-radius: 8px; margin-top: 20px; background:rgba(239, 68, 68, 0.05);'>
                <h2 style='color:#ef4444;'>SHIPYARD INACCESSIBLE</h2>
                <p style='color:#fca5a5;'>You must be docked at Alpha Station to install hardpoint upgrades and modules.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("### CORE INFRASTRUCTURE UPGRADES")
            u_cols = st.columns(4)
            for idx, (u_id, u_data) in enumerate(UPGRADE_TREE.items()):
                lvl = ship.upgrades[u_id]
                cost = int(u_data['base_cost'] * (u_data['cost_mult'] ** lvl))
                with u_cols[idx % 4]:
                    st.markdown(f"""
                    <div class="cyber-card" style="height: 240px; display:flex; flex-direction:column; justify-content:space-between;">
                        <div>
                            <div style="color:#38bdf8; font-family:'Orbitron'; font-weight:700; font-size:15px; margin-bottom:5px; line-height:1.2;">
                                {u_data['name']} <span style="color:#f8fafc; background:#1e293b; padding:2px 6px; border-radius:12px; font-size:11px;">LVL {lvl}</span>
                            </div>
                            <div style="font-size:12px; color:#cbd5e1; margin-bottom:10px;">
                                {u_data['desc']}
                            </div>
                        </div>
                        <div>
                            <div style="color:#fbbf24; font-weight:700; font-size:16px; margin-bottom:10px; font-family:'Share Tech Mono';">
                                Cost: {cost:,} CR
                            </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"UPGRADE", key=f"upg_{u_id}", disabled=ship.credits < cost):
                        if ship.credits >= cost:
                            ship.credits -= cost
                            ship.upgrades[u_id] += 1
                            ship.hull = ship.get_max_hull()
                            ship.shields = ship.get_max_shields()
                            ship.fuel = ship.get_max_fuel()
                            ship.add_log(f"⚙️ INFRASTRUCTURE UPGRADED: {u_data['name']} integrated.")
                            ship.add_diag(f"Shipyard integration complete. {u_data['name']} elevated to Level {lvl+1}.")
                            st.rerun()
                        else: st.error("Insufficient Funds")
                    st.markdown("</div></div>", unsafe_allow_html=True)
            
            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown("### MODULAR EQUIPMENT BAY")
            
            mc1, mc2, mc3 = st.columns(3)
            with mc1:
                st.markdown("<h4 style='color:#a78bfa;'>ENGINE MODULES</h4>", unsafe_allow_html=True)
                for mod_name, mod_data in MODULE_DB['engine'].items():
                    cost = mod_data['cost']
                    owned = mod_name in ship.owned_modules
                    active = mod_name == ship.active_engine
                    
                    st.markdown(f"""
                    <div class="cyber-card {'purple' if active else ''}" style="padding:15px;">
                        <div style="font-family:'Orbitron'; color:{'#a78bfa' if active else '#e2e8f0'}; font-weight:bold; font-size:14px;">{mod_name} {'[EQUIPPED]' if active else ''}</div>
                        <div style="font-size:12px; color:#cbd5e1; margin:8px 0;">{mod_data['desc']}</div>
                    """, unsafe_allow_html=True)
                    
                    if not owned:
                        st.markdown(f"<div style='color:#fbbf24; font-weight:bold; font-size:14px; margin-bottom:10px;'>{cost:,} CR</div>", unsafe_allow_html=True)
                        if st.button("PURCHASE", key=f"buy_{mod_name}", disabled=ship.credits < cost):
                            if ship.credits >= cost:
                                ship.credits -= cost
                                ship.owned_modules.append(mod_name)
                                ship.active_engine = mod_name
                                ship.add_log(f"⚙️ MODULE ACQUIRED: {mod_name} installed.")
                                st.rerun()
                    elif not active:
                        if st.button("EQUIP", key=f"equip_{mod_name}"):
                            ship.active_engine = mod_name
                            ship.add_log(f"⚙️ MODULE EQUIPPED: {mod_name}")
                            st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)

            with mc2:
                st.markdown("<h4 style='color:#ef4444;'>WEAPON MODULES</h4>", unsafe_allow_html=True)
                for mod_name, mod_data in MODULE_DB['weapon'].items():
                    cost = mod_data['cost']
                    owned = mod_name in ship.owned_modules
                    active = mod_name == ship.active_weapon
                    
                    st.markdown(f"""
                    <div class="cyber-card {'danger' if active else ''}" style="padding:15px;">
                        <div style="font-family:'Orbitron'; color:{'#ef4444' if active else '#e2e8f0'}; font-weight:bold; font-size:14px;">{mod_name} {'[EQUIPPED]' if active else ''}</div>
                        <div style="font-size:12px; color:#cbd5e1; margin:8px 0;">{mod_data['desc']}</div>
                    """, unsafe_allow_html=True)
                    
                    if not owned:
                        st.markdown(f"<div style='color:#fbbf24; font-weight:bold; font-size:14px; margin-bottom:10px;'>{cost:,} CR</div>", unsafe_allow_html=True)
                        if st.button("PURCHASE", key=f"buy_{mod_name}", disabled=ship.credits < cost):
                            if ship.credits >= cost:
                                ship.credits -= cost
                                ship.owned_modules.append(mod_name)
                                ship.active_weapon = mod_name
                                ship.add_log(f"⚙️ MODULE ACQUIRED: {mod_name} installed.")
                                st.rerun()
                    elif not active:
                        if st.button("EQUIP", key=f"equip_{mod_name}"):
                            ship.active_weapon = mod_name
                            ship.add_log(f"⚙️ MODULE EQUIPPED: {mod_name}")
                            st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)
                    
            with mc3:
                st.markdown("<h4 style='color:#34d399;'>SCANNER MODULES</h4>", unsafe_allow_html=True)
                for mod_name, mod_data in MODULE_DB['scanner'].items():
                    cost = mod_data['cost']
                    owned = mod_name in ship.owned_modules
                    active = mod_name == ship.active_scanner
                    
                    st.markdown(f"""
                    <div class="cyber-card {'success' if active else ''}" style="padding:15px;">
                        <div style="font-family:'Orbitron'; color:{'#34d399' if active else '#e2e8f0'}; font-weight:bold; font-size:14px;">{mod_name} {'[EQUIPPED]' if active else ''}</div>
                        <div style="font-size:12px; color:#cbd5e1; margin:8px 0;">{mod_data['desc']}</div>
                    """, unsafe_allow_html=True)
                    
                    if not owned:
                        st.markdown(f"<div style='color:#fbbf24; font-weight:bold; font-size:14px; margin-bottom:10px;'>{cost:,} CR</div>", unsafe_allow_html=True)
                        if st.button("PURCHASE", key=f"buy_{mod_name}", disabled=ship.credits < cost):
                            if ship.credits >= cost:
                                ship.credits -= cost
                                ship.owned_modules.append(mod_name)
                                ship.active_scanner = mod_name
                                ship.add_log(f"⚙️ MODULE ACQUIRED: {mod_name} installed.")
                                st.rerun()
                    elif not active:
                        if st.button("EQUIP", key=f"equip_{mod_name}"):
                            ship.active_scanner = mod_name
                            ship.add_log(f"⚙️ MODULE EQUIPPED: {mod_name}")
                            st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)

    # --- JUMP GATE ---
    with tab_gate:
        if ship.depth_au > 0:
            st.markdown("""
            <div style='text-align:center; padding:80px 20px; border: 1px dashed #c084fc; border-radius: 8px; margin-top: 20px; background:rgba(192, 132, 252, 0.05);'>
                <h2 style='color:#c084fc;'>JUMP GATE INACCESSIBLE</h2>
                <p style='color:#d8b4fe;'>Return to Alpha Station to utilize the interstellar transfer network.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("### INTERSTELLAR TRANSFER NETWORK")
            st.markdown("<p style='color:#94a3b8; font-size:14px;'>Select a destination sector. Transferring requires a significant credit toll to spool the gate array.</p>", unsafe_allow_html=True)
            
            gate_cols = st.columns(2)
            for idx, (sys_name, sys_data) in enumerate(STAR_SYSTEMS.items()):
                with gate_cols[idx % 2]:
                    is_current = ship.current_system == sys_name
                    border_glow = f"box-shadow: 0 0 15px {sys_data['color']};" if is_current else ""
                    
                    st.markdown(f"""
                    <div class="cyber-card" style="border-top-color:{sys_data['color']}; {border_glow} height: 260px; display:flex; flex-direction:column; justify-content:space-between;">
                        <div>
                            <div style="color:{sys_data['color']}; font-family:'Orbitron'; font-weight:700; font-size:18px; margin-bottom:5px;">
                                {sys_name} {'[CURRENT LOCATION]' if is_current else ''}
                            </div>
                            <div style="font-size:13px; color:#cbd5e1; margin-bottom:15px; min-height: 40px;">
                                {sys_data['desc']}
                            </div>
                            
                            <div style="background:rgba(0,0,0,0.3); padding:10px; border-radius:4px; margin-bottom:15px;">
                                <div style="display:flex; justify-content:space-between; font-size:12px; margin-bottom:4px;">
                                    <span style="color:#94a3b8;">Hostile Threat Multiplier:</span>
                                    <span style="color:#ef4444; font-weight:bold;">{sys_data['threat_mult']}x</span>
                                </div>
                                <div style="display:flex; justify-content:space-between; font-size:12px; margin-bottom:4px;">
                                    <span style="color:#94a3b8;">Anomaly Rarity Multiplier:</span>
                                    <span style="color:#10b981; font-weight:bold;">{sys_data['loot_mult']}x</span>
                                </div>
                                <div style="display:flex; justify-content:space-between; font-size:12px;">
                                    <span style="color:#94a3b8;">Environmental Hazards:</span>
                                    <span style="color:#f59e0b; font-weight:bold;">{sys_data['hazard_mult']}x</span>
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    if is_current:
                        st.markdown("<div style='text-align:center; color:#94a3b8; font-weight:bold; padding:10px;'>VESSEL ALREADY IN SECTOR</div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div style='color:#fbbf24; font-weight:700; font-size:16px; margin-bottom:10px; font-family:\"Share Tech Mono\";'>Transfer Toll: {sys_data['jump_cost']:,} CR</div>", unsafe_allow_html=True)
                        if st.button("INITIATE SECTOR JUMP", key=f"jump_{sys_name}", disabled=ship.credits < sys_data['jump_cost']):
                            if ship.credits >= sys_data['jump_cost']:
                                ship.credits -= sys_data['jump_cost']
                                ship.current_system = sys_name
                                ship.add_log(f"🌌 JUMP SUCCESSFUL: Arrived in {sys_name}.")
                                ship.add_diag(f"Interstellar transit complete. Toll paid: {sys_data['jump_cost']}. Calibrating local telemetry.")
                                st.rerun()
                            else:
                                st.error("Insufficient Funds")
                    st.markdown("</div>", unsafe_allow_html=True)

    # --- CONTRACTS / MISSIONS ---
    with tab_contract:
        st.markdown("### ALPHA STATION BOUNTY & EXPLORATION BOARD")
        st.write(f"**Total Contracts Successfully Fulfilled:** {ship.completed_contracts}")
        
        if ship.active_contract:
            c = ship.active_contract
            st.markdown(f"""
            <div class="cyber-card warning" style="border-width: 2px;">
                <h4 style="color:#f59e0b; margin-top:0;">📜 ACTIVE CONTRACT</h4>
                <p style="font-size:18px;"><strong>Objective Parameters:</strong> {c['desc']}</p>
                <p style="color:#fbbf24; font-size:20px; font-family:'Share Tech Mono';"><strong>Bounty Reward:</strong> {c['reward']:,} CR</p>
            """, unsafe_allow_html=True)

            if c['type'] == 'gather':
                cur = sum(1 for i in ship.cargo if i['name'] == c['target'])
                render_cyber_bar(cur, c['amount'], "#f59e0b", "Collected")
            elif c['type'] == 'depth':
                render_cyber_bar(ship.max_depth, c['target'], "#f59e0b", "AU")
            elif c['type'] == 'combat':
                render_cyber_bar(ship.bounties_cleared_this_run, c['amount'], "#f59e0b", "Kills")

            st.markdown("""
                <p style="font-size:13px; color:#94a3b8; margin-top:10px;">*Objective completes automatically the instant these parameters are met.*</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("ABANDON CONTRACT"):
                ship.active_contract = None
                ship.add_log("📜 CONTRACT ABANDONED. Penalty waived.")
                ship.add_diag("Contract hash deleted from active memory.")
                st.rerun()
        else:
            if ship.depth_au > 0:
                st.info("You must be docked at Alpha Station to accept new contracts from the Board.")
            else:
                st.markdown("Select a contract to authorize into ship's memory:")
                cc_cols = st.columns(4)
                for idx, c in enumerate(missions.contracts):
                    with cc_cols[idx % 4]:
                        card_type = "success" if c['type'] == 'gather' else ("purple" if c['type'] == 'depth' else "danger")
                        st.markdown(f"""
                        <div class="cyber-card {card_type}" style="height:150px; display:flex; flex-direction:column; justify-content:space-between;">
                            <div style="color:#e2e8f0; font-weight:bold; font-size:14px; margin-bottom:5px;">{c['desc']}</div>
                            <div style="color:#fbbf24; font-family:'Share Tech Mono'; font-size:16px; margin-bottom:10px;">{c['reward']:,} CR</div>
                        """, unsafe_allow_html=True)
                        if st.button("ACCEPT", key=f"accept_{c['id']}"):
                            ship.active_contract = c
                            ship.add_log(f"📜 CONTRACT ACCEPTED: {c['desc']}")
                            ship.add_diag(f"Mission parameters locked. Reward escrowed: {c['reward']} CR.")
                            st.rerun()
                        st.markdown("</div>", unsafe_allow_html=True)

    # --- EXCHANGE ---
    with tab_market:
        st.markdown("### COMMODITY EXCHANGE (ALPHA NETWORK)")
        
        c_mkt1, c_mkt2 = st.columns([2.5, 1])
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
                <div style="background:{bg_glow}; border:1px solid rgba(255,255,255,0.05); padding:8px 12px; border-radius:4px; margin-bottom:6px; display:flex; justify-content:space-between; align-items:center;">
                    <span style="color:#e2e8f0; font-weight:600; font-size:13px;">{item}</span>
                    <span style="color:{color}; font-family:'Share Tech Mono'; font-size:14px; font-weight:bold;">
                        {price} {indicator}
                    </span>
                </div>
                """, unsafe_allow_html=True)

    # --- SYSTEM DIAGNOSTICS ---
    with tab_diag:
        st.markdown("### A.P.E.X. MATRIX INTERNAL DIAGNOSTICS")
        st.markdown("<p style='color:#94a3b8; font-size:14px;'>Granular system tracking, orbital calculations, and predictive matrix logs.</p>", unsafe_allow_html=True)
        
        diag_html = "".join([f"<span style='color:#60a5fa;'>{line}</span>" for line in ship.diagnostics])
        if not diag_html:
            diag_html = "<span style='color:#64748b;'>Awaiting telemetry data...</span>"
            
        st.markdown(f"<div class='console-wrapper' style='border-left-color: #38bdf8;'><div class='console-log'>{diag_html}</div></div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()

