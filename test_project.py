# importing main project file
from project import *


# testing - economic indicators scoring function
def test_fundamental_scoring():
    assert fundamental_scoring(0, 0) == 0
    assert fundamental_scoring(1, 0) == 1.25
    assert fundamental_scoring(0, 1) == -1.25
    assert fundamental_scoring(-1, 1) == -1.25
    assert fundamental_scoring(100, 0) == 1.25
    assert fundamental_scoring(0, 100) == -1.25
    assert fundamental_scoring(1.01, 1) == 1.25
    assert fundamental_scoring(1, 1.2) == -1.25
    assert fundamental_scoring(4.555, 4.55) == 1.25


# tesing - commitment of traders scoring function
def test_cot_scoring():
    assert cot_scoring({"long": 30, "short": 70}, {"long": 80, "short": 20}) == -2
    assert cot_scoring({"long": 25, "short": 75}, {"long": 50, "short": 50}) == -1
    assert cot_scoring({"long": 50, "short": 50}, {"long": 80, "short": 20}) == -1
    assert cot_scoring({"long": 80, "short": 20}, {"long": 70, "short": 30}) == 0
    assert cot_scoring({"long": 10, "short": 90}, {"long": 10, "short": 90}) == 0
    assert cot_scoring({"long": 75, "short": 25}, {"long": 45, "short": 55}) == 1
    assert cot_scoring({"long": 49, "short": 51}, {"long": 20, "short": 80}) == 1
    assert cot_scoring({"long": 65, "short": 35}, {"long": 39, "short": 61}) == 2


# testing - retail sentiment scoring function
def test_retail_scoring():
    assert retail_scoring(0, 100) == 1
    assert retail_scoring(100, 0) == -1
    assert retail_scoring(50, 50) == 0
    assert retail_scoring(51, 49) == -1
    assert retail_scoring(80, 20) == -1
    assert retail_scoring(20, 80) == 1


# testing - technical indicators scoring function
def test_technical_scoring():
    assert technical_scoring("STRONG_BUY") == 2
    assert technical_scoring("STRONG_SELL") == -2
    assert technical_scoring("BUY") == 1
    assert technical_scoring("NEUTRAL") == 0
    assert technical_scoring("SELL") == -1


# testing - overall scanner recommendation output
def test_recommendation_scoring():
    assert recommendation_scoring(6) == "Strong BUY"
    assert recommendation_scoring(2) == "Neutral"
    assert recommendation_scoring(0) == "Neutral"
    assert recommendation_scoring(-6) == "Strong SELL"
    assert recommendation_scoring(8) == "Strong BUY"
    assert recommendation_scoring(-8) == "Strong SELL"
    assert recommendation_scoring(5.75) == "BUY"
    assert recommendation_scoring(-3.25) == "SELL"
    assert recommendation_scoring(3.25) == "BUY"
    assert recommendation_scoring(-4.5) == "SELL"
    
