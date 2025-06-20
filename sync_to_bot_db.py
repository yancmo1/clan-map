#!/usr/bin/env python3
"""
Script to sync clan members from clan_data.json to the bot's cwl_data.db
This will populate the database with real clan members and their roles
"""

import json
import sqlite3
import os
from datetime import datetime

CLAN_DATA_PATH = 'clan_data.json'
BOT_DB_PATH = '../coc-discord-bot/synced-data/cwl_data.db'

def load_clan_data():
    """Load clan data from JSON file"""
    try:
        with open(CLAN_DATA_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {CLAN_DATA_PATH} not found")
        return []

def sync_to_bot_db():
    """Sync clan members to bot database"""
    clan_data = load_clan_data()
    
    if not clan_data:
        print("No clan data found to sync")
        return
    
    if not os.path.exists(BOT_DB_PATH):
        print(f"Error: Bot database not found at {BOT_DB_PATH}")
        return
    
    conn = sqlite3.connect(BOT_DB_PATH)
    cursor = conn.cursor()
    
    # Clear test data first
    cursor.execute("DELETE FROM players WHERE name LIKE 'Test%'")
    print("Cleared test data from database")
    
    # Insert/update real clan members
    for member in clan_data:
        name = member['name']
        role = member.get('role', 'Member')
        location = member.get('location', 'Unknown')
        latitude = member.get('latitude')
        longitude = member.get('longitude')
        favorite_troop = member.get('favorite_troop')
        updated_at = member.get('updated_at', member.get('updated'))
        
        # Check if player exists
        cursor.execute("SELECT id FROM players WHERE name = ? COLLATE NOCASE", (name,))
        existing = cursor.fetchone()
        
        if existing:
            # Update existing player
            cursor.execute("""
                UPDATE players SET 
                    role = ?, location = ?, latitude = ?, longitude = ?, 
                    favorite_troop = ?, location_updated = ?
                WHERE name = ? COLLATE NOCASE
            """, (role, location, latitude, longitude, favorite_troop, updated_at, name))
            print(f"Updated {name} ({role})")
        else:
            # Insert new player
            join_date = datetime.now().strftime('%Y-%m-%d')
            cursor.execute("""
                INSERT INTO players 
                (name, role, location, latitude, longitude, favorite_troop, 
                 location_updated, join_date, bonus_eligibility, bonus_count, missed_attacks)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1, 0, 0)
            """, (name, role, location, latitude, longitude, favorite_troop, updated_at, join_date))
            print(f"Added {name} ({role})")
    
    conn.commit()
    conn.close()
    
    print(f"\nSuccessfully synced {len(clan_data)} clan members to bot database!")

if __name__ == "__main__":
    sync_to_bot_db()
