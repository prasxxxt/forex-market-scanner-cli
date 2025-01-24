#importing required libraries
from scrapper import Pair
import sys


# list of all supported major and minor currency pairs
all_pairs = [
    "EURUSD", "GBPUSD", "AUDUSD", "NZDUSD", "USDCAD", "USDCHF", "USDJPY",
    "EURGBP", "EURAUD", "EURNZD", "EURCAD", "EURCHF", "EURJPY", "CHFJPY",
    "GBPAUD", "GBPNZD", "GBPCAD", "GBPCHF", "GBPJPY", "CADCHF", "CADJPY",
    "AUDNZD", "AUDCAD", "AUDCHF", "AUDJPY", "NZDCAD", "NZDCHF", "NZDJPY"
]

# main function
def main():

    # getting pair name and validating
    name = input("Enter currency Pair Name: ").upper().strip()
    if name not in all_pairs:
        print("\nInvalid currency pair")
        print("Here is the list of all supported currency pairs")
        print(all_pairs)
        sys.exit()

    # setting up Pair class
    c = Pair(name)

    # splitting currencies
    b, q = name[:3], name[3:]

    # collecting score of all financial data
    interest_score = fundamental_scoring(c.economic_data[b]["interest-rate"]["current"], c.economic_data[q]["interest-rate"]["current"])
    gdp_score = fundamental_scoring(c.economic_data[b]["gdp-growth-rate"]["current"], c.economic_data[q]["gdp-growth-rate"]["current"])
    inflation_score = fundamental_scoring(c.economic_data[q]["inflation-rate"]["current"], c.economic_data[b]["inflation-rate"]["current"])
    unemployment_score = fundamental_scoring(c.economic_data[q]["unemployment-rate"]["current"], c.economic_data[b]["unemployment-rate"]["current"])
    cot_score = cot_scoring(c.cot_data[b], c.cot_data[q])
    retail_score = retail_scoring(c.retail_data["long"], c.retail_data["short"])
    technical_score = technical_scoring(c.technical_data["RECOMMENDATION"])

    # calculating total score out of 10
    total = interest_score + gdp_score + inflation_score + unemployment_score + cot_score + retail_score + technical_score

    # evaluating recommendation from total score
    recommendation = recommendation_scoring(total)

    # printing all results
    print(f'\nScore summary for {b}{q}')
    print("------------------------------")
    print(f'Interest Rate Score: {interest_score}\nGDP Growth Score: {gdp_score}\nInflation Rate Score: {inflation_score}\nUnemployment Rate Score: {unemployment_score}\nCOT Score: {cot_score}\nRetail Score: {retail_score}\nTechnical Score: {technical_score}')
    print("------------------------------")
    print(f'Total Score: {total}')
    print(f'Recommendation: {recommendation}')


# function to score economic indicators
def fundamental_scoring(base, quote):
    print(base, quote)
    if float(base) > float(quote):
        return 1.25
    elif float(base) < float(quote):
        return -1.25
    else:
        return 0


# function to score cot data
def cot_scoring(base, quote):
    print(base, quote)
    score = 0
    if base["long"] - base["short"] > 20:
        score += 1
    elif base["long"] - base["short"] < -20:
        score -= 1
    if quote["long"] - quote["short"] > 20:
        score -= 1
    elif quote["long"] - quote["short"] < -20:
        score += 1
    return score


# function to score retail data
def retail_scoring(long, short):
    print(long, short)
    if long > short:
        return -1
    elif long < short:
        return 1
    else:
        return 0


# function to store technical analysis data
def technical_scoring(technical):
    print(technical)
    score = 0
    if technical == "STRONG_BUY":
        return 2
    elif technical == "BUY":
        return 1
    elif technical == "STRONG_SELL":
        return -2
    elif technical == "SELL":
        return -1
    else:
        return 0


# function to evaluate overall recommendation from total score
def recommendation_scoring(score):
    if score >= 6:
        return "Strong BUY"
    elif 3 <= score < 6:
        return "BUY"
    elif -3 >= score > -6:
        return "SELL"
    elif score <= -6:
        return "Strong SELL"
    else:
        return "Neutral"


# calling main
if __name__ == "__main__":
    main()
