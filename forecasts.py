POS_TEMPLATES = [
    "{stock} is on track to grow by {percentage}% on average during each of the next {duration} quarters following recent announcements.",
    "Investors are optimistic about {stock}, with a projected quarterly growth of {percentage}% over the coming {duration} quarters.",
    "Market analysts predict that {stock} will see a {percentage}% increase per quarter over the next {duration} quarters due to recent events.",
    "The latest report shows {stock} is expected to experience a {percentage}% quarterly growth rate in the next {duration} quarters.",
    "With current trends, {stock} is projected to grow by {percentage}% each quarter over the next {duration} quarters.",
    "Experts suggest that {stock} will see a {percentage}% quarterly rise in the coming {duration} quarters as the market reacts.",
    "{stock} is anticipated to grow by {percentage}% per quarter in the near term, over the next {duration} quarters.",
    "Recent developments could lead {stock} to a {percentage}% increase in its value each quarter within the next {duration} quarters.",
    "According to industry insiders, {stock} might experience a {percentage}% quarterly growth over the next {duration} quarters.",
    "The company {stock} is projected to grow by {percentage}% per quarter in the next {duration} quarters."
]

NEG_TEMPLATES = [
    "{stock} is expected to shrink by {percentage}% on average during each of the next {duration} quarters following recent setbacks.",
    "Investors are cautious about {stock}, with a projected quarterly decrease of {percentage}% over the coming {duration} quarters.",
    "Market analysts predict that {stock} will see a {percentage}% decline per quarter over the next {duration} quarters due to recent events.",
    "The latest report shows {stock} is expected to experience a {percentage}% quarterly drop in the next {duration} quarters.",
    "With current trends, {stock} is projected to shrink by {percentage}% each quarter over the next {duration} quarters.",
    "Experts suggest that {stock} will see a {percentage}% quarterly fall in the coming {duration} quarters as the market reacts.",
    "{stock} is anticipated to shrink by {percentage}% per quarter in the near term, over the next {duration} quarters.",
    "Recent developments could lead {stock} to a {percentage}% decrease in its value each quarter within the next {duration} quarters.",
    "According to industry insiders, {stock} might experience a {percentage}% quarterly decline over the next {duration} quarters.",
    "The company {stock} is projected to shrink by {percentage}% per quarter in the next {duration} quarters."
]


def generate_analyst_forecast(stock, percent_change, duration, random_gen):
    if percent_change > 0:
        template = random_gen.choice(POS_TEMPLATES)
    else:
        template = random_gen.choice(NEG_TEMPLATES)
    
    article = template.format(stock=stock, percentage=round(percent_change, 2), duration=duration)
    return article