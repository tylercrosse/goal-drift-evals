import random


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