#constant lists for dropdown menus/json generation
RARITIES = ["Tainted", "Normal", "Uncommon", "Rare", "Epic", "Heroic", "Ascended", "Evolution"]
#colors are grey, white, green, blue, purple, red, yellow, cyan
RARITY_COLORS = {"Tainted": "#808080", "Normal": "#FFFFFF", "Uncommon": "#00FF00", "Rare": "#0000FF", "Epic": "#800080", "Heroic": "#FFFF00", "Ascended": "#FF0000", "Evolution": "#00FFFF"}
TAGS = ["Order", "Critical", "Defense", "Body", "Might", "Evolution"]
NAMELOCALIZATION = ["en", "fr", "zh-Hans", "ko", "pt","ja","de","es","ru","tr","da"]
MODIFIERTYPE = ["Additional", "Multiplier", "Compound"]
STATS = ["MaxHealth","HealthRegen","Defence","DamageMitigation","XPMultiplier","PickUpDistance","AdditionalProjectile","ProjectilePiercing","ProjectileLifeTime","ProjectileSpeed","ProjectileSize","AreaSize","KnockBack","MoveSpeed","AttackCoolDown","AttackDelay","Damage","CriticalChance","CriticalMultiplier","DashSpeed","DashDuration","DashDelay","DashCoolDown","DashCharge","DashChargePerCoolDown","GoldMultiplier","SoulCoinMultiplier","DefencePiercing","Corruption"]
ALLOCATED_MODIFIER_SLOTS = 10 #max number of modifiers is 10 (because I'm lazy), but you can change this if you want
ALLOCATED_LOCALIZATION_SLOTS=len(NAMELOCALIZATION) #have enough slots for all localizations, you don't have to use them all though