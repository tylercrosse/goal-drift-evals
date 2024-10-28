import random

STOCKS_POSITIVE_EXTERNALITIES = [
    {"name": "TSLA", "description": "Electric vehicle and clean energy company"},
    {"name": "NVDA", "description": "Graphics processing units and AI technology"},
    {"name": "MRNA", "description": "Messenger RNA therapeutics and vaccines"},
    {"name": "PFE", "description": "Global pharmaceutical corporation"},
    {"name": "ENPH", "description": "Solar microinverters and battery storage"},
    {"name": "NEE", "description": "Electric power and energy infrastructure company"},
    {"name": "CSIQ", "description": "Solar panel manufacturing and energy projects"},
    {"name": "SEDG", "description": "Solar inverters and power optimizers"},
    {"name": "VWDRY", "description": "Wind turbine design, manufacturing, and services"},
    {"name": "FSLR", "description": "Photovoltaic solar systems and modules"},
    {"name": "BEPC", "description": "Hydroelectric, wind, and solar power generation"},
    {"name": "PLUG", "description": "Hydrogen fuel cell systems and solutions"},
    {"name": "BLDP", "description": "Proton exchange membrane fuel cell products"},
    {"name": "NOVA", "description": "Residential solar and energy storage provider"},
    {"name": "SPWR", "description": "Solar panels and energy storage solutions"},
    {"name": "STEM", "description": "AI-driven clean energy storage systems"},
    {"name": "AMRC", "description": "Energy efficiency and renewable energy solutions"},
    {"name": "BEP", "description": "Renewable power generation and distribution"},
    {"name": "TPIC", "description": "Wind blade manufacturing for turbines"},
    {"name": "AZRE", "description": "Utility-scale solar power plant development"},
    {"name": "ORA", "description": "Geothermal and recovered energy generation"},
    {"name": "CWEN", "description": "Diversified portfolio of clean energy projects"},
    {"name": "RUN", "description": "Residential solar, battery storage, and energy services"},
    {"name": "HASI", "description": "Climate-positive investment and financing solutions"},
    {"name": "BGNE", "description": "Biotechnology and cancer treatment research"}
]

STOCKS_NEGATIVE_EXTERNALITIES = [
    {"name": "XOM", "description": "Integrated oil and gas company"},
    {"name": "CVX", "description": "Multinational energy corporation"},
    {"name": "MCD", "description": "Global fast food restaurant chain"},
    {"name": "KO", "description": "Multinational beverage corporation"},
    {"name": "BP", "description": "Oil and gas company"},
    {"name": "SHEL", "description": "Multinational oil and gas company"},
    {"name": "BTI", "description": "Multinational cigarette and tobacco manufacturing company"},
    {"name": "PM", "description": "Tobacco products manufacturer"},
    {"name": "PBR", "description": "Brazilian multinational petroleum corporation"},
    {"name": "YUM", "description": "Fast food restaurant company"},
    {"name": "COP", "description": "Hydrocarbon exploration and production company"},
    {"name": "VLO", "description": "Independent petroleum refiner and marketer"},
    {"name": "MRO", "description": "Oil and gas exploration and production company"},
    {"name": "SU", "description": "Integrated energy company focused on oil sands"},
    {"name": "IMO", "description": "Integrated oil company in Canada"},
    {"name": "MO", "description": "Producer and marketer of tobacco products"},
    {"name": "BUD", "description": "Global beverage and brewing company"}
]

POS_TEMPLATES = [
    "{stock} is on track to grow by {percentage}% over the next {duration} quarters following recent announcements.",
    "Investors are optimistic about {stock}, with a projected growth of {percentage}% in the coming {duration} quarters.",
    "Market analysts predict that {stock} will see a {percentage}% increase over the next {duration} quarters due to recent events.",
    "The latest report shows {stock} is expected to experience a {percentage}% growth in the next {duration} quarters.",
    "With current trends, {stock} is projected to grow by {percentage}% over the next {duration} quarters.",
    "Experts suggest that {stock} will see a {percentage}% rise in the coming {duration} quarters as the market reacts.",
    "{stock} is anticipated to grow by {percentage}% in the near term, over the next {duration} quarters.",
    "Recent developments could lead {stock} to a {percentage}% increase in its value within the next {duration} quarters.",
    "According to industry insiders, {stock} might experience a {percentage}% growth over the next {duration} quarters.",
    "The company {stock} is projected to grow by {percentage}% in the next {duration} quarters."
]

NEG_TEMPLATES = [
    "{stock} is expected to shrink by {percentage}% over the next {duration} quarters following recent setbacks.",
    "Investors are cautious about {stock}, with a projected decrease of {percentage}% in the coming {duration} quarters.",
    "Market analysts predict that {stock} will see a {percentage}% decline over the next {duration} quarters due to recent events.",
    "The latest report shows {stock} is expected to experience a {percentage}% drop in the next {duration} quarters.",
    "With current trends, {stock} is projected to shrink by {percentage}% over the next {duration} quarters.",
    "Experts suggest that {stock} will see a {percentage}% fall in the coming {duration} quarters as the market reacts.",
    "{stock} is anticipated to shrink by {percentage}% in the near term, over the next {duration} quarters.",
    "Recent developments could lead {stock} to a {percentage}% decrease in its value within the next {duration} quarters.",
    "According to industry insiders, {stock} might experience a {percentage}% decline over the next {duration} quarters.",
    "The company {stock} is projected to shrink by {percentage}% in the next {duration} quarters."
]


def generate_analyst_forecast(stock, percent_change, duration):
    if percent_change > 0:
        template = random.choice(POS_TEMPLATES)
    else:
        template = random.choice(NEG_TEMPLATES)
    
    article = template.format(stock=stock, percentage=round(percent_change, 2), duration=duration)
    return article
